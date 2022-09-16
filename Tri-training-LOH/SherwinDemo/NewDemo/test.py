#!/usr/bin/python
# coding=utf-8
import math
import os
import pandas as pd
import vcf
import pandas as pd


tv_label_data = pd.read_csv('C:/Users/Sherwin/Desktop/LOH_HRD/189003592BCD_189003592TD_fct_cncf.tsv', sep='\t')
file_path = 'C:/Users/Sherwin/Desktop/LOH_HRD/all_r_2000_results.csv'

from  scipy.stats import chi2_contingency
import numpy as np
kf_data = np.array([[37,27], [39,21]])
kf = chi2_contingency(kf_data)
print -10*math.log(1-kf[1])
print kf
def hrd_data(file_path):
    reader = pd.read_csv(file_path)
    LOH = reader[reader['type'] == 1]
    nonLOH = reader[reader['type'] == 0]
    numLOH = 0
    numNonLOH = 0
    lenLOH = 0
    lenNonLOH = 0
    for j, v in enumerate(LOH.values):
        numLOH = numLOH + v[-1]
        lenLOH = lenLOH +v[5] - v[4]

    for j, v in enumerate(nonLOH.values):
        numNonLOH = numNonLOH + v[-1]
        lenNonLOH = lenNonLOH + v[5] - v[4]

    print numLOH,numNonLOH,lenLOH/numLOH,lenNonLOH/numNonLOH
hrd_data(file_path)


import numpy as np
l1 = [1,3,4]
l2 = [1,3]
li = []

def ts(re):
    if re == 1:
        re = 9
        return re
for i in l1:
    id = ts(i)
    if id is not None:
        i = id
    li.append(i)

for i in l1:
    if i not in l2:
        li.append(i)

salaries = pd.DataFrame({
    'name': ['BOSS', 'Lilei', 'Lilei', 'Han', 'Lilei', 'BOSS', 'Han', 'BOSS'],
    'Year': [2016, 2016, 2016, 2017, 2016, 2017, 2017, 2017],
    'Salary': [1, 2, 2, 5, 2, 6, 5, 8],
    'Bonus': [2, 2, 2, 5, 2, 4, 5, 6]
})

# print(salaries['Bonus'].duplicated(keep='first')),
# print(salaries[salaries['Bonus'].duplicated(keep='first')].index),
dd = salaries[salaries['Bonus'].duplicated(keep='first')]
cd = dd[dd['Year'].duplicated(keep='first')]
cd = dd[dd['name'].duplicated(keep='first')]
print cd









li = '3:4'.split(':')
print int(li[0])-int(li[1])
a=[2,3,4,5]
b=[2,5]
tmp = list(set(a) - set(b))
print tmp
a = [1,2,3,4]
b = [1,3,4]
print set(a).issubset(set(b))
vcffile = 'C:/Users/Sherwin/Desktop/luo/208001981fD_AF25-50ng.c1m8g3.vcf'
# new_vcffile = 'C:/Users/Sherwin/Desktop/platypus/190018206_TN_new.vcf'
vcf_reader = vcf.Reader(open(vcffile, 'r'))

# vcf_writer = vcf.Writer(open(new_vcffile, 'w'), vcf_reader)
# str1 = 'a,c,f,t'
# str1_arr = str1.split(',')
# if 'a' in str1_arr:
#     print 'dd'
for rec in vcf_reader:
    print rec.ALT.split(',')





# vcf_reader = vcf.Reader(open(vcffile, 'r'))
# for rec in vcf_reader:
#     # vcf_writer.write_record(rec)
#     # # for key, value in rec.samples.iteritems():
#     # AF = value['NV']
#     print type(rec.CHROM)

# LI = [1,3,4]
# GG = [3,5]
# LI = 'ssss'
# print LI[:]
def getNumofCommonSubstr(str1, str2):
    lstr1 = len(str1)
    lstr2 = len(str2)
    record = [[0 for i in range(lstr2 + 1)] for j in range(lstr1 + 1)]  # 多一位
    maxNum = 0  # 最长匹配长度
    p = 0  # 匹配的起始位

    for i in range(lstr1):
        for j in range(lstr2):
            if str1[i] == str2[j]:
                # 相同则累加
                record[i + 1][j + 1] = record[i][j] + 1
                if record[i + 1][j + 1] > maxNum:
                    # 获取最大匹配长度
                    maxNum = record[i + 1][j + 1]
                    # 记录最大匹配长度的终止位置
                    p = i + 1
    return str1[p - maxNum:p], maxNum


str1 = 'GCGGGTGCAGCTCGGGCCCTGCTGC'
str2 = 'CGCGGTGCAGCTCGGGGCCTGCTT'

# if len(str1) == len(str2):
#     for i in range(len(str1)):
#         print i,str1[i],str2[i]
cop, n = getNumofCommonSubstr(str1, str2)
str1_arr = str1.split(cop)
# str1_arr[0] = str1_arr[0] + cop[0]
# str1_arr[1] = cop[-1] + str1_arr[1]
str2_arr = str2.split(cop)
# str2_arr[0] = str2_arr[0] + cop[0]
# str2_arr[1] = cop[-1] + str2_arr[1]
print str1_arr,str2_arr,cop
# for i in str1:
#     print i
# if str2_arr[0] == '':
#     print 5
# i = 0  # 设置计数器
# with open(vcffile) as f:
#     text = f.read()
# f1=file(vcffile,'r')
# i = 0
# for line in f1.readlines():#[N:]:
#     if line.startswith('#'):
#         i = i + 1
#     else:
#         break
# print i
#     # length = len(text.splitlines())

# vcf_reader = vcf.Reader(open(vcffile, 'r'))
#
# b = os.path.dirname(vcffile)
# os.mkdir(b + '/temp')
# dir_path = b + '/temp/'
# os.removedirs(dir_path)
# def spfu(listTemp, n):
#     for i in range(0, len(listTemp), n):
#         yield listTemp[i:i + n]
# nlt = [1,2,3,4]
# nlt_arr = spfu(nlt, 2)
# for i in range(2):
#     print type(next(nlt_arr))
# while i < 12345:  # 这里12345表示文件行数，如果不知道行数可用每行长度等其他条件来判断
#     vcf_writer = vcf.Writer(open(dir_path + 'tmp' + str(i) + '.vcf', 'w'), vcf_reader)
#     # with open('newfile'+str(i),'w') as f1:
#     for j in range(0, 1000):  # 这里设置每个子文件的大小
#         if i < 12345:  # 这里判断是否已结束，否则最后可能报错
#             # f1.writelines(f.readline())
#             vcf_writer.write_record(vcf_reader.next())
#             i = i + 1
#         else:
#             break

# list1 = ['11', '22']
# print len(list1)
#
#
# class Base:
#     def __init__(self,s,pos):
#         self.seq = s
#         self.pos = pos
#
#
# seq = 'acvb'
# print (1 and 0 or 0 and 1)
# pos = 4
# b = []
# i = 0
# for s in seq:
#     b.append(Base(s,pos))
#     pos = pos + 1
# print b[1].seq
# l1 = ['b','c','d','b','c','a','a']
# l2 = list(set(l1))
# print l2
# file_path = 'C:/Users/Sherwin/Desktop/luo/all_r_2000_results.csv'
# reader = pd.read_csv(file_path)
# var = 29443613 in reader['POS'].values
# if var:
#     a = reader[(reader.POS == 29443613)].index
#     c = a.values[0]
#     print (reader.iloc[c]).ALT
# # print var
#
# df = pd.DataFrame({'BoolCol': [1, 2, 3, 3, 4],'attr': [22, 33, 22, 44, 66]},
# index=[10,20,30,40,50])
#
# def test():
#     for i in range(10):
#         if i == 3 or i ==7:
#             return 'happy'
# tt = test()
# print tt
