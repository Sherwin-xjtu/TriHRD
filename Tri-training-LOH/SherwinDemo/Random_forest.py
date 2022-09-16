
# coding=utf-8
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn import cross_validation, metrics
import matplotlib.pylab as plt

# train = pd.read_csv('../dealData/data_processing/U_data.csv')
train = pd.read_csv('../AllData/labeled/trianing_50_data.csv')
# target='Disbursed' # Disbursed的值就是二元分类的输出
# train['Disbursed'].value_counts()
x_columns = [x for x in train.columns if x not in ['type']]
X = train[x_columns]
y = train['type']
rf0 = RandomForestClassifier(oob_score=True, random_state=10)
gbm1 = rf0.fit(X,y)
print rf0.oob_score_
y_predprob = gbm1.predict_proba(X)[:,1]
print "AUC Score (Train): %f" % metrics.roc_auc_score(y, y_predprob)


# param_test1 = {'n_estimators':range(10,71,1)}
# gsearch1 = GridSearchCV(estimator = RandomForestClassifier(min_samples_split=100,
#                                   min_samples_leaf=20,max_depth=8,max_features='sqrt' ,random_state=10),
#                        param_grid = param_test1, scoring='roc_auc',cv=5)
# gsearch1.fit(X,y)
# print gsearch1.grid_scores_, gsearch1.best_params_, gsearch1.best_score_
#
# param_test2 = {'max_depth':range(3,14,2), 'min_samples_split':range(50,201,20)}
# gsearch2 = GridSearchCV(estimator = RandomForestClassifier(n_estimators= 69,
#                                   min_samples_leaf=20,max_features='sqrt' ,oob_score=True, random_state=10),
#    param_grid = param_test2, scoring='roc_auc',iid=False, cv=5)
# gsearch2.fit(X,y)
# print gsearch2.grid_scores_, gsearch2.best_params_, gsearch2.best_score_
#
# rf1 = RandomForestClassifier(n_estimators= 60, max_depth=13, min_samples_split=110,
#                                   min_samples_leaf=20,max_features='sqrt' ,oob_score=True, random_state=10)
# rf1.fit(X,y)
# print rf1.oob_score_
#
# param_test3 = {'min_samples_split':range(2,60,4), 'min_samples_leaf':range(10,60,10)}
# gsearch3 = GridSearchCV(estimator = RandomForestClassifier(n_estimators= 69, max_depth=3,
#                                   max_features='sqrt' ,oob_score=True, random_state=10),
#    param_grid = param_test3, scoring='roc_auc',iid=False, cv=5)
# gsearch3.fit(X,y)
# print gsearch3.grid_scores_, gsearch3.best_params_, gsearch3.best_score_

# param_test4 = {'max_features':range(3,5,2)}
# gsearch4 = GridSearchCV(estimator = RandomForestClassifier(n_estimators= 69, max_depth=3, min_samples_split=22,
#                                   min_samples_leaf=10 ,oob_score=True, random_state=10),
#    param_grid = param_test4, scoring='roc_auc',iid=False, cv=5)
# gsearch4.fit(X,y)
# print gsearch4.grid_scores_, gsearch4.best_params_, gsearch4.best_score_

rf2 = RandomForestClassifier(n_estimators= 69, max_depth=3, min_samples_split=22,
                                  min_samples_leaf=10,max_features=3 ,oob_score=True, random_state=10)
rf2.fit(X,y)
print rf2.oob_score_



















#
# import numpy as np
# import pandas
# from sklearn.ensemble import RandomForestClassifier
#
# tdf = pandas.DataFrame(tp)
# fdf = pandas.DataFrame(fp)
#
# tdf["tag"] = "TP"
# fdf["tag"] = "FP"
#
# allrows = pandas.concat([tdf, fdf])
#
# kwargs = {"n_jobs": 8,
#           "max_depth": 12,
#           "min_samples_leaf": 50,
#           "n_estimators": 50,
#           "max_features": None,
#           "verbose": 10,
#           }
#
# clf = RandomForestClassifier(**kwargs)
#
# clf.fit(allrows[columns].values, allrows["tag"].values, allrows["weight"].values)
#
# # add audit trail into the model output:
# clf.columns = columns
