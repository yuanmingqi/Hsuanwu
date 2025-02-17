#


## PPG
[source](https://github.com/RLE-Foundation/rllte/blob/main/rllte/xploit/agent/ppg.py/#L16)
```python 
PPG(
   env: gym.Env, eval_env: Optional[gym.Env] = None, tag: str = 'default', seed: int = 1,
   device: str = 'cpu', pretraining: bool = False, num_steps: int = 128,
   eval_every_episodes: int = 10, feature_dim: int = 512, batch_size: int = 256,
   lr: float = 0.00025, eps: float = 1e-05, hidden_dim: int = 256, clip_range: float = 0.2,
   clip_range_vf: float = 0.2, vf_coef: float = 0.5, ent_coef: float = 0.01,
   aug_coef: float = 0.1, max_grad_norm: float = 0.5, policy_epochs: int = 32,
   aux_epochs: int = 6, kl_coef: float = 1.0, num_aux_mini_batch: int = 4,
   num_aux_grad_accum: int = 1, network_init_method: str = 'xavier_uniform'
)
```


---
Phasic Policy Gradient (PPG) agent.
Based on: https://github.com/vwxyzjn/cleanrl/blob/master/cleanrl/ppg_procgen.py


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
* **vf_coef** (float) : Weighting coefficient of value loss.
* **ent_coef** (float) : Weighting coefficient of entropy bonus.
* **aug_coef** (float) : Weighting coefficient of augmentation loss.
* **max_grad_norm** (float) : Maximum norm of gradients.
* **policy_epochs** (int) : Number of iterations in the policy phase.
* **aux_epochs** (int) : Number of iterations in the auxiliary phase.
* **kl_coef** (float) : Weighting coefficient of divergence loss.
* **num_aux_grad_accum** (int) : Number of gradient accumulation for auxiliary phase update.
* **network_init_method** (str) : Network initialization method name.

num_aux_mini_batch (int) Number of mini-batches in auxiliary phase.


**Returns**

PPG agent instance.


**Methods:**


### .mode
[source](https://github.com/RLE-Foundation/rllte/blob/main/rllte/xploit/agent/ppg.py/#L153)
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
[source](https://github.com/RLE-Foundation/rllte/blob/main/rllte/xploit/agent/ppg.py/#L165)
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
[source](https://github.com/RLE-Foundation/rllte/blob/main/rllte/xploit/agent/ppg.py/#L195)
```python
.freeze()
```

---
Freeze the structure of the agent.

### .get_value
[source](https://github.com/RLE-Foundation/rllte/blob/main/rllte/xploit/agent/ppg.py/#L209)
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
[source](https://github.com/RLE-Foundation/rllte/blob/main/rllte/xploit/agent/ppg.py/#L220)
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
[source](https://github.com/RLE-Foundation/rllte/blob/main/rllte/xploit/agent/ppg.py/#L237)
```python
.update()
```

---
Update the agent and return training metrics such as actor loss, critic_loss, etc.


### .save
[source](https://github.com/RLE-Foundation/rllte/blob/main/rllte/xploit/agent/ppg.py/#L418)
```python
.save()
```

---
Save models.

### .load
[source](https://github.com/RLE-Foundation/rllte/blob/main/rllte/xploit/agent/ppg.py/#L432)
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
