# -*- coding: utf-8 -*-
import pandas as pd
from sklearn import svm
from sklearn.naive_bayes import GaussianNB
from sklearn import tree
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model.logistic import LogisticRegression
from sklearn.model_selection import train_test_split

#设置待选的参数
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import StratifiedKFold
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import classification_report


def Tree(S):
    train = S
    y = train['type']
    x = train.drop(['type'], 1)
    x_train = x.values
    y_train = y.values.ravel()
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(x_train, y_train)
    return clf


def SVM(S):
    train = S
    y = train['type']
    x = train.drop(['type'], 1)
    x_train = x.values
    y_train = y.values
    from sklearn.model_selection import GridSearchCV
    from sklearn.svm import SVC
    clf = SVC(kernel='rbf', probability=True)
    param_grid = {'C': [1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1, 10, 100, 500, 550, 1000],
                  'gamma': [10, 1, 0.1, 0.01, 0.001, 0.0001]}
    grid_search = GridSearchCV(clf, param_grid, n_jobs=8, verbose=1)
    grid_search.fit(x_train, y_train)
    best_parameters = grid_search.best_estimator_.get_params()
    clf = AdaBoostClassifier(
        SVC(kernel='rbf', C=best_parameters['C'], gamma=best_parameters['gamma'], probability=True), algorithm="SAMME",
        n_estimators=200, learning_rate=0.8)
    clf.fit(x_train, y_train)
    return clf

def bagging_report(M, T):
    y_true = T['type']
    target = ['class 0', 'class 1']
    x = T.drop(['type'], 1)
    x_train = x.values
    y_pred = M.predict(x_train)
    # print y_true
    report = classification_report(y_true, y_pred, target_names=target)
    print("三个分类器集成后的性能报告：\n {0}".format(report))

if __name__ == '__main__':
    train = pd.read_csv("new_data.csv")
    # y = train['type']
    # x = train.drop(['type'], 1)
    # x_train = x.values
    # y_train = y.values.ravel()
    clf = SVM(train)
    test = pd.read_csv("../AllData/labeled/new_data.csv")
    bagging_report(clf,test)

# decision_tree_classifier = DecisionTreeClassifier()
# parameter_grid = {'max_depth':range(1,1000),
#                   'max_features':range(1,6)}
#
# skf = StratifiedKFold(n_splits=2)
# cross_validation = skf.get_n_splits(x_train,y_train)
#
# #将不同参数带入
# gridsearch = GridSearchCV(decision_tree_classifier,
#                           parameter_grid,
#                           cv = cross_validation)
# gridsearch.fit(x_train,y_train)
# print gridsearch.best_params_, gridsearch.best_score_
# #得分最高的参数值，并构建最佳的决策树
# best_param = gridsearch.best_params_
#
# best_decision_tree_classifier = DecisionTreeClassifier(max_depth=best_param['max_depth'],
#                                                    max_features=best_param['max_features'])