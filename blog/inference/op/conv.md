<head><style type="text/css">h1:first-child {display:none;}</style><link rel="shortcut icon" href="https://gcore.jsdelivr.net/gh/lblbk/picgo/work/cola.svg"></head>

# 卷积实现

记录一下常见卷积实现方法，代码是c++版本

## 朴素卷积

卷积基本原理很简单, 对应每个位置相乘再相加就好，具体代码, 这里不考虑padding或者stride以及其他操作, 根据公式套一下就出来

```cc
for (int i = 0; i < o_height; i++) {
    for (int j = 0; j < o_width; j++) {
      for (int p = 0; p < kernel_h; p++) {
        for (int q = 0; q < kernel_w; q++) {
          out_data.data[i * o_height + j] +=
              in_data.data[(i + p) * width + j + q] *
              kernel.data[p * kernel_w + q];
        }
      }
    }
  }
```

## im2col gemm



## Winograd

