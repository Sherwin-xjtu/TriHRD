#!/usr/bin/python
# coding=utf-8
import re

from scipy import stats
import pandas as pd
import numpy as np

# 注：ttest_1samp、ttest_ind和ttest_rel均进行双侧检验。

# reader = pd.read_csv('C:/Users/Sherwin/Desktop/tmp/test_single_mut2.csv')
# for index, row in reader.iterrows():
#     print type(row['type']),row['type']

# a = [0.666999996,0.684000015]
# b = [0.666999996,0.666999996,0.666999996]
# t_value1, p_value1 = stats.ttest_1samp(a, 0.995000005)
# print p_value1
# if p_value1 < 0.00001:
#     print 'pass'
# t_value2, p_value2 = stats.ttest_1samp(a, 0.995000005)
# print p_value1
# if p_value2 < 0.00001:
#     print 'pass'
#

data = [[1, 2], [3, 4]]

print np.amax(data, axis=1)