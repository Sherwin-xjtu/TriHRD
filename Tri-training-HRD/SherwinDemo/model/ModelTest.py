#!/usr/bin/python
# coding=utf-8

from sklearn.externals import joblib
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from system.Tri_training01.Report import estimate
model_file = 'C:/Users/Sherwin/Desktop/Model/tri_clt02.model'
# ds_file_mut2_30X = 'C:/Users/Sherwin/Desktop/tmp/single_mut2_30X.csv'
# dp_file_mut2_30X = 'C:/Users/Sherwin/Desktop/tmp/paired_mut2_30X.csv'
train_data = pd.read_csv('C:/Users/Sherwin/Desktop/tmp/merge2_1000.csv')
paired_data = pd.read_csv('C:/Users/Sherwin/Desktop/tmp/170014863BD_170014863FD_2_somatic_filtered_paired.csv')
single_data = pd.read_csv('C:/Users/Sherwin/Desktop/tmp/170014863BD_170014863FD_2_somatic_filtered_single.csv')
scaler = MinMaxScaler()

# label_data_sample = label_data.sample(n=100,replace=False)
# train = label_data.drop(['CHROM', 'POS', 'SAMPLEID', 'REF', 'ALT', 'CONTQ', 'TLOD', 'AD'], 1)
train = train_data.drop(['CHROM', 'POS', 'SAMPLEID', 'REF', 'ALT', 'AD', 'CONTQ','DP'], 1)
paired = paired_data.drop(['CHROM', 'POS', 'REF', 'ALT','CONTQ','DP'], 1)
single = single_data.drop(['CHROM', 'POS','REF', 'ALT', 'CONTQ','DP'], 1)

scaler.fit(train.iloc[:, 1:])

train_scaled = scaler.transform(train.iloc[:, 1:])
paired_scaled = scaler.transform(paired.iloc[:, 1:])
single_scaled = scaler.transform(single.iloc[:, 1:])


single_scaled = pd.DataFrame(single_scaled, columns=['AF', 'TLOD'])
single_scaled['type'] = single_data['type']

paired_scaled = pd.DataFrame(paired_scaled, columns=['AF', 'TLOD'])
paired_scaled['type'] = paired_data['type']

paired_scaled = paired_scaled.drop(['TLOD'], 1)
single_scaled = single_scaled.drop(['TLOD'], 1)

model = joblib.load(open(model_file, 'rb'))  # 加载保存的模型
Estimate = estimate()  # 评估器

Estimate.bagging_report(M=model, T=single_scaled, L=paired_scaled)