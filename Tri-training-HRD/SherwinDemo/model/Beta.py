#!/usr/bin/python
# coding=utf-8
import re
import warnings

warnings.filterwarnings("ignore")
from scipy import stats
import pandas as pd
import numpy

from scipy.stats import beta
import numpy as np
import matplotlib.pyplot as plt

# 注：ttest_1samp、ttest_ind和ttest_rel均进行双侧检验。
reader_data = pd.read_csv('C:/Users/Sherwin/Desktop/newdata/170014863BD_170014863FD_2_somatic_filtered_single.csv')
# print type(reader[reader['type'].isin(['PASS'])])
samples_af1 = []
samples2_tlod1 = []
samples_af2 = []
samples2_tlod2 = []
reader = reader_data[reader_data['DP'] > 30]
reader.to_csv('C:/Users/Sherwin/Desktop/newdata/170014863BD_170014863FD_2_somatic_filtered_single_30X.csv', index=False)
reader = pd.read_csv('C:/Users/Sherwin/Desktop/newdata/170014863BD_170014863FD_2_somatic_filtered_single_30X.csv')

a = 1
b = 1
x = [0.684000015,0.666999996,0.666999996,0.666999996,0.998]
y = beta.pdf(x,a,b)
plt.plot(x,y)
plt.title('Beta')
plt.xlabel('x')
plt.ylabel('density')
plt.show()