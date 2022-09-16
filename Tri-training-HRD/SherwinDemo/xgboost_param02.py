#Import libraries:
import pandas as pd
import numpy as np
import xgboost as xgb
from xgboost.sklearn import XGBClassifier
from sklearn import cross_validation, metrics   #Additional scklearn functions
from sklearn.grid_search import GridSearchCV   #Perforing grid search
import warnings
warnings.filterwarnings('ignore')
import matplotlib.pylab as plt
# %matplotlib inline
from matplotlib.pylab import rcParams
rcParams['figure.figsize'] = 12, 4

train = pd.read_csv("../dealData/data/Test_L__072302_t_scale.csv")

target = 'type'
IDcol = 'ID'


def modelfit(alg, dtrain, predictors, useTrainCV=True, cv_folds=5, early_stopping_rounds=50):
    if useTrainCV:
        xgb_param = alg.get_xgb_params()
        xgtrain = xgb.DMatrix(dtrain[predictors].values, label=dtrain[target].values)
        cvresult = xgb.cv(xgb_param, xgtrain, num_boost_round=alg.get_params()['n_estimators'], nfold=cv_folds,
                          metrics='auc', early_stopping_rounds=early_stopping_rounds, show_stdv=False)
        alg.set_params(n_estimators=cvresult.shape[0])

    # Fit the algorithm on the data
    alg.fit(dtrain[predictors], dtrain['type'], eval_metric='auc')

    # Predict training set:
    dtrain_predictions = alg.predict(dtrain[predictors])
    dtrain_predprob = alg.predict_proba(dtrain[predictors])[:, 1]

    # Print model report:
    print "\nModel Report"
    print "Accuracy : %.4g" % metrics.accuracy_score(dtrain['type'].values, dtrain_predictions)
    print "AUC Score (Train): %f" % metrics.roc_auc_score(dtrain['type'], dtrain_predprob)

    # print alg.get_booster().get_fscore()
    feat_imp = pd.Series(alg.get_booster().get_fscore()).sort_values(ascending=False)

    feat_imp.plot(kind='bar', title='Feature Importances')
    plt.ylabel('Feature Importance Score')
    cvresult.plot()
    print cvresult.shape[0]
    plt.show()





if __name__ == '__main__':
    #Choose all predictors except target & IDcols
    predictors = [x for x in train.columns if x not in [target, IDcol]]
    xgb1 = XGBClassifier(
        learning_rate =0.1,
        n_estimators=15,
        max_depth=5,
        min_child_weight=1,
        gamma=0,
        subsample=0.8,
        colsample_bytree=0.8,
        objective= 'binary:logistic',
        nthread=4,
        scale_pos_weight=1,
        seed=27)
    # modelfit(xgb1, train, predictors)

    #
    param_test1 = {
     'max_depth':range(3,10,2),
     'min_child_weight':range(1,6,2)
    }
    gsearch1 = GridSearchCV(estimator = XGBClassifier( learning_rate =0.1, n_estimators=100, max_depth=5,
     min_child_weight=1, gamma=0, subsample=0.8, colsample_bytree=0.8,
     objective= 'binary:logistic', nthread=4, scale_pos_weight=1, seed=27),
     param_grid = param_test1, scoring='roc_auc',n_jobs=4,iid=False, cv=5)
    gsearch1.fit(train[predictors],train[target])
    print gsearch1.grid_scores_, gsearch1.best_params_, gsearch1.best_score_
    #
    param_test2 = {
        'max_depth': [2, 3, 4],
        'min_child_weight': [4, 5, 6]
    }
    gsearch2 = GridSearchCV(estimator=XGBClassifier(learning_rate=0.1, n_estimators=100, max_depth=3,
                                                    min_child_weight=5, gamma=0, subsample=0.8, colsample_bytree=0.8,
                                                    objective='binary:logistic', nthread=4, scale_pos_weight=1,
                                                    seed=27),
                            param_grid=param_test2, scoring='roc_auc', n_jobs=4, iid=False, cv=5)
    gsearch2.fit(train[predictors], train[target])
    print gsearch2.grid_scores_, gsearch2.best_params_, gsearch2.best_score_
    #
    param_test2b = {
        'min_child_weight': [3,4]
    }
    gsearch2b = GridSearchCV(estimator=XGBClassifier(learning_rate=0.1, n_estimators=100, max_depth=2,
                                                     min_child_weight=4, gamma=0, subsample=0.8, colsample_bytree=0.8,
                                                     objective='binary:logistic', nthread=4, scale_pos_weight=1,
                                                     seed=27),
                             param_grid=param_test2b, scoring='roc_auc', n_jobs=4, iid=False, cv=5)
    gsearch2b.fit(train[predictors], train[target])

    # modelfit(gsearch2b.best_estimator_, train, predictors)
    print gsearch2b.grid_scores_, gsearch2b.best_params_, gsearch2b.best_score_
    #
    param_test3 = {
        'gamma': [i / 10.0 for i in range(0, 5)]
    }
    gsearch3 = GridSearchCV(estimator=XGBClassifier(learning_rate=0.1, n_estimators=100, max_depth=2,
                                                    min_child_weight=4, gamma=0, subsample=0.8, colsample_bytree=0.8,
                                                    objective='binary:logistic', nthread=4, scale_pos_weight=1,
                                                    seed=27),
                            param_grid=param_test3, scoring='roc_auc', n_jobs=4, iid=False, cv=5)
    gsearch3.fit(train[predictors], train[target])
    print gsearch3.grid_scores_, gsearch3.best_params_, gsearch3.best_score_
    #
    # xgb2 = XGBClassifier(
    #     learning_rate=0.1,
    #     n_estimators=29,
    #     max_depth=4,
    #     min_child_weight=2,
    #     gamma=0,
    #     subsample=0.8,
    #     colsample_bytree=0.8,
    #     objective='binary:logistic',
    #     nthread=4,
    #     scale_pos_weight=1,
    #     seed=27)
    # modelfit(xgb2, train, predictors)
    #
    param_test4 = {
        'subsample': [i / 10.0 for i in range(6, 10)],
        'colsample_bytree': [i / 10.0 for i in range(6, 10)]
    }
    gsearch4 = GridSearchCV(estimator=XGBClassifier(learning_rate=0.1, n_estimators=100, max_depth=2,
                                                    min_child_weight=4, gamma=0, subsample=0.8, colsample_bytree=0.6,
                                                    objective='binary:logistic', nthread=4, scale_pos_weight=1,
                                                    seed=27),
                            param_grid=param_test4, scoring='roc_auc', n_jobs=4, iid=False, cv=5)
    gsearch4.fit(train[predictors], train[target])
    print gsearch4.grid_scores_, gsearch4.best_params_, gsearch4.best_score_

    param_test5 = {
        'subsample': [i / 100.0 for i in range(75, 90, 5)],
        'colsample_bytree': [i / 100.0 for i in range(75, 90, 5)]
    }
    gsearch5 = GridSearchCV(estimator=XGBClassifier(learning_rate=0.1, n_estimators=100, max_depth=2,
                                                    min_child_weight=4, gamma=0, subsample=0.8, colsample_bytree=0.6,
                                                    objective='binary:logistic', nthread=4, scale_pos_weight=1,
                                                    seed=27),
                            param_grid=param_test5, scoring='roc_auc', n_jobs=4, iid=False, cv=5)
    gsearch5.fit(train[predictors], train[target])
    print gsearch5.grid_scores_, gsearch5.best_params_, gsearch5.best_score_
    #
    param_test6 = {
        'reg_alpha': [1e-5, 1e-2, 0.1, 1, 100]
    }
    gsearch6 = GridSearchCV(estimator=XGBClassifier(learning_rate=0.1, n_estimators=100, max_depth=2,
                                                    min_child_weight=4, gamma=0, subsample=0.8, colsample_bytree=0.75,
                                                    objective='binary:logistic', nthread=4, scale_pos_weight=1,
                                                    seed=27),
                            param_grid=param_test6, scoring='roc_auc', n_jobs=4, iid=False, cv=5)
    gsearch6.fit(train[predictors], train[target])
    print gsearch6.grid_scores_, gsearch6.best_params_, gsearch6.best_score_
    #
    param_test7 = {
        'reg_alpha': [0, 0.001, 0.005, 0.01, 0.05]
    }
    gsearch7 = GridSearchCV(estimator=XGBClassifier(learning_rate=0.1, n_estimators=29, max_depth=4,
                                                    min_child_weight=1, gamma=0, subsample=0.8, colsample_bytree=0.75,
                                                    objective='binary:logistic', nthread=4, scale_pos_weight=1,
                                                    seed=27),
                            param_grid=param_test7, scoring='roc_auc', n_jobs=4, iid=False, cv=5)
    gsearch7.fit(train[predictors], train[target])
    print gsearch7.grid_scores_, gsearch7.best_params_, gsearch7.best_score_
    #
    # xgb3 = XGBClassifier(
    #     learning_rate=0.1,
    #     n_estimators=1000,
    #     max_depth=4,
    #     min_child_weight=1,
    #     gamma=0,
    #     subsample=0.8,
    #     colsample_bytree=0.75,
    #     reg_alpha=0,
    #     objective='binary:logistic',
    #     nthread=4,
    #     scale_pos_weight=1,
    #     seed=27)
    # modelfit(xgb3, train, predictors)