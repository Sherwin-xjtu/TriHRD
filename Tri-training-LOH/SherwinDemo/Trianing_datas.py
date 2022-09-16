#!/usr/bin/python
# coding=utf-8
import numpy as np
import pandas as pd


tp_data = pd.read_csv('../dealData/data_processing/tp_s.csv')
tp_data = tp_data.drop(['CHROM','POS','QUAL','SOR'], 1)
tp_trianing_data = tp_data.sample(n=100,replace = True)
tp_data = tp_data.drop(tp_trianing_data.index.values)
tp_test = tp_data.sample(n=100,replace = True)
tp_data = tp_data.drop(tp_test.index.values)

fp_data = pd.read_csv('../dealData/data_processing/fp_s.csv')
fp_data = fp_data.drop(['CHROM','POS','QUAL','SOR'], 1)
fp_trianing_data = fp_data.sample(n=100,replace = True)
fp_data = fp_data.drop(fp_trianing_data.index.values)
fp_test = fp_data.sample(n=100,replace = True)
fp_data = fp_data.drop(fp_test.index.values)

res_trianing = pd.concat([tp_trianing_data,fp_test],axis=0)
res_test = pd.concat([tp_test,fp_test],axis=0)
res_all = pd.concat([tp_data,fp_data],axis=0)
res_trianing.to_csv('../dealData/data_processing/trianing_50_data.csv',index = False)
res_test.to_csv('../dealData/data_processing/new_data.csv',index = False)
res_all.to_csv('../dealData/data_processing/U_data.csv',index = False)