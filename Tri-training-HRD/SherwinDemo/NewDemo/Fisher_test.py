#!/usr/bin/python
# coding=utf-8
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
#
# obs2 = [[483,478], [1,1]]
# aa, bb=stats.fisher_exact(obs2, alternative='greater')
# print(aa,bb)

nums = [0.0041,0.0054,0.0078,0.0162]
# nums = [0.0022,0.002,0.002,0.002,0.0019,0.0019,0.0018,0.004,0.0023]
#均值
me = np.mean(nums)
#中位数
md = np.median(nums)
counts = np.bincount(nums)
from scipy import stats
cc = stats.mode(nums)[0][0]
#返回众数
mm = np.argmax(counts)
print me,md,counts,cc