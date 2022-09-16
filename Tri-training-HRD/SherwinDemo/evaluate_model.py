#!/usr/bin/python
# coding=utf-8
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import pandas as pd
import numpy as np

train = pd.read_csv('../AllData/labeled/test_data.csv')
x_train_columns = [x for x in train.columns if x not in ['type']]
X_train = train[x_train_columns]
y_train = train['type']

test = pd.read_csv('../AllData/labeled/test_data.csv')
x_test_columns = [x for x in test.columns if x not in ['type']]
X_test = test[x_test_columns]

y_test = test['type']
pipe_lr = Pipeline([('scl', StandardScaler()),
                    ('pca', PCA(n_components = 2)),
                    ('clf', LogisticRegression(random_state=1))])
pipe_lr.fit(X_train, y_train)
print pipe_lr.score(X_test, y_test) #用测试集评估准确率

from sklearn.model_selection import cross_val_score
scores = cross_val_score(estimator = pipe_lr,X = X_train,y = y_train,cv = 5)
print np.mean(scores)  #平均准确率
print np.std(scores)   #计算标准差  标准差是评估数据离散的程度


from sklearn.model_selection import learning_curve
train_size, train_scores, test_scores = learning_curve(estimator=pipe_lr,
                                                    X=X_train,
                                                    y=y_train,
                                                    train_sizes=np.linspace(0.1, 1, 10),#在0.1和1间线性的取10个值
                                                    cv = 5,
                                                    n_jobs=1)
train_mean = np.mean(train_scores, axis=1) #对得分矩阵train_scores各行取均值得到m列的向量 对十次评分取均值
test_mean = np.mean(test_scores, axis=1)   #对得分矩阵test_scores各行取均值得到m列的向量  对十次评分取均值

from sklearn.model_selection import validation_curve
param_range = [0.001, 0.01, 0.1, 1.0, 10.0, 100.0]
train_scores, test_scores = validation_curve(
              estimator=pipe_lr,
              X=X_train,
              y=y_train,
              param_name='clf_C',#针对管道中名称为clf的模型，调整其参数C
              param_range=param_range,#指定参数取值范围
              cv = 10)
train1_mean = np.mean(train_scores, axis=1)
test1_mean = np.mean(test_scores, axis=1)

