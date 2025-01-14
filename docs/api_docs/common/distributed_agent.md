#


## DistributedAgent
[source](https://github.com/RLE-Foundation/rllte/blob/main/rllte/common/distributed_agent.py/#L125)
```python 
DistributedAgent(
   env: gym.Env, eval_env: Optional[gym.Env] = None, tag: str = 'default', seed: int = 1,
   device: str = 'cpu', num_steps: int = 80, num_actors: int = 45, num_learners: int = 4,
   num_storages: int = 60, batch_size: int = 4
)
```


---
Trainer for distributed algorithms.


**Args**

* **env** (Env) : A Gym-like environment for training.
* **eval_env** (Env) : A Gym-like environment for evaluation.
* **tag** (str) : An experiment tag.
* **seed** (int) : Random seed for reproduction.
* **device** (str) : Device (cpu, cuda, ...) on which the code should be run.
* **pretraining** (bool) : Turn on pre-training model or not.
* **num_steps** (int) : The sample length of per rollout.
* **num_actors** (int) : Number of actors.
* **num_learners** (int) : Number of learners.
* **num_storages** (int) : Number of storages.
* **batch_size** (int) : Number of samples per batch to load.


**Returns**

Distributed agent instance.


**Methods:**


### .train
[source](https://github.com/RLE-Foundation/rllte/blob/main/rllte/common/distributed_agent.py/#L171)
```python
.train(
   num_train_steps: int = 30000000, init_model_path: Optional[str] = None
)
```

---
Training function.


**Args**

* **num_train_steps** (int) : Number of training steps.
* **init_model_path** (Optional[str]) : Path of Iinitial model parameters.


**Returns**

None.

### .eval
[source](https://github.com/RLE-Foundation/rllte/blob/main/rllte/common/distributed_agent.py/#L309)
```python
.eval()
```

---
Evaluation function.
