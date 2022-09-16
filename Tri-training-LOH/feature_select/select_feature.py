#!/usr/bin/python
# coding=utf-8
# from sklearn.datasets import fetch_20newsgroups
#
# # 从互联网上下载即时新闻样本，subset='all'下载近2万条文本存储在变量news中
# news = fetch_20newsgroups(subset='all')
# # 导入train_test_split模块用于分割训练集
# from sklearn.cross_validation import train_test_split
#
# X_train, X_test, y_train, y_test = train_test_split(news.data, news.target, test_size=0.25, random_state=33)

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVC
count_vec = CountVectorizer()
train = pd.read_csv('../AllData/labeled/trianing_50_data.csv')
x_train_columns = [x for x in train.columns if x not in ['type']]
X_train = train[x_train_columns]
y_train = train['type']

test = pd.read_csv('../AllData/labeled/test_data.csv')
x_test_columns = [x for x in test.columns if x not in ['type']]
X_test = test[x_test_columns]
y_test = test['type']

# 使用词频统计的方式将原始数据和测试文本转化为特征向量
X_count_train = count_vec.fit_transform(X_train)
X_count_test = count_vec.transform(X_test)
# 使用朴素贝叶斯分类器
from sklearn.naive_bayes import MultinomialNB

mnb = SVC(probability=True)
mnb.fit(X_count_train, y_train)
y_count_predict = mnb.predict(X_count_test)
# 输出更加详细的其他评价分类性能的指标
from sklearn.metrics import classification_report
target = ['class 0','class 1']
print('The accuracy of classifying using CountVectorizer is:', mnb.score(X_count_test, y_test))
print(classification_report(y_test, y_count_predict, target_names=target))

from sklearn.feature_extraction.text import TfidfVectorizer

tf_vec = TfidfVectorizer()
# 使用词频统计的方式将原始数据和测试文本转化为特征向量
X_tf_train = tf_vec.fit_transform(X_train)
X_tf_test = tf_vec.transform(X_test)
# 使用朴素贝叶斯分类器
# from sklearn.naive_bayes import MultinomialNB

mnb = SVC(probability=True)
mnb.fit(X_tf_train, y_train)
y_tf_predict = mnb.predict(X_tf_test)
# 输出更加详细的其他评价分类性能的指标
from sklearn.metrics import classification_report

print('The accuracy of classifying using TfidfVectorizer is:', mnb.score(X_tf_test, y_test))
print(classification_report(y_test, y_tf_predict, target_names=target))
