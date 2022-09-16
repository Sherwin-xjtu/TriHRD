#!/usr/bin/python
# coding=utf-8
import re
import warnings

from SherwinDemo.model.IDW import InverseDistanceWeight

warnings.filterwarnings("ignore")
from scipy import stats, mean
import pandas as pd
import numpy


# 注：ttest_1samp、ttest_ind和ttest_rel均进行双侧检验。
#
# reader_data = pd.read_csv('C:/Users/Sherwin/Desktop/newdata/170014863BD_170014863FD_2_somatic_filtered_single.csv')
#
# # print type(reader[reader['type'].isin(['PASS'])])
# samples_af1 = []
# samples2_tlod1 = []
# samples_af2 = []
# samples2_tlod2 = []
# samples = []
# reader = reader_data[reader_data['DP'] > 30]
# reader.to_csv('C:/Users/Sherwin/Desktop/newdata/170014863BD_170014863FD_2_somatic_filtered_single_30X.csv', index=False)
# reader = pd.read_csv('C:/Users/Sherwin/Desktop/newdata/170014863BD_170014863FD_2_somatic_filtered_single_30X.csv')
# IDW = InverseDistanceWeight()
# n = 5
# for index, row in reader.iterrows():
#     samples = []
#     sample = None
#     sp = []
#     point = []
#     arr = row['type'].replace(']', '')
#     arr = arr.replace('[', '')
#     arr = arr.replace('\'', '')
#
#     if row['DP'] > 30:
#         if arr == 'PASS':
#             point.append(row['POS'])
#             point.append(row['DP'])
#             point.append(float(row['AF']))
#             sp_f = []
#             sp_b = []
#             fw = 0
#             bw = 0
#             for k in range(index,index+50):
#                 sp_f = []
#                 sample = reader.iloc[k-1]
#                 arr = sample['type'].replace(']', '')
#                 arr = arr.replace('[', '')
#                 arr = arr.replace('\'', '')
#                 if 'germline, panel_of_normals' == arr:
#                     samples_af1.append(sample['AF'])
#                     samples2_tlod1.append(sample['TLOD'])
#                     sp_f.append(sample['POS'])
#                     sp_f.append(sample['DP'])
#                     sp_f.append(float(sample['AF']))
#                     samples.append(sp_f)
#                     fw = fw + 1
#                 if fw == n:
#                     break
#
#             for j in range(index, index+50):
#                 sp_b = []
#                 sample = reader.iloc[j + 1]
#                 arr = sample['type'].replace(']', '')
#                 arr = arr.replace('[', '')
#                 arr = arr.replace('\'', '')
#                 if 'germline, panel_of_normals' == arr:
#                     samples_af1.append(sample['AF'])
#                     samples2_tlod1.append(sample['TLOD'])
#                     sp_b.append(sample['POS'])
#                     sp_b.append(sample['DP'])
#                     sp_b.append(float(sample['AF']))
#                     samples.append(sp_b)
#                     bw = bw + 1
#                 if bw == n:
#                     break
#             P = 3
#
#             if samples == []:
#                 print row['POS']
#                 continue

            # t_value1, p_value1 = stats.ttest_1samp(samples_af1, row['AF'])

            # if p_value1 < 0.01:
            #     t_value2, p_value2 = stats.ttest_1samp(samples_af2, row['AF'])
            #     if p_value2 < 0.01:
            #         # t_value3, p_value3 = stats.ttest_1samp(samples2_tlod1, row['TLOD'])
            #         # if p_value3 < 0.01:
            #         #     t_value4, p_value4 = stats.ttest_1samp(samples2_tlod2, row['TLOD'])
            #         #     if p_value4 < 0.01:
            #         # print row['POS'],row['DP'],row['AF']
            #         pass
x = [66, 75, 78, 80, 81, 81, 82, 83, 83, 83, 83, 84, 85, 85, 86, 86, 86, 86, 87, 87, 88, 88, 88, 88]
mean(x)
stats.binom.test(sum(x > 99), len(x), p=0.5, alternative="less")


