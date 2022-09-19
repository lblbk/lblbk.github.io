<head>
	<style type="text/css">h1:first-child {display:none;}</style>
	<script type="text/javascript" src="https://gcorejs.cloudflare.com/ajax/libs/mathjax/2.7.7/latest.js?config=TeX-MML-AM_CHTML"></script>
    <script type="text/x-mathjax-config">
        MathJax.Hub.Config({
            tex2jax: {
            skipTags: ['script', 'noscript', 'style', 'textarea', 'pre'],
            inlineMath: [['$','$']]
            }
        });
    </script>
</head>

# Latex

> 记录一下平常写latex公式时常用的命令

### 希腊字母

> 常见希腊字母写法

| 希腊字母   | latex公式  | 希腊字母 | latex公式 | 希腊字母  | latex公式 |
| ---------- | ---------- | -------- | --------- | --------- | --------- |
| $\alpha$   | `\alpha`   | $\beta$  | `\beta`   | $\gamma$  | `\gamma`  |
| $\epsilon$ | `\epsilon` | $\mu$    | `\mu`     | $\delta$  | `\delta`  |
| $\zeta$    | `\zeta`    | $\eta$   | `\eta`    | $\sigma$  | `\sigma`  |
| $\pi$      | `\pi`      | $\tau$   | `\tau`    | $\lambda$ | `\lambda` |
| $\phi$     | `\phi`     | $\chi$   | `\chi`    | $\psi$    | `\psi`    |
| $\omega$   | `\omega`   | $\theta$ | `\theta`  | $\rho$    | `\rho`    |

### 数学符号

#### 基本数学符号

> 常见数学公式符号写法

| 数学符号    | latex公式   | 数学符号  | latex公式 | 数学符号         | latex公式        |
| ----------- | ----------- | --------- | --------- | ---------------- | ---------------- |
| $\hat{x}$   | `\hat{x}`   | $\bar{x}$ | `\bar{x}` | $\overline{x+y}$ | `\overline{x+y}` |
| $x_1$       | `\x_1`      | $x^1$     | `\x^1`    | $x_{1, 2}$       | `\x_{1, 2}`      |
| $\tilde{x}$ | `\tilde{x}` |           |           |                  |                  |

#### 矩阵

> 矩阵是比较复杂的公式，因此单独写一下

##### 数组

$$
\begin{array}{}
a & b \\
c & d
\end{array}
$$

latex

```latex
$$\begin{array}{}
a & b \\
c & d
\end{array}$$
```

##### 矩阵

通过扩展数组可以展示矩阵
$$
\left(
\begin{array}{}
a & b \\
c & d
\end{array}
\right)
$$
latex

```latex
\left(
\begin{array}{}
a & b \\
c & d
\end{array}
\right)
```

改变括号样式
$$
\left[
\begin{array}{}
a & b \\
c & d
\end{array}
\right]
$$

```latex
\left[
\begin{array}{}
a & b \\
c & d
\end{array}
\right]
```

##### 矩阵 专用关键词

$$
\begin{matrix}
a & b \\
c & d
\end{matrix}
$$

```latex
\begin{matrix}
a & b \\
c & d
\end{matrix}
```

**圆括号**
$$
\begin{pmatrix}
a & b \\
c & d
\end{pmatrix}
$$

```latex
\begin{pmatrix}
a & b \\
c & d
\end{pmatrix}
```

**方括号**
$$
\begin{bmatrix}
a & b \\
c & d
\end{bmatrix}
$$

```latex
\begin{bmatrix}
a & b \\
c & d
\end{bmatrix}
```

**大括号**
$$
\begin{Bmatrix}
a & b \\
c & d
\end{Bmatrix}
$$

```latex
\begin{Bmatrix}
a & b \\
c & d
\end{Bmatrix}
```

**行列式**
$$
\begin{vmatrix}
a & b \\
c & d
\end{vmatrix}
$$

```latex
\begin{vmatrix}
a & b \\
c & d
\end{vmatrix}
```

**范数**
$$
\begin{Vmatrix}
a & b \\
c & d
\end{Vmatrix}
$$

```latex
\begin{Vmatrix}
a & b \\
c & d
\end{Vmatrix}
```

##### 大型矩阵

> 简单记录一些大型矩阵的写法，平常也用不到

**n*n 矩阵**
$$
\begin{pmatrix}
a_{00} & \cdots & a_{0n} \\
\vdots & \ddots & \vdots \\
a_{n0} & \cdots & a_{nn}
\end{pmatrix}
$$

```latex
\begin{pmatrix}
a_{00} & \cdots & a_{0n} \\
\vdots & \ddots & \vdots \\
a_{n0} & \cdots & a_{nn}
\end{pmatrix}
```

**划分线条**

列线条
$$
\left(
\begin{array}{c:c|c:c}
1 & 1 & 1 & 1 \\
2 & 2 & 2 & 2 \\
3 & 3 & 3 & 3 \\
4 & 4 & 4 & 4
\end{array}
\right)
$$

```latex
\left(
\begin{array}{c:c|c:c}
1 & 1 & 1 & 1 \\
2 & 2 & 2 & 2 \\
3 & 3 & 3 & 3 \\
4 & 4 & 4 & 4
\end{array}
\right)
```

行线条
$$
\left(
\begin{array}{}
1 & 1 & 1 & 1 \\ \hline
2 & 2 & 2 & 2 \\
\hline
3 & 3 & 3 & 3 \\
\hdashline
4 & 4 & 4 & 4
\end{array}
\right)
$$

```latex
\left(
\begin{array}{}
1 & 1 & 1 & 1 \\ \hline
2 & 2 & 2 & 2 \\
\hline
3 & 3 & 3 & 3 \\
\hdashline
4 & 4 & 4 & 4
\end{array}
\right)
```

