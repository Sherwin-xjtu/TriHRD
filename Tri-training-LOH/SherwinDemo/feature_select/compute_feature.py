#!/usr/bin/python
# coding=utf-8
import pandas as pd
import numpy as np
import xgboost as xgb
import operator
import matplotlib.pyplot as plt
import sys
import os
import vcf


reader = pd.read_csv('C:/Users/Sherwin/Desktop/newdata/DATA/run_idw_fp.csv')
TT = reader[reader['AF']<0.012]
#print type(reader['AF'][0])
r_strand_bias_rate = abs(reader['SB_rf']-reader['SB_rr'])/(reader['SB_rf']+reader['SB_rr'])
a_strand_bias_rate = abs(reader['SB_af']-reader['SB_ar'])/(reader['SB_af']+reader['SB_ar'])
strand_bias_rate = r_strand_bias_rate-a_strand_bias_rate
reader['sbr'] = strand_bias_rate
reader['sbar'] = a_strand_bias_rate

md_rate = abs(reader['SB_rf']-reader['SB_af'])+abs(reader['SB_rr']-reader['SB_ar'])
reader['mr'] = md_rate

frfr_r_strand_bias_rate = abs(reader['F1R2_rf']-reader['F2R1_rr'])/(reader['F1R2_rf']+reader['F2R1_rr'])
frfr_a_strand_bias_rate = abs(reader['F1R2_af']-reader['F2R1_ar'])/(reader['F1R2_af']+reader['F2R1_ar'])
frfr_strand_bias_rate = frfr_r_strand_bias_rate-frfr_a_strand_bias_rate
reader['frfrr'] = frfr_strand_bias_rate
# re = reader[reader['frfrr']<-0.49]
#
# re = reader[reader['sbr']<= -0.25]
# print re
# print pd.concat([TT, re], axis=0), pd.merge(TT,re,how='outer')
# # res = pd.concat([TT, re], axis=0)
# res.to_csv('C:/Users/Sherwin/Desktop/newdata/DATA/GGFFGf.csv', index=False, sep=',')
# reader.to_csv('C:/Users/Sherwin/Desktop/newdata/DATA/run_idw_tp.csv', index=False, sep=',')
# print reader['AF']
# for index,af in reader['AF'].iteritems():
#     tmp = []
#     c = af.split(',')
#     tmp.append(float(c[0]))
#     if c[1] == '':
#         tmp.append(0)
#     li_af.append(tmp)
# reader['AF'] = li_af
# print reader['AF']

li = [1,2,3,4]
print li[0:]