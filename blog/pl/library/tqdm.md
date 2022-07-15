# tqdm

**进度条**

`pip install tqdm`

```python
from tqdm import tqdm
import time
```

**case1** 可迭代对象

```python
for i in tqdm(range(100)):
    time.sleep(0.1)
    
# output
100%|██████████| 100/100 [00:11<00:00,  9.03it/s]
```

**case2** 添加自定义描述

```python
pbar = tqdm(['a', 'b', 'c', 'd', 'e'])
for char in pbar:
    pbar.set_description("Processing {}".format(char))
    # 一样的效果
    # pbar.desc = "Processing {}".format(char)
    time.sleep(0.5)
    
# output
Processing e: 100%|██████████| 5/5 [00:02<00:00,  1.97it/s]
```

**case3** 手动控制进度

```python
with tqdm(total=200) as pbar:
    for i in range(20):
        pbar.update(10)
        time.sleep(0.1)
# output
100%|██████████| 200/200 [00:02<00:00, 90.01it/s]
```

**write方法** 多个进度条

```python
pbar = tqdm(range(10))
for i in pbar:
    if not (i % 3):
        pbar.write("Processing {}".format(i))
    time.sleep(0.1)
pbar.close()

# output
Processing 0
 30%|███       | 3/10 [00:00<00:00,  9.16it/s]Processing 3
 60%|██████    | 6/10 [00:00<00:00,  9.01it/s]Processing 6
 90%|█████████ | 9/10 [00:00<00:00,  9.02it/s]Processing 9
100%|██████████| 10/10 [00:01<00:00,  9.07it/s]
```

