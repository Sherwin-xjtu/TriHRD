#!/usr/bin/python
# coding=utf-8
import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.preprocessing import Imputer


def u_standardization(input_path,output_path):
    train = pd.read_csv(input_path)
        # train['CHROM'] = train['CHROM'].astype(int)
    # train['CHROM']=train['CHROM'].replace(['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','X','Y'],
    #                            [1,2,3,4,5,6,7,8,9,19,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25])
    # train.to_csv('../dealData/data/Test_U__072302_t.csv',index = False)
    # train = pd.read_csv("../dealData/data/Test_U__072302_t.csv")
    # train.fillna(train.mean()).to_csv('../dealData/data/Test_U__072302_t_11.csv',index = False)
    # train = train.fillna(train.mean())
    # train = Imputer().fit_transform(train)
    # 标准化处理
    # label_data = pd.read_csv('../dealData/data/Test_U__072302_t_11.csv')
    # cols = list(train)
    # # move the column to head of list using index, pop and insert
    # cols.insert(2, cols.pop(cols.index('QUAL')))
    # train = train.ix[:, cols]
    train.iloc[:,3:-1] = train.iloc[:,3:].astype(np.float64)
    # 标准化 normalized_X = preprocessing.normalize()
    train.iloc[:,3:-1] = train.iloc[:,3:].apply(preprocessing.scale)
    train.to_csv(output_path,index = False)

def l_standardization(input_path,output_path):
    train = pd.read_csv(input_path)
    train = train.fillna(train.mean())
    # train = train.drop(['AC','AF'], 1)
    # 标准化处理
    # label_data = pd.read_csv('../dealData/data/Test_U__072302_t_11.csv')
    # 标准化 normalized_X = preprocessing.normalize()
    train.iloc[:, 2:-1] = train.iloc[:, 2:-1].astype(np.float64)
    # train.iloc[:, 3:-2] = preprocessing.normalize(train.iloc[:, 3:-2])
    train.iloc[:, 2:-1] = preprocessing.scale(train.iloc[:, 2:-1])
    train.to_csv(output_path,index = False)

if __name__=="__main__":

    # u_input_path = "../dealData/data/180807_U.csv"
    # u_output_path = "../dealData/data_processing/180807_U_s.csv"
    # u_standardization(u_input_path,u_output_path)

    l_input_path = "../dealData/data_processing/all_1500.csv"
    l_output_path = "../dealData/data_processing/all_1500_s.csv"
    l_standardization(l_input_path, l_output_path)
    #
    lt_input_path = "../dealData/data_processing/trianing_50_data.csv"
    lt_output_path = "../dealData/data_processing/trianing_50_data_s.csv"
    l_standardization(lt_input_path, lt_output_path)
    #
    # unlabeled = pd.read_csv('../dealData/data_processing/chr21_fp_ns.csv')
    # labeled = pd.read_csv('../dealData/data_processing/chr21_tp_ns.csv')
    # tp = labeled
    # fp = unlabeled
    # res = pd.concat([tp, fp], axis=0)
    # res.to_csv('../dealData/data_processing/chr21_nall_labeled.csv', index=False)