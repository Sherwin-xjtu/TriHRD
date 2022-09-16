#!/usr/bin/python
# coding=utf-8
from __future__ import division  # 用于/相除的时候,保留真实结果.小数

import math

import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency
import argparse
import logging
import vcf
import pandas as pd
from numpy import *
# from log_config import Config
import csv,os,argparse,string,sys,multiprocessing,logging,functools,time,signal, re
sys.dont_write_bytecode = True
csv.register_dialect("line_terminator",lineterminator="\n")
VERSION='1.0.1'

def hrd_data(file_path):
    reader = pd.read_csv(file_path,sep='\t')
    reader = reader.drop(['chrom','seg','num.mark','segclust','cnlr.median.clust'], 1)
    LOH = reader[reader['type'] == 1]
    nonLOH = reader[reader['type'] == 0]
    numLOH = 0
    numNonLOH = 0
    lenLOH = 0
    lenNonLOH = 0
    ACMall = 0
    ATEall = 0
    ALEall = 0
    AHTall = 0

    for j, v in enumerate(LOH.values):
        numLOH = numLOH + v[-1]
        lenLOH = lenLOH + v[5] - v[4]
        ACMall = ACMall + v[1]
        if not math.isnan(v[7]):
            ATEall = ATEall + v[7]
        if not math.isnan(v[8]):
            ALEall = ALEall + v[8]

        AHTall = AHTall + v[0]
    for j, v in enumerate(nonLOH.values):
        numNonLOH = numNonLOH + v[-1]
        lenNonLOH = lenNonLOH + v[5] - v[4]
    numLOH = LOH['lable'].size
    numNonLOH = nonLOH['lable'].size
    avLenLOH = float(lenLOH / numLOH)
    avLenNonLOH = float(lenNonLOH/numNonLOH)

    LF = float(numLOH / (numLOH + numNonLOH))
    # kf_data = np.array([[LOH['lable'].size, nonLOH['lable'].size], [numLOH, numNonLOH]])
    # kf = chi2_contingency(kf_data)
    # CLT = -10 * math.log(1 - kf[1])

    ACM = float(ACMall / LOH['lable'].size)
    ATE = float(ATEall / LOH['lable'].size)
    ALE = float(ALEall / LOH['lable'].size)
    AHT = float(AHTall / LOH['lable'].size)
    # print numLOH, numNonLOH, lenLOH / numLOH, lenNonLOH / numNonLOH
    data = [numLOH, numNonLOH, float(lenLOH/numLOH), float(lenNonLOH/numNonLOH), LF, ACM, ATE, ALE, AHT]
    return data

def hrd_data_test(file_path):
    reader = pd.read_csv(file_path,sep='\t')
    # reader = reader.drop(['chrom','seg','num.mark','segclust','cnlr.median.clust'], 1)
    LOH = reader[reader['PreType'] == 1]
    nonLOH = reader[reader['PreType'] == 0]
    numLOH = 0
    numNonLOH = 0
    lenLOH = 0
    lenNonLOH = 0
    ACMall = 0
    ATEall = 0
    ALEall = 0
    AHTall = 0

    for j, v in enumerate(LOH.values):
        numLOH = numLOH + v[-1]
        lenLOH = lenLOH + v[5] - v[4]
        ACMall = ACMall + v[1]
        if not math.isnan(v[7]):
            ATEall = ATEall + v[7]
        if not math.isnan(v[8]):
            ALEall = ALEall + v[8]
        AHTall = AHTall + v[0]
    for j, v in enumerate(nonLOH.values):
        numNonLOH = numNonLOH + v[-1]
        lenNonLOH = lenNonLOH + v[5] - v[4]
    # numLOH = LOH['lable'].size
    # numNonLOH = nonLOH['lable'].size
    avLenLOH = float(lenLOH / numLOH)
    avLenNonLOH = float(lenNonLOH/numNonLOH)

    LF = float(numLOH / (numLOH + numNonLOH))
    # kf_data = np.array([[LOH['lable'].size, nonLOH['lable'].size], [numLOH, numNonLOH]])
    # kf = chi2_contingency(kf_data)
    # CLT = -10 * math.log(1 - kf[1])

    ACM = float(ACMall / LOH['PreType'].size)
    ATE = float(ATEall / LOH['PreType'].size)
    ALE = float(ALEall / LOH['PreType'].size)
    AHT = float(AHTall / LOH['PreType'].size)
    # print numLOH, numNonLOH, lenLOH / numLOH, lenNonLOH / numNonLOH
    data = [numLOH, numNonLOH, avLenLOH, avLenNonLOH, LF, ACM, ATE, ALE, AHT]
    return data

# def processing():
#     # Y_list_str = map(str, self.Y_list)
#     # CHROM_list_str = map(str, self.CHROM_list)
#     # POS_list_str = map(str, self.POS_list)
#     # AF_list_str = map(str, self.AF_list)
#     # DP_list_str = map(str, self.DP_list)
#
#     # 字典中的key值即为csv中列名
#     dataframe_L = pd.DataFrame({'CHROM': CHROM_list_str,
#                                 'POS': POS_list_str,
#                                 'AF': AF_list_str,
#                                 'DP': DP_list_str,
#                                 'type': Y_list_str
#                                 },
#                                columns=['CHROM', 'POS','AF','DP','type'])
#
#     # 将DataFrame存储为csv,index表示是否显示行名，default=True
#     dataframe_L.to_csv(labeled_path, index=False,sep=',')

def getPathFile(path):
    '''
    name:getPathFile
    function:获取所给文件夹下所有vcf文件路径
    path：所给文件夹路径
    '''
    Path = []
    try:
        pathDir = os.listdir(path)
        for allDir in pathDir:
            child = os.path.join('%s/%s' % (path, allDir))
            # 跳过文件夹以及非流量包文件，将后缀名改为自己需要的文件类型即可实现自己的过滤
            if os.path.isfile(child) and (".tsv" in str(allDir) or (".tsv" in str(allDir))):
                Path.append(child)
    except:
        pass
    return Path

# def split_file(vcffile):
#     i = 0  # 设置计数器
#     vcf_reader = vcf.Reader(open(vcffile, 'r'))
#     b = os.path.dirname(vcffile)
#     os.mkdir(b + '/temp')
#     dir_path = b+'/temp/'
#
#     with open(vcffile) as f:
#         text = f.read()
#
#     f1 = file(vcffile, 'r')
#     hi = 0
#     for line in f1.readlines():
#         if line.startswith('#'):
#             hi = hi + 1
#         else:
#             break
#     length = len(text.splitlines())-hi
#     while i < length:  # 这里12345表示文件行数，如果不知道行数可用每行长度等其他条件来判断
#         vcf_writer = vcf.Writer(open(dir_path+'tmp' + str(i) + '.vcf', 'w'), vcf_reader)
#         # with open('newfile'+str(i),'w') as f1:
#         for j in range(0, 1000):  # 这里设置每个子文件的大小
#             if i < length:  # 这里判断是否已结束，否则最后可能报错
#                 # f1.writelines(f.readline())
#                 vcf_writer.write_record(vcf_reader.next())
#                 i = i + 1
#             else:
#                 break
#     return dir_path

if __name__=="__main__":

    dir_path = 'C:/Users/Sherwin/Desktop/LOH_HRD/lable_result02/test_/TRUE/'
    all_file_path = getPathFile(dir_path)

    labeled_path = 'C:/Users/Sherwin/Desktop/LOH_HRD/lable_result02/test_/test_true.tsv'
    numLOH_list = []
    numNonLOH_list = []
    avLenLOH_list = []
    avLenNonLOH_list = []
    LF_list = []
    ACM_list = []
    ATE_list = []
    ALE_list = []
    AHT_list = []
    type_list = []

    for file in all_file_path:
        # data = hrd_data_test(file)
        data = hrd_data_test(file)
        numLOH_list.append(data[0])
        numNonLOH_list.append(data[1])
        avLenLOH_list.append(data[2])
        avLenNonLOH_list.append(data[3])
        LF_list.append(data[4])
        ACM_list.append(data[5])
        ATE_list.append(data[6])
        ALE_list.append(data[7])
        AHT_list.append(data[8])
        type_list.append(1)

    # 字典中的key值即为csv中列名
    dataframe_L = pd.DataFrame({'numLOH': numLOH_list,
                                'numNonLOH': numNonLOH_list,
                                'avLenLOH': avLenLOH_list,
                                'avLenNonLOH': avLenNonLOH_list,
                                'LF': LF_list,
                                'ACM': ACM_list,
                                'ATE': ATE_list,
                                'ALE': ALE_list,
                                'AHT': AHT_list,
                                'type': type_list
                                },
                               columns=['numLOH', 'numNonLOH', 'avLenLOH', 'avLenNonLOH', 'LF', 'ACM', 'ATE', 'ALE', 'AHT','type'])

    # 将DataFrame存储为csv,index表示是否显示行名，default=True
    dataframe_L.to_csv(labeled_path, index=False, sep='\t')















