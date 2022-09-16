#!/usr/bin/python
# coding=utf-8
import pandas as pd
import numpy as np

t1 = pd.read_csv('C:/Users/Sherwin/Desktop/LOH_HRD/lable_result02/train/FALSE/F170014295BCD_170014295FD_lableResult_loh.tsv', sep='\t')
t2 = pd.read_csv('C:/Users/Sherwin/Desktop/LOH_HRD/lable_result02/train/FALSE/F180008383BD_180008383FD_lableResult_loh.tsv', sep='\t')
t3 = pd.read_csv('C:/Users/Sherwin/Desktop/LOH_HRD/lable_result02/train/FALSE/F180011855BCD_180011855FD_lableResult_loh.tsv', sep='\t')
t4 = pd.read_csv('C:/Users/Sherwin/Desktop/LOH_HRD/lable_result02/train/FALSE/F180013396BCD_180013396FD_lableResult_loh.tsv', sep='\t')
t5 = pd.read_csv('C:/Users/Sherwin/Desktop/LOH_HRD/lable_result02/train/FALSE/F180015038BCD_180015038TD_lableResult_loh.tsv', sep='\t')
t6 = pd.read_csv('C:/Users/Sherwin/Desktop/LOH_HRD/lable_result02/train/FALSE/F180015360BCD_180015359FD_lableResult_loh.tsv', sep='\t')
t7 = pd.read_csv('C:/Users/Sherwin/Desktop/LOH_HRD/lable_result02/train/FALSE/F180015385BCD_180015384FD_lableResult_loh.tsv', sep='\t')
t8 = pd.read_csv('C:/Users/Sherwin/Desktop/LOH_HRD/lable_result02/train/FALSE/F180015810BCD_180015810FD_lableResult_loh.tsv', sep='\t')
t9 = pd.read_csv('C:/Users/Sherwin/Desktop/LOH_HRD/lable_result02/train/FALSE/F180016967BD_180016967FD_lableResult_loh.tsv', sep='\t')
t10 = pd.read_csv('C:/Users/Sherwin/Desktop/LOH_HRD/lable_result02/train/FALSE/F180017873BD_180017873TD_lableResult_loh.tsv', sep='\t')
t11 = pd.read_csv('C:/Users/Sherwin/Desktop/LOH_HRD/lable_result02/train/FALSE/F180018355BCD_180018362FD_lableResult_loh.tsv', sep='\t')
t12 = pd.read_csv('C:/Users/Sherwin/Desktop/LOH_HRD/lable_result02/train/FALSE/F180020310BD_180020310FD_lableResult_loh.tsv', sep='\t')
t13 = pd.read_csv('C:/Users/Sherwin/Desktop/LOH_HRD/lable_result02/train/FALSE/F180020316BD_180020316FD_lableResult_loh.tsv', sep='\t')
t14 = pd.read_csv('C:/Users/Sherwin/Desktop/LOH_HRD/lable_result02/train/FALSE/F180020579BCD_180020579FD_lableResult_loh.tsv', sep='\t')
t15= pd.read_csv('C:/Users/Sherwin/Desktop/LOH_HRD/lable_result02/train/FALSE/F180020909BCD_180020908FDR1_lableResult_loh.tsv', sep='\t')



res=pd.concat([t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t11,t12,t13,t14,t15],axis=0)

res.to_csv('C:/Users/Sherwin/Desktop/LOH_HRD/lable_result02/train/false.tsv',index = False,sep='\t')
