#


## SAC
[source](https://github.com/RLE-Foundation/rllte/blob/main/rllte/xploit/agent/sac.py/#L20)
```python 
SAC(
   env: gym.Env, eval_env: Optional[gym.Env] = None, tag: str = 'default', seed: int = 1,
   device: str = 'cpu', pretraining: bool = False, num_init_steps: int = 2000,
   eval_every_steps: int = 5000, feature_dim: int = 50, batch_size: int = 1024,
   lr: float = 0.0001, eps: float = 1e-08, hidden_dim: int = 1024,
   critic_target_tau: float = 0.005, update_every_steps: int = 2,
   log_std_range: Tuple[float, ...] = (-5.0, 2), betas: Tuple[float, ...] = (0.9,
   0.999), temperature: float = 0.1, fixed_temperature: bool = False,
   discount: float = 0.99, network_init_method: str = 'orthogonal'
)
```


---
Soft Actor-Critic (SAC) agent.
When 'augmentation' module is invoked, this agent will transform into Data Regularized Q (DrQ) agent.
Based on: https://github.com/denisyarats/pytorch_sac


**Args**

* **env** (Env) : A Gym-like environment for training.
* **eval_env** (Env) : A Gym-like environment for evaluation.
* **tag** (str) : An experiment tag.
* **seed** (int) : Random seed for reproduction.
* **device** (str) : Device (cpu, cuda, ...) on which the code should be run.
* **pretraining** (bool) : Turn on the pre-training mode.
* **num_init_steps** (int) : Number of initial exploration steps.
* **eval_every_steps** (int) : Evaluation interval.
* **feature_dim** (int) : Number of features extracted by the encoder.
* **batch_size** (int) : Number of samples per batch to load.
* **lr** (float) : The learning rate.
* **eps** (float) : Term added to the denominator to improve numerical stability.
* **hidden_dim** (int) : The size of the hidden layers.
* **critic_target_tau** (float) : The critic Q-function soft-update rate.
* **update_every_steps** (int) : The agent update frequency.
* **log_std_range** (Tuple[float]) : Range of std for sampling actions.
* **betas** (Tuple[float]) : coefficients used for computing running averages of gradient and its square.
* **temperature** (float) : Initial temperature coefficient.
* **fixed_temperature** (bool) : Fixed temperature or not.
* **discount** (float) : Discount factor.
* **network_init_method** (str) : Network initialization method name.



**Returns**

PPO agent instance.


**Methods:**


### .mode
[source](https://github.com/RLE-Foundation/rllte/blob/main/rllte/xploit/agent/sac.py/#L143)
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
[source](https://github.com/RLE-Foundation/rllte/blob/main/rllte/xploit/agent/sac.py/#L158)
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

### .alpha
[source](https://github.com/RLE-Foundation/rllte/blob/main/rllte/xploit/agent/sac.py/#L189)
```python
.alpha()
```

---
Get the temperature coefficient.

### .freeze
[source](https://github.com/RLE-Foundation/rllte/blob/main/rllte/xploit/agent/sac.py/#L193)
```python
.freeze()
```

---
Freeze the structure of the agent.

### .act
[source](https://github.com/RLE-Foundation/rllte/blob/main/rllte/xploit/agent/sac.py/#L217)
```python
.act(
   obs: th.Tensor, training: bool = True
)
```

---
Sample actions based on observations.


**Args**

* **obs** (Tensor) : Observations.
* **training** (bool) : training mode, True or False.


**Returns**

Sampled actions.

### .update
[source](https://github.com/RLE-Foundation/rllte/blob/main/rllte/xploit/agent/sac.py/#L237)
```python
.update()
```

---
Update the agent and return training metrics such as actor loss, critic_loss, etc.


### .update_critic
[source](https://github.com/RLE-Foundation/rllte/blob/main/rllte/xploit/agent/sac.py/#L309)
```python
.update_critic(
   obs: th.Tensor, action: th.Tensor, reward: th.Tensor, terminated: th.Tensor,
   next_obs: th.Tensor, weights: th.Tensor, aug_obs: th.Tensor,
   aug_next_obs: th.Tensor
)
```

---
Update the critic network.


**Args**

* **obs** (Tensor) : Observations.
* **action** (Tensor) : Actions.
* **reward** (Tensor) : Rewards.
* **terminated** (Tensor) : Terminateds.
* **next_obs** (Tensor) : Next observations.
* **weights** (Tensor) : Batch sample weights.
* **aug_obs** (Tensor) : Augmented observations.
* **aug_next_obs** (Tensor) : Augmented next observations.


**Returns**

Critic loss metrics.

### .update_actor_and_alpha
[source](https://github.com/RLE-Foundation/rllte/blob/main/rllte/xploit/agent/sac.py/#L381)
```python
.update_actor_and_alpha(
   obs: th.Tensor, weights: th.Tensor
)
```

---
Update the actor network and temperature.


**Args**

* **obs** (Tensor) : Observations.
* **weights** (Tensor) : Batch sample weights.


**Returns**

Actor loss metrics.

### .save
[source](https://github.com/RLE-Foundation/rllte/blob/main/rllte/xploit/agent/sac.py/#L416)
```python
.save()
```

---
Save models.

### .load
[source](https://github.com/RLE-Foundation/rllte/blob/main/rllte/xploit/agent/sac.py/#L432)
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
