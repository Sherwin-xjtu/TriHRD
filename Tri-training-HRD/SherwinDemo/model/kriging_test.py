#!/usr/bin/python
# coding=utf-8
import numpy as np
from math import *
from numpy.linalg import *

h_data = np.loadtxt(open('C:/Users/Sherwin/Desktop/tt.csv'), delimiter=",", skiprows=0)
print('原始数据如下(x,y,z):\n未知点高程初值设为0\n', h_data)


def dis(p1, p2):
    a = pow((pow((p1[0] - p2[0]), 2) + pow((p1[1] - p2[1]), 2)), 0.5)
    return a


def rh(z1, z2):
    r = 1 / 2 * pow((z1[2] - z2[2]), 2)
    return r


def proportional(x, y):
    xx, xy = 0, 0
    for i in range(len(x)):
        xx += pow(x[i], 2)
        xy += x[i] * y[i]
    k = xy / xx
    return k


r = []
pp = []
p = []
for i in range(len(h_data)):
    pp.append(h_data[i])
for i in range(len(pp)):
    for j in range(len(pp)):
        p.append(dis(pp[i], pp[j]))
        r.append(rh(pp[i], pp[j]))
r = np.array(r).reshape(len(h_data), len(h_data))
r = np.delete(r, len(h_data) - 1, axis=0)
r = np.delete(r, len(h_data) - 1, axis=1)

h = np.array(p).reshape(len(h_data), len(h_data))
h = np.delete(h, len(h_data) - 1, axis=0)
oh = h[:, len(h_data) - 1]
h = np.delete(h, len(h_data) - 1, axis=1)

hh = np.triu(h, 0)
rr = np.triu(r, 0)
r0 = []
h0 = []
for i in range(len(h_data) - 1):
    for j in range(len(h_data) - 1):
        if hh[i][j] != 0:
            a = h[i][j]
            h0.append(a)
        if rr[i][j] != 0:
            a = rr[i][j]
            r0.append(a)
k = proportional(h0, r0)
hnew = h * k
a2 = np.ones((1, len(h_data) - 1))
a1 = np.ones((len(h_data) - 1, 1))
a1 = np.r_[a1, [[0]]]
hnew = np.r_[hnew, a2]
hnew = np.c_[hnew, a1]
print('半方差联立矩阵：\n', hnew)
oh = np.array(k * oh)
oh = np.r_[oh, [1]]
w = np.dot(inv(hnew), oh)
print('权阵运算结果：\n', w)
z0, s2 = 0, 0
for i in range(len(h_data) - 1):
    z0 = w[i] * h_data[i][2] + z0
    s2 = w[i] * oh[i] + s2
s2 = s2 + w[len(h_data) - 1]
print('未知点高程值为：\n', z0)
print('半变异值为：\n', pow(s2, 0.5))
