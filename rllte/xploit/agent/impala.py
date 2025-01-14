import os
import threading
import traceback
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, Tuple, List, Optional

import gymnasium as gym
import numpy as np
import torch as th
from torch import nn
from torch.nn import functional as F
from torch import multiprocessing as mp

from rllte.common.distributed_agent import DistributedAgent, Environment
from rllte.xploit.agent.networks import DistributedActorCritic, get_network_init
from rllte.xploit.encoder import MnihCnnEncoder, IdentityEncoder
from rllte.xploit.storage import DistributedStorage as Storage
from rllte.xplore.distribution import Categorical, DiagonalGaussian

class VTraceLoss:
    """V-trace loss function.

    Args:
        clip_rho_threshold (float): Clipping coefficient of `rho`.
        clip_pg_rho_threshold (float): Clipping coefficient of policy gradient `rho`.

    Returns:
        V-trace loss instance.
    """
    def __init__(
        self,
        clip_rho_threshold: float = 1.0,
        clip_pg_rho_threshold: float = 1.0,
    ) -> None:
        self.clip_rho_threshold = clip_rho_threshold
        self.clip_pg_rho_threshold = clip_pg_rho_threshold

    def compute_ISW(self, target_dist, behavior_dist, action):
        log_rhos = target_dist.log_prob(action) - behavior_dist.log_prob(action)
        return th.exp(log_rhos)

    def __call__(self, batch):
        _target_dist = batch["target_dist"]
        _behavior_dist = batch["behavior_dist"]
        _action = batch["action"]
        _baseline = batch["values"]
        _bootstrap_value = batch["bootstrap_value"]
        _values = batch["values"]
        _discounts = batch["discounts"]
        _rewards = batch["reward"]

        with th.no_grad():
            rhos = self.compute_ISW(target_dist=_target_dist, behavior_dist=_behavior_dist, action=_action)
            if self.clip_rho_threshold is not None:
                clipped_rhos = th.clamp(rhos, max=self.clip_rho_threshold)
            else:
                clipped_rhos = rhos
            cs = th.clamp(rhos, max=1.0)
            # Append bootstrapped value to get [v1, ..., v_t+1]
            values_t_plus_1 = th.cat([_values[1:], th.unsqueeze(_bootstrap_value, 0)], dim=0)
            deltas = clipped_rhos * (_rewards + _discounts * values_t_plus_1 - _values)

            acc = th.zeros_like(_bootstrap_value)
            result = []
            for t in range(_discounts.shape[0] - 1, -1, -1):
                acc = deltas[t] + _discounts[t] * cs[t] * acc
                result.append(acc)
            result.reverse()
            vs_minus_v_xs = th.stack(result)

            # Add V(x_s) to get v_s.
            vs = th.add(vs_minus_v_xs, _values)
            # Advantage for policy gradient.
            broadcasted_bootstrap_values = th.ones_like(vs[0]) * _bootstrap_value
            vs_t_plus_1 = th.cat([vs[1:], broadcasted_bootstrap_values.unsqueeze(0)], dim=0)
            if self.clip_pg_rho_threshold is not None:
                clipped_pg_rhos = th.clamp(rhos, max=self.clip_pg_rho_threshold)
            else:
                clipped_pg_rhos = rhos
            pg_advantages = clipped_pg_rhos * (_rewards + _discounts * vs_t_plus_1 - _values)

        pg_loss = -(_target_dist.log_prob(_action) * pg_advantages).sum()
        baseline_loss = F.mse_loss(vs, _baseline, reduction="sum") * 0.5
        entropy_loss = (_target_dist.entropy()).sum()

        return pg_loss, baseline_loss, entropy_loss

class IMPALA(DistributedAgent):
    """Importance Weighted Actor-Learner Architecture (IMPALA).
        Based on: https://github.com/facebookresearch/torchbeast/blob/main/torchbeast/monobeast.py

    Args:
        env (Env): A Gym-like environment for training.
        eval_env (Env): A Gym-like environment for evaluation.
        tag (str): An experiment tag.
        seed (int): Random seed for reproduction.
        device (str): Device (cpu, cuda, ...) on which the code should be run.

        num_steps (int): The sample length of per rollout.
        num_actors (int): Number of actors.
        num_learners (int): Number of learners.
        num_storages (int): Number of storages.
        feature_dim (int): Number of features extracted by the encoder.
        batch_size (int): Number of samples per batch to load.
        lr (float): The learning rate.
        eps (float): Term added to the denominator to improve numerical stability.
        hidden_dim (int): The size of the hidden layers.
        use_lstm (bool): Use LSTM in the policy network or not.
        ent_coef (float): Weighting coefficient of entropy bonus.
        baseline_coef(float): Weighting coefficient of baseline value loss.
        max_grad_norm (float): Maximum norm of gradients.
        discount (float): Discount factor.
        network_init_method (str): Network initialization method name.

    Returns:
        IMPALA agent instance.
    """

    def __init__(
        self,
        env: gym.Env, 
        eval_env: Optional[gym.Env] = None,
        tag: str = "default",
        seed: int = 1,
        device: str = "cpu",
        num_steps: int = 80,
        num_actors: int = 45,
        num_learners: int = 4,
        num_storages: int = 60,
        feature_dim: int = 512,
        batch_size: int = 4,
        lr: float = 4e-4,
        eps: float = 0.01,
        use_lstm: bool = False,
        ent_coef: float = 0.01,
        baseline_coef: float = 0.5,
        max_grad_norm: float = 40,
        discount: float = 0.99,
        network_init_method: str = "identity",
    ) -> None:
        super().__init__(env=env,
                         eval_env=eval_env,
                         tag=tag,
                         seed=seed,
                         device=device,
                         num_steps=num_steps,
                         num_actors=num_actors,
                         num_learners=num_learners,
                         batch_size=batch_size
                         )
        self.feature_dim = feature_dim
        self.lr = lr
        self.eps = eps
        self.ent_coef = ent_coef
        self.baseline_coef = baseline_coef
        self.max_grad_norm = max_grad_norm
        self.discount = discount
        self.network_init_method = network_init_method

        # build encoder
        if len(self.obs_shape) == 3:
            self.encoder = MnihCnnEncoder(
                observation_space=env.observation_space,
                feature_dim=feature_dim
            )
        elif len(self.obs_shape) == 1:
            self.encoder = IdentityEncoder(
                observation_space=env.observation_space,
                feature_dim=feature_dim
            )
            self.feature_dim = self.obs_shape[0]

        # build storage
        self.storage = Storage(
            observation_space=env.observation_space,
            action_space=env.action_space,
            device=device,
            num_steps=self.num_steps,
            num_storages=num_storages,
            batch_size=batch_size
        )

        # build distribution
        if self.action_type == "Discrete":
            self.dist = Categorical
        elif self.action_type == "Box":
            self.dist = DiagonalGaussian
        else:
            raise NotImplementedError("Unsupported action type!")

        # create models
        self.actor = DistributedActorCritic(
            obs_shape=self.action_type,
            action_shape=self.action_shape,
            action_dim=self.action_dim,
            action_type=self.action_type,
            action_range=self.action_range,
            feature_dim=feature_dim,
            use_lstm=use_lstm,
        )
        self.learner = DistributedActorCritic(
            obs_shape=self.action_type,
            action_shape=self.action_shape,
            action_dim=self.action_dim,
            action_type=self.action_type,
            action_range=self.action_range,
            feature_dim=feature_dim,
            use_lstm=use_lstm,
        )
        
    def mode(self, training: bool = True) -> None:
        """Set the training mode.

        Args:
            training (bool): True (training) or False (testing).

        Returns:
            None.
        """
        self.training = training
        self.actor.train(training)
        self.learner.train(training)

    def set(self, 
            encoder: Optional[Any] = None,
            storage: Optional[Any] = None,
            distribution: Optional[Any] = None,
            augmentation: Optional[Any] = None,
            reward: Optional[Any] = None,
            ) -> None:
        """Set a module for the agent.

        Args:
            encoder (Optional[Any]): An encoder of `rllte.xploit.encoder` or a custom encoder.
            storage (Optional[Any]): A storage of `rllte.xploit.storage` or a custom storage.
            distribution (Optional[Any]): A distribution of `rllte.xplore.distribution` or a custom distribution.
            augmentation (Optional[Any]): An augmentation of `rllte.xplore.augmentation` or a custom augmentation.
            reward (Optional[Any]): A reward of `rllte.xplore.reward` or a custom reward.

        Returns:
            None.
        """
        super().set(
            encoder=encoder,
            storage=storage,
            distribution=distribution,
            augmentation=augmentation,
            reward=reward
        )
        if encoder is not None:
            self.encoder = encoder
            assert self.encoder.feature_dim == self.feature_dim, "The `feature_dim` argument of agent and encoder must be same!"
    
    def freeze(self) -> None:
        """Freeze the structure of the agent."""
        # set encoder and distribution
        self.actor.encoder = self.encoder
        self.learner.encoder = deepcopy(self.encoder)
        self.actor.dist = self.dist
        self.learner.dist = self.dist
        # network initialization
        self.actor.apply(get_network_init(self.network_init_method))
        self.learner.apply(get_network_init(self.network_init_method))
        # share memory
        self.actor.share_memory()
        # to device
        self.learner.to(self.device)
        # create optimizers
        self.opt = th.optim.RMSprop(
            self.learner.parameters(),
            lr=self.lr,
            eps=self.eps,
        )
        # set the training mode
        self.mode(training=True)

    def act(
        self,
        env: Environment,
        actor_idx: int,
        free_queue: mp.SimpleQueue,
        full_queue: mp.SimpleQueue,
        init_actor_state_storages: List[th.Tensor],
    ) -> None:
        """Sampling function for each actor.

        Args:
            env (Environment): A Gym-like environment wrapped by `Environment`.
            actor_idx (int): The index of actor.
            free_queue (Queue): Free queue for communication.
            full_queue (Queue): Full queue for communication.
            init_actor_state_storages (List[Tensor]): Initial states for LSTM.

        Returns:
            None.
        """
        try:
            seed = actor_idx * int.from_bytes(os.urandom(4), byteorder="little")
            env_output = env.reset(seed)

            actor_state = self.actor.init_state(batch_size=1)
            actor_output, _ = self.actor.get_action(env_output, actor_state)

            while True:
                idx = free_queue.get()
                if idx is None:
                    break

                # Write old rollout end.
                for key in env_output:
                    self.storage.storages[key][idx][0, ...] = env_output[key]
                for key in actor_output:
                    self.storage.storages[key][idx][0, ...] = actor_output[key]
                for i, tensor in enumerate(actor_state):
                    init_actor_state_storages[idx][i][...] = tensor

                # Do new rollout.
                for t in range(self.num_steps):
                    with th.no_grad():
                        actor_output, actor_state = self.actor.get_action(env_output, actor_state)
                    env_output = env.step(actor_output["action"])

                    for key in env_output:
                        self.storage.storages[key][idx][t + 1, ...] = env_output[key]
                    for key in actor_output:
                        self.storage.storages[key][idx][t + 1, ...] = actor_output[key]

                full_queue.put(idx)

        except KeyboardInterrupt:
            pass  # Return silently.
        except Exception as e:
            self.logger.error(f"Exception in worker process {actor_idx}!")
            traceback.print_exc()
            raise e
        
    def update(
        self,
        batch: Dict,
        init_actor_states: Tuple[th.Tensor, ...],
        lr_scheduler: th.optim.lr_scheduler,
        lock=threading.Lock(),  # noqa B008
    ) -> Dict[str, Tuple]:
        """
        Update the learner model.

        Args:
            batch (Batch): Batch samples.
            init_actor_states (List[Tensor]): Initial states for LSTM.
            lr_scheduler (th.optim.lr_scheduler): Learning rate scheduler.
            lock (Lock): Thread lock.

        Returns:
            Training metrics.
        """
        with lock:
            learner_outputs, _ = self.learner.get_action(batch, init_actor_states)

            # Take final value function slice for bootstrapping.
            bootstrap_value = learner_outputs["baseline"][-1]

            # Move from obs[t] -> action[t] to action[t] -> obs[t].
            batch = {key: tensor[1:] for key, tensor in batch.items()}
            learner_outputs = {key: tensor[:-1] for key, tensor in learner_outputs.items()}

            discounts = (~batch["terminated"]).float() * self.discount

            batch.update(
                {
                    "discounts": discounts,
                    "bootstrap_value": bootstrap_value,
                    "target_dist": self.learner.get_dist(learner_outputs["policy_outputs"]),
                    "behavior_dist": self.learner.get_dist(batch["policy_outputs"]),
                    "values": learner_outputs["baseline"],
                }
            )

            pg_loss, baseline_loss, entropy_loss = VTraceLoss()(batch)
            total_loss = pg_loss + self.baseline_coef * baseline_loss - self.ent_coef * entropy_loss

            episode_returns = batch["episode_return"][batch["terminated"]]
            episode_steps = batch["episode_step"][batch["terminated"]]

            self.opt.zero_grad()
            total_loss.backward()
            nn.utils.clip_grad_norm_(self.learner.parameters(), self.max_grad_norm)
            self.opt.step()
            lr_scheduler.step()

            self.actor.load_state_dict(self.learner.state_dict())
            return {
                "episode_returns": tuple(episode_returns.cpu().numpy()),
                "episode_steps": tuple(episode_steps.cpu().numpy()),
                "total_loss": total_loss.item(),
                "pg_loss": pg_loss.item(),
                "baseline_loss": baseline_loss.item(),
                "entropy_loss": entropy_loss.item(),
            }

    def save(self) -> None:
        """Save models."""
        save_dir = Path.cwd() / "model"
        save_dir.mkdir(exist_ok=True)
        th.save(self.learner, save_dir / "agent.pth")
            
        self.logger.info(f"Model saved at: {save_dir}")

    def load(self, path: str) -> None:
        """Load initial parameters.

        Args:
            path (str): Import path.

        Returns:
            None.
        """
        self.logger.info(f"Loading Initial Parameters from {path}")
        actor_params = th.load(os.path.join(path, "actor.pth"), map_location=self.device)
        learner_params = th.load(os.path.join(path, "learner.pth"), map_location=self.device)
        self.actor.load_state_dict(actor_params)
        self.learner.load_state_dict(learner_params)
