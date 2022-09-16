
# coding=utf-8
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn import cross_validation, metrics
import matplotlib.pylab as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


train = pd.read_csv('../AllData/labeled/trianing_data.csv')
x_train_columns = [x for x in train.columns if x not in ['type']]
X_train = train[x_train_columns]
y_train = train['type']

test = pd.read_csv('../AllData/labeled/test_data.csv')
x_test_columns = [x for x in train.columns if x not in ['type']]
X_test = train[x_test_columns]
y_test = train['type']


pipe_lr = Pipeline([('scl', StandardScaler()),
                    ('pca', PCA(n_components = 2)),
                    ('clf', LogisticRegression(random_state=1))])
pipe_lr.fit(X_train, y_train)
pipe_lr.score(X_test, y_test) #用测试集评估准确率

from sklearn.model_selection import cross_val_score
scores = cross_val_score(estimator = pipe_lr,
                         X = X_train,
                         y = y_train,
                         cv = 10,    #指定K的值
                         n_jobs = 1)
print('CV accuracy scores: %s' % scores)
print('CV accuracy: %.3f +/- %.3f' % (np.mean(scores), np.std(scores)))
# print np.mean(scores)  #平均准确率
# print np.std(scores)   #计算标准差  标准差是评估数据离散的程度

import numpy as np
from sklearn.cross_validation import StratifiedKFold
kfold = StratifiedKFold(y = y_train,
                        n_folds = 10,
                        random_state = 1)
scores = []
for k, (train, test) in enumerate(kfold):
    pipe_lr.fit(X_train[train], y_train[train])
    score = pipe_lr.score(X_train[test], y_train[test])
    scores.append(score)

