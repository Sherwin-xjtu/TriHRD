#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : soccer_value.py
# @Author: Huangqinjian
# @Date  : 2018/3/22
# @Desc  :

import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn import preprocessing
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.preprocessing import Imputer
from sklearn.grid_search import GridSearchCV
from hyperopt import hp
from xgboost.sklearn import XGBClassifier
# 加载训练数据
def featureSet(data):
    imputer = Imputer(missing_values='NaN', strategy='mean', axis=0)
    imputer.fit(data.loc[:, ['rw', 'st', 'lw', 'cf', 'cam', 'cm']])
    x_new = imputer.transform(data.loc[:, ['rw', 'st', 'lw', 'cf', 'cam', 'cm']])

    le = preprocessing.LabelEncoder()
    le.fit(['Low', 'Medium', 'High'])
    att_label = le.transform(data.work_rate_att.values)
    # print(att_label)
    def_label = le.transform(data.work_rate_def.values)
    # print(def_label)

    data_num = len(data)
    XList = []
    for row in range(0, data_num):
        tmp_list = []
        tmp_list.append(data.iloc[row]['club'])
        tmp_list.append(data.iloc[row]['league'])
        tmp_list.append(data.iloc[row]['potential'])
        tmp_list.append(data.iloc[row]['international_reputation'])
        tmp_list.append(data.iloc[row]['pac'])
        tmp_list.append(data.iloc[row]['sho'])
        tmp_list.append(data.iloc[row]['pas'])
        tmp_list.append(data.iloc[row]['dri'])
        tmp_list.append(data.iloc[row]['def'])
        tmp_list.append(data.iloc[row]['phy'])
        tmp_list.append(data.iloc[row]['skill_moves'])
        tmp_list.append(x_new[row][0])
        tmp_list.append(x_new[row][1])
        tmp_list.append(x_new[row][2])
        tmp_list.append(x_new[row][3])
        tmp_list.append(x_new[row][4])
        tmp_list.append(x_new[row][5])
        tmp_list.append(att_label[row])
        tmp_list.append(def_label[row])
        XList.append(tmp_list)
    yList = data.y.values
    return XList, yList

# 加载测试数据
def loadTestData(filePath):
    data = pd.read_csv(filepath_or_buffer=filePath)
    imputer = Imputer(missing_values='NaN', strategy='mean', axis=0)
    imputer.fit(data.loc[:, ['rw', 'st', 'lw', 'cf', 'cam', 'cm']])
    x_new = imputer.transform(data.loc[:, ['rw', 'st', 'lw', 'cf', 'cam', 'cm']])

    le = preprocessing.LabelEncoder()
    le.fit(['Low', 'Medium', 'High'])
    att_label = le.transform(data.work_rate_att.values)
    # print(att_label)
    def_label = le.transform(data.work_rate_def.values)
    # print(def_label)

    data_num = len(data)
    XList = []
    for row in range(0, data_num):
        tmp_list = []
        tmp_list.append(data.iloc[row]['club'])
        tmp_list.append(data.iloc[row]['league'])
        tmp_list.append(data.iloc[row]['potential'])
        tmp_list.append(data.iloc[row]['international_reputation'])
        tmp_list.append(data.iloc[row]['pac'])
        tmp_list.append(data.iloc[row]['sho'])
        tmp_list.append(data.iloc[row]['pas'])
        tmp_list.append(data.iloc[row]['dri'])
        tmp_list.append(data.iloc[row]['def'])
        tmp_list.append(data.iloc[row]['phy'])
        tmp_list.append(data.iloc[row]['skill_moves'])
        tmp_list.append(x_new[row][0])
        tmp_list.append(x_new[row][1])
        tmp_list.append(x_new[row][2])
        tmp_list.append(x_new[row][3])
        tmp_list.append(x_new[row][4])
        tmp_list.append(x_new[row][5])
        tmp_list.append(att_label[row])
        tmp_list.append(def_label[row])
        XList.append(tmp_list)
    return XList


def trainandTest(X_train, y_train, X_test):
    # XGBoost训练过程
    model = xgb.XGBRegressor(learning_rate=0.1, n_estimators=550, max_depth=4, min_child_weight=5, seed=0,
                             subsample=0.7, colsample_bytree=0.7, gamma=0.1, reg_alpha=1, reg_lambda=1)
    model.fit(X_train, y_train)

    # 对测试集进行预测
    ans = model.predict(X_test)

    ans_len = len(ans)
    id_list = np.arange(10441, 17441)
    data_arr = []
    for row in range(0, ans_len):
        data_arr.append([int(id_list[row]), ans[row]])
    np_data = np.array(data_arr)

    # 写入文件
    pd_data = pd.DataFrame(np_data, columns=['id', 'y'])
    # print(pd_data)
    pd_data.to_csv('submit.csv', index=None)

    # 显示重要特征
    # plot_importance(model)
    # plt.show()


def cv_results(xgb1,dtrain):
    params = xgb1.get_xgb_params()
    xgtrain = xgb.DMatrix(dtrain[predictors].values, label=dtrain[target].values)
    cvresult = xgb.cv(params, xgtrain, num_boost_round=100, early_stopping_rounds=20,
                       verbose_eval=50, show_stdv=False)

    # cvresult[['train-rmse-mean','test-rmse-mean']].plot()
    # plt.figure()
    # cvresult.plot()
    # plt.title('XGBoost Feature Importance')
    # plt.xlabel('relative importance')
    # plt.show()

    xgb1.set_params(n_estimators=cvresult.shape[0])
    # Fit the algorithm on the data
    xgb1.fit(dtrain[predictors], dtrain['type'], eval_metric='auc')

    # Predict training set:
    dtrain_predictions = xgb1.predict(dtrain[predictors])
    dtrain_predprob = xgb1.predict_proba(dtrain[predictors])[:, 1]

    # Print model report:
    print "\nModel Report"
    print "Accuracy : %.4g" % metrics.accuracy_score(dtrain['type'].values, dtrain_predictions)
    print "AUC Score (Train): %f" % metrics.roc_auc_score(dtrain['type'], dtrain_predprob)

    # print alg.get_booster().get_fscore()
    feat_imp = pd.Series(xgb1.get_booster().get_fscore()).sort_values(ascending=False)

    feat_imp.plot(kind='bar', title='Feature Importances')
    plt.ylabel('Feature Importance Score')
    cvresult.plot()
    print cvresult.shape[0]
    plt.show()








if __name__ == '__main__':
    target = 'type'
    IDcol = 'ID'
    trainFilePath = '../dealData/data/Test_L__072302_t_scale.csv'
    # testFilePath = 'dataset/soccer/test.csv'
    train = pd.read_csv(trainFilePath)
    xgb1 = XGBClassifier(
        learning_rate=0.1,
        n_estimators=15,
        max_depth=5,
        min_child_weight=1,
        gamma=0,
        subsample=0.8,
        colsample_bytree=0.8,
        objective='binary:logistic',
        nthread=4,
        scale_pos_weight=1,
        seed=27)
    predictors = [x for x in train.columns if x not in [target, IDcol]]
    y = train['type']
    # print type(y)
    X = train.drop(['type'], 1)
    dtrain = xgb.DMatrix(X, label=y)
    cv_results(xgb1, train)

    # X_train, y_train = featureSet(data)
    # X_test = loadTestData(testFilePath)
    # 预测最终的结果
    # trainandTest(X_train, y_train, X_test)

    cv_params = {'n_estimators': [400, 500, 600, 700, 800]}
    other_params = {'learning_rate': 0.1, 'n_estimators': 500, 'max_depth': 5, 'min_child_weight': 1, 'seed':100,
                    'subsample': 0.8, 'colsample_bytree': 0.8, 'gamma': 0, 'reg_alpha': 0, 'reg_lambda': 1}

    # cv_params = {'max_depth': [3, 4, 5, 6, 7, 8, 9, 10], 'min_child_weight': [1, 2, 3, 4, 5, 6]}
    # other_params = {'learning_rate': 0.1, 'n_estimators': 600, 'max_depth': 5, 'min_child_weight': 1, 'seed': 0,
    #                 'subsample': 0.8, 'colsample_bytree': 0.8, 'gamma': 0, 'reg_alpha': 0, 'reg_lambda': 1}

    # cv_params = {'gamma': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]}
    # other_params = {'learning_rate': 0.1, 'n_estimators': 600, 'max_depth': 3, 'min_child_weight': 5, 'seed': 0,
    #                 'subsample': 0.8, 'colsample_bytree': 0.8, 'gamma': 0, 'reg_alpha': 0, 'reg_lambda': 1}

    # cv_params = {'subsample': [0.6, 0.7, 0.8, 0.9], 'colsample_bytree': [0.6, 0.7, 0.8, 0.9]}
    # other_params = {'learning_rate': 0.1, 'n_estimators': 600, 'max_depth': 3, 'min_child_weight': 5, 'seed': 0,
    #                 'subsample': 0.8, 'colsample_bytree': 0.8, 'gamma': 0.1, 'reg_alpha': 0, 'reg_lambda': 1}

    # cv_params = {'reg_alpha': [0.05, 0.1, 1, 2, 3], 'reg_lambda': [0.05, 0.1, 1, 2, 3]}
    # other_params = {'learning_rate': 0.1, 'n_estimators': 600, 'max_depth': 3, 'min_child_weight': 5, 'seed': 0,
    #                 'subsample': 0.8, 'colsample_bytree': 0.6, 'gamma': 0.1, 'reg_alpha': 0, 'reg_lambda': 1}

    # cv_params = {'learning_rate': [0.01, 0.05, 0.07, 0.1, 0.2]}
    # other_params = {'learning_rate': 0.1, 'n_estimators': 600, 'max_depth': 3, 'min_child_weight': 5, 'seed': 0,
    #                 'subsample': 0.8, 'colsample_bytree': 0.6, 'gamma': 0.1, 'reg_alpha': 0.05, 'reg_lambda': 1}

    model = xgb.XGBRegressor(**other_params)
    optimized_GBM = GridSearchCV(estimator=model, param_grid=cv_params, scoring='r2', cv=5, verbose=1, n_jobs=4)
    optimized_GBM.fit(train[predictors], train[target])
    evalute_result = optimized_GBM.grid_scores_
    print('每轮迭代运行结果:{0}'.format(evalute_result))
    print('参数的最佳取值：{0}'.format(optimized_GBM.best_params_))
    print('最佳模型得分:{0}'.format(optimized_GBM.best_score_))




    """
    下面部分为调试参数的代码
    """

    #
    # cv_params = {'n_estimators': [400, 500, 600, 700, 800]}
    # other_params = {'learning_rate': 0.1, 'n_estimators': 500, 'max_depth': 5, 'min_child_weight': 1, 'seed': 0,
    #                 'subsample': 0.8, 'colsample_bytree': 0.8, 'gamma': 0, 'reg_alpha': 0, 'reg_lambda': 1}
    #
    # cv_params = {'n_estimators': [550, 575, 600, 650, 675]}
    # other_params = {'learning_rate': 0.1, 'n_estimators': 600, 'max_depth': 5, 'min_child_weight': 1, 'seed': 0,
    #                 'subsample': 0.8, 'colsample_bytree': 0.8, 'gamma': 0, 'reg_alpha': 0, 'reg_lambda': 1}
    #
    # cv_params = {'max_depth': [3, 4, 5, 6, 7, 8, 9, 10], 'min_child_weight': [1, 2, 3, 4, 5, 6]}
    # other_params = {'learning_rate': 0.1, 'n_estimators': 550, 'max_depth': 5, 'min_child_weight': 1, 'seed': 0,
    #                 'subsample': 0.8, 'colsample_bytree': 0.8, 'gamma': 0, 'reg_alpha': 0, 'reg_lambda': 1}
    #
    # cv_params = {'gamma': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]}
    # other_params = {'learning_rate': 0.1, 'n_estimators': 550, 'max_depth': 4, 'min_child_weight': 5, 'seed': 0,
    #                 'subsample': 0.8, 'colsample_bytree': 0.8, 'gamma': 0, 'reg_alpha': 0, 'reg_lambda': 1}
    #
    # cv_params = {'subsample': [0.6, 0.7, 0.8, 0.9], 'colsample_bytree': [0.6, 0.7, 0.8, 0.9]}
    # other_params = {'learning_rate': 0.1, 'n_estimators': 550, 'max_depth': 4, 'min_child_weight': 5, 'seed': 0,
    #                 'subsample': 0.8, 'colsample_bytree': 0.8, 'gamma': 0.1, 'reg_alpha': 0, 'reg_lambda': 1}
    #
    # cv_params = {'reg_alpha': [0.05, 0.1, 1, 2, 3], 'reg_lambda': [0.05, 0.1, 1, 2, 3]}
    # other_params = {'learning_rate': 0.1, 'n_estimators': 550, 'max_depth': 4, 'min_child_weight': 5, 'seed': 0,
    #                 'subsample': 0.7, 'colsample_bytree': 0.7, 'gamma': 0.1, 'reg_alpha': 0, 'reg_lambda': 1}
    #
    # cv_params = {'learning_rate': [0.01, 0.05, 0.07, 0.1, 0.2]}
    # other_params = {'learning_rate': 0.1, 'n_estimators': 550, 'max_depth': 4, 'min_child_weight': 5, 'seed': 0,
    #                 'subsample': 0.7, 'colsample_bytree': 0.7, 'gamma': 0.1, 'reg_alpha': 1, 'reg_lambda': 1}
    #
    # model = xgb.XGBRegressor(**other_params)
    # optimized_GBM = GridSearchCV(estimator=model, param_grid=cv_params, scoring='r2', cv=5, verbose=1, n_jobs=4)
    # optimized_GBM.fit(X_train, y_train)
    # evalute_result = optimized_GBM.grid_scores_
    # print('每轮迭代运行结果:{0}'.format(evalute_result))
    # print('参数的最佳取值：{0}'.format(optimized_GBM.best_params_))
    # print('最佳模型得分:{0}'.format(optimized_GBM.best_score_))
