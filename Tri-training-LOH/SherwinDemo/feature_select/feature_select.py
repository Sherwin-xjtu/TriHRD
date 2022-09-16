#!/usr/bin/python
# coding=utf-8

import numpy as np
# from sklearn.preprocessing import Imputer
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
# data = pd.read_csv(path+"/AllData/labeled/NA12878_stander.csv")
data = pd.read_csv("F:/shenzhen/Sherwin/HRD/all_scaler.csv")
data = data.drop(['id'],1)
y_data = data['label']
x_data = data.drop(['label'], 1)
X_train = np.array(x_data)
Y_train = np.array(y_data)
name_list = ['nhet', 'cnlr.median', 'mafR', 'mafR.clust', 'start', 'end',
       'cf.em','tcn.em', 'lcn.em']
fig,axes = plt.subplots(5,2,figsize=(9,9))
fal = X_train[Y_train==0]
tru = X_train[Y_train==1]
ax = axes.ravel()
for i in range(10):
    _,bins = np.histogram(X_train[:,i],bins=50)
    ax[i].hist(fal[:,i],bins=bins,color=mglearn.cm3(0),alpha=.5)
    ax[i].hist(tru[:, i], bins=bins, color=mglearn.cm3(2), alpha=.5)
    ax[i].set_title(name_list[i])
    ax[i].set_yticks(())
# ax[0].set_xlabel("Feature false")
ax[0].set_ylabel("Frequence")
ax[0].legend(['false','true'],loc="best")
fig.tight_layout()
plt.savefig(path+'/dealData/data_processing/all_scaler.jpg')
plt.show()

pca = PCA(n_components=2)
pca.fit(X_train)
X_pca = pca.transform(X_train)


plt.figure(figsize=(8,8))
mglearn.discrete_scatter(X_pca[:,0],X_pca[:,1],Y_train)
plt.legend(['false','true'],loc="best")
plt.gca().set_aspect("equal")
plt.xlabel("First principal component")
plt.ylabel("Second principal component")
plt.show()