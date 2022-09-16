#!/usr/bin/python
# coding=utf-8
from sklearn import metrics
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVC
count_vec = CountVectorizer()
train = pd.read_csv('../AllData/labeled/test_data.csv')
x_train_columns = [x for x in train.columns if x not in ['type']]
X_train = train[x_train_columns]
y_train = train['type']
test = pd.read_csv('../dealData/data_processing/chr21_all_labeled.csv')
x_test_columns = [x for x in test.columns if x not in ['type','CHROM','POS']]
X_test = test[x_test_columns]
y_test = test['type']
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import RandomForestClassifier
model = ExtraTreesClassifier()
model.fit(X_test, y_test)
# display the relative importance of each attribute
print(model.feature_importances_)

from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
model = RandomForestClassifier()
# create the RFE model and select 3 attributes
rfe = RFE(model, 6)
rfe = rfe.fit(X_test, y_test)
# summarize the selection of the attributes
print(rfe.support_)
print(rfe.ranking_)