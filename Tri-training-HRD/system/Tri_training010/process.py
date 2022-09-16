#!/usr/bin/python
# coding=utf-8
import numpy as np
import pandas as pd
from system.Setting.config import Config
from sklearn.preprocessing import MinMaxScaler


# 预处理数据

class Process:
    def __init__(self):
        self.labeled_path = Config.labeled_path
        self.labeled_path = Config.t_labeled_path
        self.unlabeled_path = Config.unlabeled_path
        self.L = None  # 初始已标记样本集
        self.T = None  # 测试集
        self.U = None  # 初始未标记样本集
        self.U_1 = None  # Sherwin
        self.TV = None  # Sherwin 模型验证集

    # 读取已标记数据并且分割训练集和测试集

    def read_labeled(self,train_set,unabled_set,uu_reader):
        label_data = train_set
        test_data = unabled_set
        unlabel_data = uu_reader
        # tv_label_data = pd.read_csv('C:/Users/Sherwin/Desktop/newdata/DATA/merge2_test.csv')
        scaler = MinMaxScaler()

        # label_data_sample = label_data.sample(n=100,replace=False)
        # train = label_data.drop(['CHROM', 'POS', 'SAMPLEID', 'REF', 'ALT', 'CONTQ', 'TLOD', 'AD'], 1)
        #['CHROM', 'POS', 'ID', 'DP',  'REF', 'ALT', 'SB_rf','SB_rr','SB_af','SB_ar','F1R2_rf','F1R2_af','F2R1_rr','F2R1_ar','MPOS','SBR','FRR','ECNT','CONTQ','TLOD','AF','MMQ','MBQ','STRANDQ','GERMQ','SEQQ','ROQ']
        train = label_data
        test = test_data
        unlabel = unlabel_data

        scaler.fit(train.iloc[:, :-1])
        train_scaled = scaler.transform(train.iloc[:, :-1])
        test_scaled = scaler.transform(test.iloc[:, :-1])
        unlabel_scaled = scaler.transform(unlabel.iloc[:, :-1])
        #
        train_scaled_ = pd.DataFrame(train_scaled, columns=['numLOH', 'numNonLOH', 'avLenLOH', 'avLenNonLOH', 'LF', 'ACM', 'ATE', 'ALE', 'AHT'])
        train_scaled_['type'] = label_data['type'].values

        test_scaled_ = pd.DataFrame(test_scaled, columns=['numLOH', 'numNonLOH', 'avLenLOH', 'avLenNonLOH', 'LF', 'ACM', 'ATE', 'ALE', 'AHT'])
        test_scaled_['type'] = test_data['type'].values

        unlabel_scaled = pd.DataFrame(unlabel_scaled,columns=['numLOH', 'numNonLOH', 'avLenLOH', 'avLenNonLOH', 'LF', 'ACM', 'ATE', 'ALE', 'AHT'])
        unlabel_scaled['type'] = unlabel_data['type'].values
        # print train_scaled_,test_scaled_
        self.L = train
        self.T = test
        self.U = unlabel

    # 读取未标记数据
    def read_unlabeled(self):
        unlabel_data = pd.read_csv('G:/Tri-training-HRD/Alldata/labeled/NA12877_stander.csv')
        self.U_1 = unlabel_data
        self.U = unlabel_data


if __name__ == '__main__':
    pro = Process()
    pro.read_labeled()
    pro.read_unlabeled()
    L = pro.L
# print(L)
