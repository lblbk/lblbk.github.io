# 评价指标

> 大部分常用指标在 `sklearn` 中均有对应API

### 准确率、精准率、召回率

| GT/预测 |  T   |  F   |
| :-----: | :--: | :--: |
|    T    |  TP  |  FN  |
|    F    |  FP  |  TN  |

**准确率** : 预测中预测正确的比例(越大越好) $$Acc = \frac{TP + TN}{TP + FN + FP + FN}$$

**精准率** : 指在所有检测出的目标中检测正确的概率(越大越好) $$Precision=\frac{TP}{TP+FN}$$

**召回率** : 指所有的正样本中正确识别的概率 $$Recall=\frac{TP}{TP+FN}$$

**True Positive Rate**：跟 Recall 定义一样 （越大越好) $$True Positive Rate= \frac{TP}{TP+FN}$$

**FPR** : 负样本中被预测为正的比例(越小越好) $$False Positive Rate= \frac{FP}{FP+FN}$$



**PR 曲线** 是以 Recall 为横轴，Precision 为纵轴；而 ROC曲线则是以 FPR 为横轴，TPR 为纵轴

```python
from sklearn import svm, datasets
from sklearn.model_selection import train_test_split
import numpy as np

iris = datasets.load_iris()
X = iris.data
y = iris.target

# Add noisy features
random_state = np.random.RandomState(0)
n_samples, n_features = X.shape
X = np.c_[X, random_state.randn(n_samples, 200 * n_features)]

# Limit to the two first classes, and split into training and test
X_train, X_test, y_train, y_test = train_test_split(X[y < 2], y[y < 2],
                                                    test_size=.5,
                                                    random_state=random_state)
# Create a simple classifier
classifier = svm.LinearSVC(random_state=random_state)
classifier.fit(X_train, y_train)
y_score = classifier.decision_function(X_test)

from sklearn.metrics import plot_precision_recall_curve
import matplotlib.pyplot as plt

disp = plot_precision_recall_curve(classifier, X_test, y_test)
disp.ax_.set_title('2-class Precision-Recall curve')
plt.show()
```

![image-20210120181158432](https://gcore.jsdelivr.net/gh/lblbk/picgo/work/20210120181205.png)

**ROC曲线**

![image-20210120184751043](https://gcore.jsdelivr.net/gh/lblbk/picgo/work/20210120184751.png)

### 混淆矩阵

```python
import seaborn as sns
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt

sns.set()
y_true = ["cat", "dog", "cat", "cat", "dog", "rabbit", 'cat', 'dog', 'rabbit']
y_pred = ["dog", "dog", "rabbit", "cat", "dog", "rabbit", 'cat', 'dog', 'rabbit']

labels = ["dog", "rabbit", "cat"]

C2 = confusion_matrix(y_true, y_pred, labels=labels)
sns.heatmap(C2, annot=True)

indices = range(len(C2))

plt.xticks(indices, labels)
plt.yticks(indices, labels)

plt.xlabel('predict')
plt.ylabel('gt')
plt.title('confusion_matrix')

plt.show()
```

![confusion_matrix](https://gcore.jsdelivr.net/gh/lblbk/picgo/work/20210118170351.jpeg)

***



[Precision-Recall — scikit-learn 0.24.1 documentation (scikit-learn.org)](https://scikit-learn.org/stable/auto_examples/model_selection/plot_precision_recall.html)

[Receiver Operating Characteristic (ROC) — scikit-learn 0.24.1 documentation (scikit-learn.org)](https://scikit-learn.org/stable/auto_examples/model_selection/plot_roc.html#sphx-glr-auto-examples-model-selection-plot-roc-py)

