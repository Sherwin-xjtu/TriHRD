#!/usr/bin/python
# coding=utf-8
import pandas as pd
import numpy as np
from sklearn.preprocessing import Imputer

from sklearn.preprocessing import StandardScaler
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler, RobustScaler
# label_1 = pd.read_csv('./2015_data/label_1.csv')
# label_0 = pd.read_csv('./2015_data/label_0.csv')
# label = pd.concat([label_0,label_1])
# print(label)
# label.to_csv('./2015_data/label.csv',index = False)


unlabeled = pd.read_csv('C:/Users/Sherwin/Desktop/output/NA12878-GATK3-chr21/fp.csv')
labeled = pd.read_csv('C:/Users/Sherwin/Desktop/output/NA12878-GATK3-chr21/tp.csv')

tp = labeled.drop(['SOR'],1)
fp = unlabeled.drop(['SOR'],1)
res=pd.concat([tp,fp],axis=0)

res.iloc[:, 2:-2] = Imputer().fit_transform(res.iloc[:, 2:-2])
res.iloc[:, 2:-2] = res.iloc[:, 2:-2].astype(np.float64)
# train.iloc[:, 3:-2] = preprocessing.normalize(train.iloc[:, 3:-2])
res.iloc[:, 2:-2] = preprocessing.scale(res.iloc[:, 2:-2])

min_max_scaler = preprocessing.MinMaxScaler()
res.iloc[:, 2:-2] = min_max_scaler.fit_transform(res.iloc[:, 2:-2])
print res.iloc[:, 2:-1]
res.to_csv('C:/Users/Sherwin/Desktop/output/NA12878-GATK3-chr21/NA12878-GATK3-chr21.csv',index = False)
