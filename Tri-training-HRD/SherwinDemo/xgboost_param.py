#!/usr/bin/python
# coding=utf-8
import pandas as pd
import numpy as np
import xgboost as xgb
from xgboost.sklearn import XGBClassifier
from sklearn import cross_validation, metrics   #Additional     scklearn functions
from sklearn.grid_search import GridSearchCV   #Perforing grid search
from xgboost import plot_importance
import matplotlib.pylab as plt

import warnings
warnings.filterwarnings("ignore")

from matplotlib.pylab import rcParams
rcParams['figure.figsize'] = 12, 4
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import sys
reload(sys)
sys.setdefaultencoding('gb18030')


#Choose all predictors except target & IDcols

def modelfit(alg, dtrain, predictors,useTrainCV=True, cv_folds=5, early_stopping_rounds=50):
    if useTrainCV:
        xgb_param = alg.get_xgb_params()
        xgtrain = xgb.DMatrix(dtrain[predictors].values, label=dtrain['type'].values)
        cvresult = xgb.cv(xgb_param, xgtrain, num_boost_round=alg.get_params()['n_estimators'], nfold=cv_folds,
            metrics='auc', early_stopping_rounds=early_stopping_rounds,show_stdv=False)
        alg.set_params(n_estimators=cvresult.shape[0])

    #Fit the algorithm on the data
    alg.fit(dtrain[predictors], dtrain['type'],eval_metric='auc')

    #Predict training set:
    dtrain_predictions = alg.predict(dtrain[predictors])
    dtrain_predprob = alg.predict_proba(dtrain[predictors])[:,1]

    #Print model report:
    print "\nModel Report"
    print "Accuracy : %.4g" % metrics.accuracy_score(dtrain['type'].values, dtrain_predictions)
    print "AUC Score (Train): %f" % metrics.roc_auc_score(dtrain['type'], dtrain_predprob)

    # feat_imp = pd.Series(alg.booster().get_fscore()).sort_values(ascending=False)
    # feat_imp.plot(kind='bar', title='Feature Importances')
    # plt.ylabel('Feature Importance Score')

    print(cvresult.shape[0])   #决策树数量
    plot_importance(alg)
    plt.show()


train = pd.read_csv("../dealData/data/Test_L_071803_t02.csv")
predictors = [x for x in train.columns if x not in ['type']]
xgb1 = XGBClassifier(
 learning_rate =0.1,
 n_estimators=1000,
 max_depth=5,
 min_child_weight=1,
 gamma=0,
 subsample=0.8,
 colsample_bytree=0.8,
 objective= 'binary:logistic',
 nthread=4,
 scale_pos_weight=1,
 seed=27)
modelfit(xgb1, train, predictors)

# param_test1 = {
#     'max_depth':range(3,10,2),
#     'min_child_weight':range(1,6,2)
# }
#
# gsearch1 = GridSearchCV(
#     estimator = XGBClassifier(learning_rate =0.1, n_estimators=140, max_depth=5,
#                               min_child_weight=1, gamma=0, subsample=0.8,colsample_bytree=0.8,
#                               objective= 'binary:logistic', nthread=4,scale_pos_weight=1, seed=27),
#     param_grid = param_test1,
#     scoring='roc_auc',
#     n_jobs=4,
#     iid=False,
#     cv=5)
#
# gsearch1.fit(train[predictors],train['type'])
# gsearch1.grid_scores
# gsearch1.best_params_
# gsearch1.best_score_