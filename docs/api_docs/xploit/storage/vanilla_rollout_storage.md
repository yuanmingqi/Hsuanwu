#


## VanillaRolloutStorage
[source](https://github.com/RLE-Foundation/rllte/blob/main/rllte/xploit/storage/vanilla_rollout_storage.py/#L11)
```python 
VanillaRolloutStorage(
   observation_space: gym.Space, action_space: gym.Space, device: str = 'cpu',
   num_steps: int = 256, num_envs: int = 8, batch_size: int = 64, discount: float = 0.99,
   gae_lambda: float = 0.95
)
```


---
Vanilla rollout storage for on-policy algorithms.


**Args**

* **observation_space** (Space) : The observation space of environment.
* **action_space** (Space) : The action space of environment. 
* **device** (str) : Device (cpu, cuda, ...) on which the code should be run.
* **num_steps** (int) : The sample length of per rollout.
* **num_envs** (int) : The number of parallel environments.
* **batch_size** (int) : Batch size of samples.
* **discount** (float) : discount factor.
* **gae_lambda** (float) : Weighting coefficient for generalized advantage estimation (GAE).


**Returns**

Vanilla rollout storage.


**Methods:**


### .add
[source](https://github.com/RLE-Foundation/rllte/blob/main/rllte/xploit/storage/vanilla_rollout_storage.py/#L86)
```python
.add(
   obs: th.Tensor, actions: th.Tensor, rewards: th.Tensor, terminateds: th.Tensor,
   truncateds: th.Tensor, next_obs: th.Tensor, log_probs: th.Tensor,
   values: th.Tensor
)
```

---
Add sampled transitions into storage.


**Args**

* **obs** (Tensor) : Observations.
* **actions** (Tensor) : Actions.
* **rewards** (Tensor) : Rewards.
* **terminateds** (Tensor) : Terminateds.
* **truncateds** (Tensor) : Truncateds.
* **next_obs** (Tensor) : Next observations.
* **log_probs** (Tensor) : Log of the probability evaluated at `actions`.
* **values** (Tensor) : Estimated values.


**Returns**

None.

### .update
[source](https://github.com/RLE-Foundation/rllte/blob/main/rllte/xploit/storage/vanilla_rollout_storage.py/#L123)
```python
.update()
```

---
Reset the terminal state of each env.

### .compute_returns_and_advantages
[source](https://github.com/RLE-Foundation/rllte/blob/main/rllte/xploit/storage/vanilla_rollout_storage.py/#L128)
```python
.compute_returns_and_advantages(
   last_values: th.Tensor
)
```

---
Perform generalized advantage estimation (GAE).


**Args**

* **last_values** (Tensor) : Estimated values of the last step.
* **gamma** (float) : Discount factor.
* **gae_lamdba** (float) : Coefficient of GAE.


**Returns**

None.

### .sample
[source](https://github.com/RLE-Foundation/rllte/blob/main/rllte/xploit/storage/vanilla_rollout_storage.py/#L154)
```python
.sample()
```

---
Sample data from storage.
