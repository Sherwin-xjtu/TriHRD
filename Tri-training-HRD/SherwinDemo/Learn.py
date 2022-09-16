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

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model.logistic import LogisticRegression
from sklearn.model_selection import train_test_split



class Learn:

	def __init__(self):
		pass
	"""SVM算法"""
	"""SVM调参"""
	# def svm_cross_validation(train_x, train_y):
	# 	from sklearn.model_selection import GridSearchCV
	# 	from sklearn.svm import SVC
	# 	model = SVC(kernel='rbf', probability=True)
	# 	param_grid = {'C': [1e-3, 1e-2, 1e-1, 1, 10, 100, 1000], 'gamma': [0.001, 0.0001]}
	# 	grid_search = GridSearchCV(model, param_grid, n_jobs=8, verbose=1)
	# 	grid_search.fit(train_x, train_y)
	# 	best_parameters = grid_search.best_estimator_.get_params()
	# 	for para, val in list(best_parameters.items()):
	# 		print(para, val)
	# 	model = SVC(kernel='rbf', C=best_parameters['C'], gamma=best_parameters['gamma'], probability=True)
	# 	model.fit(train_x, train_y)
	# 	return model

	def SVM(self,S):
		train = S
		y = train['type']
		x = train.drop(['type'],1)
		x_train = x.values
		y_train = y.values

		from sklearn.model_selection import GridSearchCV
		from sklearn.svm import SVC
		clf = SVC(kernel='rbf', probability=True)
		param_grid = {'C': [1e-5,1e-4,1e-3, 1e-2, 1e-1, 1, 10, 100, 500,550,1000], 'gamma': [10,1,0.1,0.01,0.001, 0.0001]}
		grid_search = GridSearchCV(clf, param_grid, n_jobs=8, verbose=1)
		grid_search.fit(x_train, y_train)
		best_parameters = grid_search.best_estimator_.get_params()
		# for para, val in list(best_parameters.items()):
		# 	print(para, val)
		# print best_parameters
		# clf = SVC(kernel='rbf', C=best_parameters['C'], gamma=best_parameters['gamma'], probability=True)
		# print best_parameters['C'], best_parameters['gamma']
		clf = AdaBoostClassifier(SVC(kernel='rbf', C=best_parameters['C'], gamma=best_parameters['gamma'], probability=True),
								 algorithm="SAMME",n_estimators=200, learning_rate=0.8)

		clf.fit(x_train, y_train)

		# clt = svm.SVC(C=821,kernel='rbf',gamma=0.001,decision_function_shape='ovr')
		# clt.fit(x_train,y_train.ravel())
		return clf



	# def SVM(self,S):
	# 	train = S
	# 	y = train['type']
	# 	x = train.drop(['type'],1)
	# 	x_train = x.values
	# 	y_train = y.values
	# 	clt = svm.SVC(C=821,kernel='rbf',gamma=0.001,decision_function_shape='ovr')
	# 	clt.fit(x_train,y_train.ravel())
	# 	return clt



	""" 朴素贝叶斯算法 """
	def Naive_Bayes(self,S):
		train = S
		y = train['type']
		x = train.drop(['type'],1)
		x_train = x.values
		y_train = y.values.ravel()
		gnb = GaussianNB()
		clt = gnb.fit(x_train, y_train)
		return clt 
	""" 决策树算法 """
	def Tree(self,S):
		train = S
		y = train['type']
		x = train.drop(['type'],1)
		x_train = x.values
		y_train = y.values.ravel()
		# clf = tree.DecisionTreeClassifier(max_depth=306,max_features = 2)
		clf = AdaBoostClassifier(tree.DecisionTreeClassifier(
			max_depth=2, min_samples_split=20,
			min_samples_leaf=5), algorithm="SAMME",
			n_estimators=200, learning_rate=0.8)
		clf = clf.fit(x_train, y_train)
		return clf

	""" 随机森林算法 """
	def Random_Forest(self,S):
		train = S
		y = train['type']
		x = train.drop(['type'],1)
		x_train = x.values
		y_train = y.values.ravel()
		# kwargs = {"n_jobs": 8,
		# 		  "max_depth": 12,
		# 		  "min_samples_leaf": 50,
		# 		  "n_estimators": 50,
		# 		  "max_features": None,
		# 		  "verbose": 10,
		# 		  }
		# clf = RandomForestClassifier(**kwargs)
		clf = RandomForestClassifier()
		# clf = AdaBoostClassifier(
		# 	RandomForestClassifier(),
		# 	algorithm="SAMME",
		# 	n_estimators=200, learning_rate=0.8)
		# clf = clf.fit(x_train,y_train, allrows["weight"].values)
		clf = clf.fit(x_train, y_train)
		return clf

	""" 逻辑回归算法 """
	def Logistic_Regression(self, S):
		train = S
		y = train['type']
		x = train.drop(['type'], 1)
		x_train = x.values
		y_train = y.values.ravel()
		# 我们建一个TfidfVectorizer实例来计算TF-IDF权重：
		# vectorizer = TfidfVectorizer()
		# X_train = vectorizer.fit_transform(X_train_raw)
		# X_test = vectorizer.transform(X_test_raw)
		# LogisticRegression同样实现了fit()和predict()方法

		clf = AdaBoostClassifier(
			LogisticRegression(),
			algorithm="SAMME",
			n_estimators=200, learning_rate=0.8)
		# clf = LogisticRegression()
		clf = clf.fit(x_train, y_train)
		return clf

	""" 准确率评估 """
	def Estimate(self,T,M):
		y = T['type']
		x = T.drop(['type'],1)
		x_test = x.values
		y_test = y.values	
		score = M.score(x_test,y_test)
		return score	
	""" 返回模型 """
	def genModel(self,i,L):
		switch = {
			0 : self.SVM(L),
			1 : self.Tree(L),
			2 : self.Random_Forest(L)
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
		M.append(learn.genModel(i,L))
	bagging = Bagging(M)
	print T
	y_pre = bagging.predict(T)
	print(y_pre)
	






