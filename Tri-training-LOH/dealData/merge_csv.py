#!/usr/bin/python
# coding=utf-8
import pandas as pd
import numpy as np
from sklearn.preprocessing import Imputer
from sklearn.preprocessing import StandardScaler
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler, RobustScaler

labeled = pd.read_csv('C:/Users/Sherwin/Desktop/test2_3.csv')

res=labeled

res.iloc[:, 5:-1] = Imputer().fit_transform(res.iloc[:, 5:-1])
res.iloc[:, 5:-1] = res.iloc[:, 5:-1].astype(np.float64)
res.to_csv('C:/Users/Sherwin/Desktop/test2_3_.csv',index = False)




# res.iloc[:, 2:-1] = preprocessing.scale(res.iloc[:, 2:-1])
#
# min_max_scaler = preprocessing.MinMaxScaler()
# res.iloc[:, 2:-1] = min_max_scaler.fit_transform(res.iloc[:, 2:-1])


# res.to_csv('../dealData/data_processing/all_r.csv',index = False)
