#


## NpuPPO
[source](https://github.com/RLE-Foundation/rllte/blob/main/rllte/xploit/agent/npu_ppo.py/#L17)
```python 
NpuPPO(
   env: gym.Env, eval_env: Optional[gym.Env] = None, tag: str = 'default', seed: int = 1,
   device: str = 'cpu', pretraining: bool = False, num_steps: int = 128,
   eval_every_episodes: int = 10, feature_dim: int = 512, batch_size: int = 256,
   lr: float = 0.00025, eps: float = 1e-05, hidden_dim: int = 512, clip_range: float = 0.1,
   clip_range_vf: float = 0.1, n_epochs: int = 4, vf_coef: float = 0.5,
   ent_coef: float = 0.01, aug_coef: float = 0.1, max_grad_norm: float = 0.5,
   network_init_method: str = 'orthogonal'
)
```


---
Proximal Policy Optimization (PPO) agent for `NPU` device.
When the `augmentation` module is invoked, this agent will transform into Data Regularized Actor-Critic (DrAC) agent.
Based on: https://github.com/yuanmingqi/pytorch-a2c-ppo-acktr-gail


**Args**

* **env** (Env) : A Gym-like environment for training.
* **eval_env** (Env) : A Gym-like environment for evaluation.
* **tag** (str) : An experiment tag.
* **seed** (int) : Random seed for reproduction.
* **device** (str) : Device (cpu, cuda, ...) on which the code should be run.
* **pretraining** (bool) : Turn on the pre-training mode.
* **num_steps** (int) : The sample length of per rollout.
* **eval_every_episodes** (int) : Evaluation interval.
* **feature_dim** (int) : Number of features extracted by the encoder.
* **batch_size** (int) : Number of samples per batch to load.
* **lr** (float) : The learning rate.
* **eps** (float) : Term added to the denominator to improve numerical stability.
* **hidden_dim** (int) : The size of the hidden layers.
* **clip_range** (float) : Clipping parameter.
* **clip_range_vf** (float) : Clipping parameter for the value function.
* **n_epochs** (int) : Times of updating the policy.
* **vf_coef** (float) : Weighting coefficient of value loss.
* **ent_coef** (float) : Weighting coefficient of entropy bonus.
* **aug_coef** (float) : Weighting coefficient of augmentation loss.
* **max_grad_norm** (float) : Maximum norm of gradients.
* **network_init_method** (str) : Network initialization method name.



**Returns**

PPO agent instance.


**Methods:**


### .mode
[source](https://github.com/RLE-Foundation/rllte/blob/main/rllte/xploit/agent/npu_ppo.py/#L136)
```python
.mode(
   training: bool = True
)
```

---
Set the training mode.


**Args**

* **training** (bool) : True (training) or False (testing).


**Returns**

None.

### .set
[source](https://github.com/RLE-Foundation/rllte/blob/main/rllte/xploit/agent/npu_ppo.py/#L148)
```python
.set(
   encoder: Optional[Any] = None, storage: Optional[Any] = None,
   distribution: Optional[Any] = None, augmentation: Optional[Any] = None,
   reward: Optional[Any] = None
)
```

---
Set a module for the agent.


**Args**

* **encoder** (Optional[Any]) : An encoder of `rllte.xploit.encoder` or a custom encoder.
* **storage** (Optional[Any]) : A storage of `rllte.xploit.storage` or a custom storage.
* **distribution** (Optional[Any]) : A distribution of `rllte.xplore.distribution` or a custom distribution.
* **augmentation** (Optional[Any]) : An augmentation of `rllte.xplore.augmentation` or a custom augmentation.
* **reward** (Optional[Any]) : A reward of `rllte.xplore.reward` or a custom reward.


**Returns**

None.

### .freeze
[source](https://github.com/RLE-Foundation/rllte/blob/main/rllte/xploit/agent/npu_ppo.py/#L178)
```python
.freeze()
```

---
Freeze the structure of the agent.

### .get_value
[source](https://github.com/RLE-Foundation/rllte/blob/main/rllte/xploit/agent/npu_ppo.py/#L192)
```python
.get_value(
   obs: th.Tensor
)
```

---
Get estimated values for observations.


**Args**

* **obs** (Tensor) : Observations.


**Returns**

Estimated values.

### .act
[source](https://github.com/RLE-Foundation/rllte/blob/main/rllte/xploit/agent/npu_ppo.py/#L203)
```python
.act(
   obs: th.Tensor, training: bool = True, step: int = 0
)
```

---
Sample actions based on observations.


**Args**

* **obs**  : Observations.
* **training**  : training mode, True or False.
* **step**  : Global training step.


**Returns**

Sampled actions.

### .update
[source](https://github.com/RLE-Foundation/rllte/blob/main/rllte/xploit/agent/npu_ppo.py/#L221)
```python
.update()
```

---
Update the agent and return training metrics such as actor loss, critic_loss, etc.


### .save
[source](https://github.com/RLE-Foundation/rllte/blob/main/rllte/xploit/agent/npu_ppo.py/#L307)
```python
.save()
```

---
Save models.

### .load
[source](https://github.com/RLE-Foundation/rllte/blob/main/rllte/xploit/agent/npu_ppo.py/#L321)
```python
.load(
   path: str
)
```

---
Load initial parameters.


**Args**

* **path** (str) : Import path.


**Returns**

None.