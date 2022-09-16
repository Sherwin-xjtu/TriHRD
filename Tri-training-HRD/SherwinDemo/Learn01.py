#!/usr/bin/python
# coding=utf-8
from sklearn import svm
from sklearn.naive_bayes import GaussianNB
from sklearn import tree
# import xgboost as xgb
import numpy as np
from system.Tri_training01.bootstrapSample import Sample
from system.Setting.config import Config
from system.Tri_training01.process import Process
from system.Tri_training01.Bagging import Bagging
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn import neighbors
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model.logistic import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV, KFold, train_test_split
from sklearn.metrics import make_scorer, accuracy_score
from sklearn.ensemble import VotingClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
from sklearn import mixture


class Learn:

    def __init__(self):
        pass

    """SVM算法"""

    def SVM(self, S):
        train = S
        y = train['type']
        x = train.drop(['type'], 1)
        x_train = x.values
        y_train = y.values


        svm_regressor = SVC(kernel='rbf', probability=True)
        param_grid = {'C': [1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1, 10, 100, 500, 550, 1000],
                      'gamma': [10, 1, 0.1, 0.01, 0.001, 0.0001]}
        grid_search = GridSearchCV(svm_regressor, param_grid, n_jobs=8, verbose=1)
        grid_search.fit(x_train, y_train)
        best_parameters = grid_search.best_estimator_.get_params()
        ada_regressor = AdaBoostClassifier(
            SVC(kernel='rbf', C=best_parameters['C'], gamma=best_parameters['gamma'], probability=True),
            algorithm="SAMME")
        ada_param_grid = {'n_estimators': range(10, 410, 10),
                          'learning_rate': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]}
        ada_grid_search = GridSearchCV(ada_regressor, ada_param_grid, n_jobs=8, verbose=1)
        ada_grid_search.fit(x_train, y_train)
        ada_best_parameters = ada_grid_search.best_estimator_.get_params()
        print ada_best_parameters
        clf = AdaBoostClassifier(
            SVC(kernel='rbf', C=best_parameters['C'], gamma=best_parameters['gamma'], probability=True),
            algorithm="SAMME", n_estimators=ada_best_parameters['n_estimators'],
            learning_rate=ada_best_parameters['learning_rate'])
        clf.fit(x_train, y_train)
        return clf

    """ 朴素贝叶斯算法 """

    def Naive_Bayes(self, S):
        train = S
        y = train['type']
        x = train.drop(['type'], 1)
        x_train = x.values
        y_train = y.values.ravel()
        gnb = GaussianNB()
        clf = AdaBoostClassifier(gnb, algorithm="SAMME",
                                 n_estimators=200, learning_rate=0.8)
        clf = clf.fit(x_train, y_train)
        return clf

    """ KNN算法 """

    def KNeighbors(self, S):
        train = S
        y = train['type']
        x = train.drop(['type'], 1)
        x_train = x.values
        y_train = y.values.ravel()
        nbrs_clf = neighbors.KNeighborsClassifier()
        clf = nbrs_clf.fit(x_train, y_train)
        return clf

    """ 决策树算法 """

    def Tree(self, S):
        train = S
        y = train['type']
        x = train.drop(['type'], 1)
        x_train = x.values
        y_train = y.values.ravel()
        regressor = tree.DecisionTreeClassifier(random_state=0)
        parameters = {'max_depth': range(1, 6), 'min_samples_split': range(2, 30),
                      'min_samples_leaf': range(1, 10)}
        scoring_fnc = make_scorer(accuracy_score)
        kfold = KFold(n_splits=10)
        grid = GridSearchCV(regressor, parameters, scoring_fnc, cv=kfold)
        grid = grid.fit(x_train, y_train)
        reg = grid.best_estimator_
        best_parameters = grid.best_estimator_.get_params()

        ada_regressor = AdaBoostClassifier(
            tree.DecisionTreeClassifier(
                max_depth=best_parameters['max_depth'], min_samples_split=best_parameters['min_samples_split'],
                min_samples_leaf=best_parameters['min_samples_leaf']),
            algorithm="SAMME")
        ada_param_grid = {'n_estimators': range(10, 410, 10),
                          'learning_rate': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]}
        ada_grid_search = GridSearchCV(ada_regressor, ada_param_grid, n_jobs=8, verbose=1)
        ada_grid_search.fit(x_train, y_train)
        ada_best_parameters = ada_grid_search.best_estimator_.get_params()
        # print ada_best_parameters
        clf = AdaBoostClassifier(
            tree.DecisionTreeClassifier(
                max_depth=best_parameters['max_depth'], min_samples_split=best_parameters['min_samples_split'],
                min_samples_leaf=best_parameters['min_samples_leaf']),
            algorithm="SAMME", n_estimators=ada_best_parameters['n_estimators'],
            learning_rate=ada_best_parameters['learning_rate'])
        clf = clf.fit(x_train, y_train)
        return clf

    """ 随机森林算法 """

    def Random_Forest(self, S):
        train = S
        y = train['type']
        x = train.drop(['type'], 1)
        x_train = x.values
        y_train = y.values.ravel()

        regressor = RandomForestClassifier()

        clf = regressor.fit(x_train, y_train)
        return clf

    """ 逻辑回归算法 """

    def Logistic_Regression(self, S):
        train = S
        y = train['type']
        x = train.drop(['type'], 1)
        x_train = x.values
        y_train = y.values.ravel()
        clf = LogisticRegression()
        clf = clf.fit(x_train, y_train)
        return clf

    """ 逻辑回归算法 """

    def voting_clf(self, S):
        train = S
        y = train['type']
        x = train.drop(['type'], 1)
        x_train = x.values
        y_train = y.values.ravel()
        voting_clf = VotingClassifier(estimators=[("lr", dt_clf), ("rf", rf_clf), ("svc", nb_clf)], voting="soft")
        clf = voting_clf.fit(x_train, y_train)
        return clf



    def test1(self,S):
        train = S
        y = train['type']
        x = train.drop(['type'], 1)
        x_train = x.values
        y_train = y.values.ravel()

        # 三个基学习器
        dt_clf = tree.DecisionTreeClassifier()
        rf_clf = RandomForestClassifier()
        svm_clf = SVC(probability=True)
        log_clf = LogisticRegression()
        nbrs_clf = neighbors.KNeighborsClassifier()
        nb_clf = GaussianNB()
        GMM_clf = mixture.GMM(n_components=2)

        # 投票分类器
        voting_clf = VotingClassifier(estimators=[("rf", dt_clf), ("svc", rf_clf), ("nc", nbrs_clf)], voting="soft")
        voting_clf.fit(x_train, y_train)
        return  voting_clf
        # for clf in (dt_clf, rf_clf, log_clf, nbrs_clf, svm_clf, nb_clf, nbrs_clf, GMM_clf, voting_clf):
        #     clf.fit(x_train, y_train)
        #     y_pred = clf.predict(X_test)
        #     print(clf.__class__.__name__, accuracy_score(y_test, y_pred))

    def test2(self, S):
        train = S
        y = train['type']
        x = train.drop(['type'], 1)
        x_train = x.values
        y_train = y.values.ravel()

        # 三个基学习器
        dt_clf = tree.DecisionTreeClassifier()
        rf_clf = RandomForestClassifier()
        svm_clf = SVC(probability=True)
        log_clf = LogisticRegression()
        nbrs_clf = neighbors.KNeighborsClassifier()
        nb_clf = GaussianNB()
        GMM_clf = mixture.GMM(n_components=2)

        # 投票分类器
        voting_clf = VotingClassifier(estimators=[("rf", dt_clf), ("svc", rf_clf), ("nc", svm_clf)], voting="soft")
        voting_clf.fit(x_train, y_train)
        return voting_clf

    def test3(self, S):
        train = S
        y = train['type']
        x = train.drop(['type'], 1)
        x_train = x.values
        y_train = y.values.ravel()

        # 三个基学习器
        dt_clf = tree.DecisionTreeClassifier()
        rf_clf = RandomForestClassifier()
        svm_clf = SVC(probability=True)
        log_clf = LogisticRegression()
        nbrs_clf = neighbors.KNeighborsClassifier()
        nb_clf = GaussianNB()
        GMM_clf = mixture.GMM(n_components=2)

        # 投票分类器
        voting_clf = VotingClassifier(estimators=[("rf", dt_clf), ("svc", log_clf), ("nc", GMM_clf)], voting="soft")
        voting_clf.fit(x_train, y_train)
        return voting_clf

    """ 准确率评估 """

    def Estimate(self, T, M):
        y = T['type']
        x = T.drop(['type'], 1)
        x_test = x.values
        y_test = y.values
        score = M.score(x_test, y_test)
        return score

    """ 返回模型 """

    def genModel(self, i, L):
        switch = {
            0: self.test1(L),
            1: self.test2(L),
            2: self.test3(L)
        }
        return switch.get(i)


if __name__ == '__main__':
    pro = Process()
    pro.read_labeled()
    L = pro.L
    T = pro.T
    learn = Learn()
    M = []
    for i in range(3):
        M.append(learn.genModel(i, L))
    bagging = Bagging(M)
    print T
    y_pre = bagging.predict(T)
    print(y_pre)







