#!/usr/bin/python
# coding=utf-8
import math

import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import pandas as pd
def test(n):
    global m
    m = n
    m += 1
m =0
test(m)
print 'The number is ',m
# f = open('C:/Users/Sherwin/Desktop/vcf.vcf'+".txt", 'w')
# f.write('The number of mnp is '+str(5))
# f.close()
fc = open('C:/Users/Sherwin/Desktop/vcf.vcf'+".txt", 'a')
fc.write('The number of mnp is '+str(444))
fc.close()
test(m)
print m
# def ff(x,n):
#     k = 1
#     r = 1
#     while n>0:
#         for k in range(0,n):
#             k=n%3
#             if k>0:
#                 r = r * x
#                 k -=1
#                 print r
#         n=n/3
#         x=x*x*x
#     return r*x
# a = ff(2,5)
# print a,math.exp(4)
# # %matplotlib inline
#
# # x = [0.07, 0.01, 0.03, 0.03, 0.06, 0.05, 0.04, 0.1, 0.08, 0.02, 0.02, 0.03, 0.07, 0.1, 0.04, 0.06, 0.03, 0.03, 0.1, 0.08, 0.12, 0.07, 0.09, 0.13, 0.12, 0.15, 0.06, 0.06, 0.09, 0.09, 0.22, 0.09, 0.06, 0.13, 0.14, 0.07, 0.07]
# #
# # x = np.reshape(x,newshape=(37,1))
# #
# # y = [1.23, 3.54, 2.71, 2.92, 0.65, 1.66, 1.49, 0.65, 1.04, 1.09, 0.94, 1.27, 1.07, 0.85, 0.85, 0.61, 0.92, 1.16, 1.02, 0.74, 1.0, 1.2, 0.8, 0.96, 0.64, 1.06, 0.58, 0.7, 0.6, 0.74, 0.65, 0.95, 0.72, 0.77, 0.99, 0.81, 1.11]
# # print len(y)
# # y = np.reshape(y,newshape=(37,1))
# # # 调用模型
# # lr = LinearRegression()
# # # 训练模型
# # lr.fit(x,y)
# # # 计算R平方
# # print (lr.score(x,y))
# # # 计算y_hat
# # y_hat = lr.predict(x)
# # # 打印出图
# # plt.scatter(x,y)
# # plt.plot(x, y_hat)
# # plt.show()
# file_path = 'C:/Users/Sherwin/Desktop/TMB/Reference.csv'
# reader = pd.read_csv(file_path)
# print reader['POS']