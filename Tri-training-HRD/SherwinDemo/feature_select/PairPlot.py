#!/usr/bin/python
# coding=utf-8
import pandas as pd
import numpy as np
from sklearn.preprocessing import Imputer
from sklearn.preprocessing import StandardScaler
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler, RobustScaler
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import mglearn
from sklearn.decomposition import PCA
import os


os.chdir(os.path.abspath('..'))
os.chdir(os.path.abspath('..'))
path = os.getcwd()
data = pd.read_csv(path+"/AllData/labeled/NA12878_stander.csv")
data = data.drop(['CHROM','POS','PL'],1)
y_data = data['type']
x_data = data.drop(['type'], 1)
grr = pd.plotting.scatter_matrix(x_data,c=y_data,figsize=(15,15),marker='o',hist_kwds={'bins':20},
                        s=30,alpha=.8,cmap=mglearn.cm3)
plt.savefig(path+'/dealData/data_processing/NA12878_standers_scatter.jpg')
plt.show()