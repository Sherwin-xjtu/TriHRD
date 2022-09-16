#!/usr/bin/python
# coding=utf-8
from __future__ import division  # 用于/相除的时候,保留真实结果.小数

import math

import pandas as pd
import numpy as np
import xgboost as xgb
import operator
import matplotlib.pyplot as plt
import sys
import os


# reload(sys)
# sys.setdefaultencoding('utf8')
# import sys
# reload(sys)
# sys.setdefaultencoding('gb18030')
#
from scipy.stats import chi2_contingency
from sklearn.model_selection import train_test_split


class RWCSV:
    def __init__(self):
        pass

    def pre_data(self,file_path):
        reader = pd.read_csv(file_path,sep='\t')
        true_data = reader[reader['type'] == 1]
        false_data_ = reader[reader['type'] == 0]
        true_data = true_data.sample(n=150, replace=False)
        false_data = false_data_.sample(n=140, replace=False)
        train_set = pd.concat([true_data, false_data], axis=0)
        unabled_set = reader.drop(train_set.index.values)
        xt, yt = self.X_Y(reader)
        # xt, yt = self.X_Y(train_set)
        # X_test1, y_test1 = self.X_Y(self.Ln)
        # X_train, X_tv, y_train, y_tv = train_test_split(X, y, test_size=0.70, random_state=2)
        X_train, X_validation, y_train, y_validation = train_test_split(xt, yt, test_size=0.3, random_state=1,stratify=yt)
        X_train['type'] = y_train
        train_set = X_train
        X_validation['type'] = y_validation
        unabled_set = pd.concat([X_validation, unabled_set], axis=0)
        return train_set,unabled_set

    def hrd_data(self,file_path):
        reader = pd.read_csv(file_path)
        LOH = reader[reader['type'] == 1]
        nonLOH = reader[reader['type'] == 0]
        numLOH = 0
        numNonLOH = 0
        lenLOH = 0
        lenNonLOH = 0
        ACMall = 0
        ATEall = 0
        ALEall = 0
        AHTall = 0

        for j, v in enumerate(LOH.values):
            numLOH = numLOH + v[-1]
            lenLOH = lenLOH + v[5] - v[4]
            ACMall = ACMall + v[1]
            ATEall = ATEall + v[7]
            ALEall = ALEall + v[8]
            AHTall = AHTall + v[0]
        for j, v in enumerate(nonLOH.values):
            numNonLOH = numNonLOH + v[-1]
            lenNonLOH = lenNonLOH + v[5] - v[4]
        LF = numLOH/(numLOH+numNonLOH)
        kf_data = np.array([[LOH.values, nonLOH.values], [numLOH, numNonLOH]])
        kf = chi2_contingency(kf_data)
        CLT = -10 * math.log(1 - kf[1])
        ACM = ACMall/LOH.values
        ATE = ATEall/LOH.values
        ALE = ALEall/LOH.values
        AHT = AHTall/LOH.values
        # print numLOH, numNonLOH, lenLOH / numLOH, lenNonLOH / numNonLOH
        data = [numLOH, numNonLOH, lenLOH/numLOH, lenNonLOH/numNonLOH,LF,CLT,ACM,ATE,ALE,AHT]
        return data


    def X_Y(self, S):
        train = S
        y = train['type']
        x = train.drop(['type'], 1)
        x_train = x.values
        y_train = y.values.ravel()
        return x, y


    def ds(self, file_path):
        ds = pd.read_csv(file_path)
        true_ds = pd.read_csv(file_path)

        ds = ds[(ds['DP'] > 30) & (ds['type'] == 'germline;panel_of_normals')]

        ds.loc[ds['type'].str.contains('germline;panel_of_normals'), 'type'] = 0

        ds.to_csv('C:/Users/Sherwin/Desktop/tmp/single_mut2_30X.csv', index=False)

        true_ds = true_ds[true_ds['type'] == 'PASS']
        true_ds.loc[true_ds['type'].str.contains('PASS'), 'type'] = 1

        true_ds.to_csv('C:/Users/Sherwin/Desktop/tmp/single_mut2_30X_true_PASS.csv', index=False)


    def dp(self, file_path):

        dp = pd.read_csv(file_path)
        dp.loc[dp['type'].str.contains('PASS'), 'type'] = 1
        # dp = dp[dp['DP'] > 500]
        # dp = dp.drop(['AF0'], 1)
        dp.to_csv('C:/Users/Sherwin/Desktop/tmp/paired_mut2_30X.csv', index=False)

    def meger(self, ds_file, dp_file):
        ds = pd.read_csv(ds_file)
        dp = pd.read_csv(dp_file)
        ds_sample = ds.sample(n=150, replace=False)
        dp_sample = dp.sample(n=300, replace=False)

        ds_t = ds.drop(ds_sample.index.values)
        dp_t = dp.drop(dp_sample.index.values)


        #
        # ds_01 = ds[ds['AF'] < 0.23]
        # ds_01 = ds_01.sample(n=100, replace=False)
        # ds_10 = ds[ds['AF'] >= 0.23]
        # ds_103 = ds_10[ds_10['AF'] < 0.3]
        # ds_103 = ds_103.sample(n=70, replace=False)
        # ds_10 = ds[ds['AF'] >= 0.3]
        # ds_104 = ds_10[ds_10['AF'] < 0.4]
        # ds_104 = ds_104.sample(n=50, replace=False)
        # ds_10 = ds[ds['AF'] >= 0.4]
        # ds_105 = ds_10[ds_10['AF'] < 0.5]
        # ds_105 = ds_105.sample(n=550, replace=False)
        # ds_10 = ds[ds['AF'] >= 0.5]
        # ds_106 = ds_10[ds_10['AF'] < 0.6]
        # ds_106 = ds_106.sample(n=550, replace=False)
        # ds_10 = ds[ds['AF'] >= 0.6]
        # ds_107 = ds_10[ds_10['AF'] < 0.7]
        # ds_107 = ds_107.sample(n=550, replace=False)
        # ds_10 = ds[ds['AF'] >= 0.7]
        # ds_108 = ds_10[ds_10['AF'] < 0.8]
        # ds_108 = ds_108.sample(n=50, replace=False)
        # ds_10 = ds[ds['AF'] >= 0.8]
        # ds_109 = ds_10[ds_10['AF'] < 0.9]
        # ds_109 = ds_109.sample(n=50, replace=False)
        # ds_10 = ds[ds['AF'] >= 0.9]
        # ds_1010 = ds_10[ds_10['AF'] < 1]
        # ds_1010 = ds_1010.sample(n=50, replace=False)
        # ds_train = pd.concat([ds_01, ds_103, ds_104, ds_105, ds_106, ds_107, ds_108, ds_109, ds_1010], axis=0)

        # ds_10 = ds_10.sample(n=110, replace=False)
        #
        # ds_ = pd.concat([ds_01, ds_10], axis=0)
        # ds_tt = ds.sample(n=10000, replace=False)

        # ds_t = ds.drop(ds_.index.values)

        # dp_01 = dp[dp['AF'] < 0.01]

        # dp_01 = dp_01.sample(n=100, replace=False)
        # dp_10 = dp[dp['AF'] >= 0.1]
        # dp_101 = dp_10[dp_10['AF'] < 0.2]
        # dp_101 = dp_101.sample(n=5, replace=False)
        # dp_10 = dp[dp['AF'] >= 0.2]
        # dp_102 = dp_10[dp_10['AF'] < 0.3]
        # dp_102 = dp_102.sample(n=50, replace=False)
        # dp_10 = dp[dp['AF'] >= 0.3]
        # dp_103 = dp_10[dp_10['AF'] < 0.4]
        # dp_103 = dp_103.sample(n=50, replace=False)
        # dp_10 = dp[dp['AF'] >= 0.4]
        # dp_104 = dp_10[dp_10['AF'] < 0.5]
        # dp_104 = dp_104.sample(n=50, replace=False)
        # dp_10 = dp[dp['AF'] >= 0.5]
        # dp_105 = dp_10[dp_10['AF'] < 0.6]
        # dp_105 = dp_105.sample(n=50, replace=False)
        # dp_10 = dp[dp['AF'] >= 0.6]
        # dp_106 = dp_10[dp_10['AF'] < 0.7]
        # dp_106 = dp_106.sample(n=20, replace=False)
        # dp_10 = dp[dp['AF'] >= 0.7]
        # dp_107 = dp_10[dp_10['AF'] < 0.8]
        # dp_107 = dp_107.sample(n=20, replace=False)
        # dp_10 = dp[dp['AF'] >= 0.8]
        # dp_108 = dp_10[dp_10['AF'] < 0.9]
        # dp_108 = dp_108.sample(n=10, replace=False)
        # dp_10 = dp[dp['AF'] >= 0.9]
        # dp_109 = dp_10[dp_10['AF'] < 1]
        # dp_109 = dp_109.sample(n=50, replace=False)
        # dp_train = pd.concat([dp_01, dp_101, dp_102, dp_103, dp_104, dp_105, dp_106, dp_107, dp_108, dp_109], axis=0)

        # dp_ = pd.concat([dp_01, dp_01], axis=0)
        #
        # dp_t = dp.drop(dp_.index.values)
        # dp_tt = dp.sample(n=5000, replace=False)
        #
        res = pd.concat([ds_sample, dp_sample], axis=0)
        res_t = pd.concat([ds_t, dp_t], axis=0)

        # res_all = pd.concat([ds, dp], axis=0)

        res.to_csv('C:/Users/Sherwin/Desktop/newdata/DATA/merge2_1000.csv', index=False)
        res_t.to_csv('C:/Users/Sherwin/Desktop/newdata/DATA/merge2_test.csv', index=False)
        # res_all.to_csv('C:/Users/Sherwin/Desktop/tmp/merge2_all.csv', index=False)

    def single(self, file_path):
        ds = pd.read_csv(file_path)

        # ds = ds[(ds['DP'] > 30) & (ds['type'] == 'germline;panel_of_normals')]
        #
        # ds.loc[ds['type'].str.contains('germline;panel_of_normals'), 'type'] = 0
        # print ds['FILTER']
        type = []
        for i in ds['type']:
            if i == 'PASS':
                type.append(1)
            else:
                type.append(0)
        ds['type'] = type
        ds_01 = ds[ds['type'] == 1]

        ds_01.to_csv('C:/Users/Sherwin/Desktop/tmp/single_mut2_test1_type.csv', index=False)

    def single_merge(self, file_path1, file_path2):
        ds = pd.read_csv(file_path1)
        dp = pd.read_csv(file_path2)

        type0 = []
        for i in ds['type']:
            if i == 'PASS':
                type0.append(1)
            else:
                type0.append(0)
        ds['type'] = type0
        ds_01 = ds[ds['type'] == 1]

        type1 = []
        for i in dp['type']:
            if i == 'PASS':
                type1.append(1)
            else:
                type1.append(0)
        dp['type'] = type1
        dp_01 = dp[dp['type'] == 1]

        # print ds_01,dp_01
        MD = pd.merge(ds_01, dp_01, on=['POS'])
        MD_ = pd.merge(ds, dp_01, on=['POS'])
        MD.to_csv('C:/Users/Sherwin/Desktop/tmp/MD.csv', index=False)
        MD_.to_csv('C:/Users/Sherwin/Desktop/tmp/MD_.csv', index=False)
        # dp_01.to_csv('C:/Users/Sherwin/Desktop/tmp/dp_01.csv', index=False)

    def single_paired_merge(self, file1, file2):
        ds = pd.read_csv(file1)
        dp = pd.read_csv(file2)

        single_paired = pd.merge(ds, dp, on=['POS','CHROM','REF','ALT','type','SAMPLEID'])
        single_paired.to_csv('C:/Users/Sherwin/Desktop/tmp/test_merge.csv', index=False)

    def tsvTocsv(self,file):
        tsv_file = pd.read_csv(file, sep='\t')

        tsv_file.to_csv('C:/Users/Sherwin/Desktop/newdata/DATA/tp.csv',index=False)

if __name__ == '__main__':
    tri = RWCSV()

    ds_file = 'C:/Users/Sherwin/Desktop/tmp/test_single_mut2.csv'
    dp_file = 'C:/Users/Sherwin/Desktop/tmp/paired_mut2.csv'
    # tri.ds(ds_file)
    # tri.dp(dp_file)
    ds_file_mut2_30X = 'C:/Users/Sherwin/Desktop/newdata/DATA/fp.csv'
    dp_file_mut2_30X = 'C:/Users/Sherwin/Desktop/newdata/DATA/dp.csv'
    tri.meger(ds_file_mut2_30X,dp_file_mut2_30X)
    # single_file = 'C:/Users/Sherwin/Desktop/tmp/single_mut2_test3.csv'
    # tri.single(single_file)

    single_file1 = 'C:/Users/Sherwin/Desktop/tmp/single_mut2_test2.csv'
    single_file2 = 'C:/Users/Sherwin/Desktop/tmp/single_mut2_test2_.csv'
    # tri.single_merge(single_file1,single_file2)

    single_file = 'C:/Users/Sherwin/Desktop/tmp/single_mut2_30X_true_PASS.csv'
    paired_file = 'C:/Users/Sherwin/Desktop/tmp/paired_mut2_30X.csv'
    # tri.single_paired_merge(single_file,paired_file)

    # tsv_file = 'C:/Users/Sherwin/Desktop/newdata/DATA/tp.tsv'
    # tri.tsvTocsv(tsv_file)

    test_file = 'C:/Users/Sherwin/Desktop/newdata/DATA/test.csv'
    # tri.pre_data(test_file)