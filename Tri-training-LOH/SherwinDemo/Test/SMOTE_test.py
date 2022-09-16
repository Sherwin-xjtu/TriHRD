#!/usr/bin/python
# coding=utf-8
# 使用sklearn的make_classification生成不平衡数据样本
from sklearn.datasets import make_classification
# 生成一组0和1比例为9比1的样本，X为特征，y为对应的标签
X, y = make_classification(n_classes=2, class_sep=2,
                           weights=[0.9, 0.1], n_informative=3,
                           n_redundant=1, flip_y=0,
                           n_features=20, n_clusters_per_class=1,
                           n_samples=1000, random_state=10)
from collections import Counter
# 查看所生成的样本类别分布，0和1样本比例9比1，属于类别不平衡数据
print(Counter(y))
# Counter({0: 900, 1: 100})


# 使用imlbearn库中上采样方法中的SMOTE接口
from imblearn.over_sampling import SMOTE
# 定义SMOTE模型，random_state相当于随机数种子的作用
smo = SMOTE(random_state=42)
X_smo, y_smo = smo.fit_sample(X, y)
print(Counter(y_smo))
# Counter({0: 900, 1: 900})


# 可通过radio参数指定对应类别要生成的数据的数量
smo = SMOTE(ratio={1: 500 },random_state=42)
# 生成0和1比例为3比1的数据样本
X_smo, y_smo = smo.fit_sample(X, y)
print(Counter(y_smo))
# Counter({0: 900, 1: 300})

from imblearn.under_sampling import RandomUnderSampler
# 同理，也可使用ratio来指定下采样的比例
rus = RandomUnderSampler(ratio=1, random_state=0)
X_rus, y_rus = rus.fit_sample(X, y)
print X_rus
print y_rus
print(Counter(y_rus))
# Counter({0: 500, 1: 300})


