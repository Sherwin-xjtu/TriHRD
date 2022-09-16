#!/usr/bin/python
# coding=utf-8
from __future__ import division
import pandas as pd


def pre_data(files):
    reader1 = pd.read_csv(files[0])
    reader2 = pd.read_csv(files[1])
    reader3 = pd.read_csv(files[2])
    reader4 = pd.read_csv(files[3])
    reader5 = pd.read_csv(files[4])
    reader6 = pd.read_csv(files[5])
    reader7 = pd.read_csv(files[6])
    reader8 = pd.read_csv(files[7])
    reader9 = pd.read_csv(files[8])
    reader10 = pd.read_csv(files[9])
    reader11 = pd.read_csv(files[10])
    reader12 = pd.read_csv(files[11])
    reader13 = pd.read_csv(files[12])
    reader14 = pd.read_csv(files[13])
    reader15 = pd.read_csv(files[14])
    reader16 = pd.read_csv(files[15])
    reader17 = pd.read_csv(files[16])
    reader18 = pd.read_csv(files[17])

    rd1 = reader1
    rd1 = rd1[rd1['type'] == 0]
    rd2 = reader2
    rd2 = rd2[rd2['type'] == 0]
    rd3 = reader3
    rd3 = rd3[rd3['type'] == 0]
    rd4 = reader4
    rd4 = rd4[rd4['type'] == 0]
    rd5 = reader5
    rd5 = rd5[rd5['type'] == 0]
    rd6 = reader6
    rd6 = rd6[rd6['type'] == 0]
    rd7 = reader7
    rd7 = rd7[rd7['type'] == 0]
    rd8 = reader8
    rd8 = rd8[rd8['type'] == 0]
    rd9 = reader9
    rd9 = rd9[rd9['type'] == 0]
    rd10 = reader10
    rd10 = rd10[rd10['type'] == 0]
    rd11 = reader11
    rd11 = rd11[rd11['type'] == 0]
    rd12 = reader12
    rd12 = rd12[rd12['type'] == 0]
    rd13 = reader13
    rd13 = rd13[rd13['type'] == 0]
    rd14 = reader14
    rd14 = rd14[rd14['type'] == 0]
    rd15 = reader15
    rd15 = rd15[rd15['type'] == 0]
    rd16 = reader16
    rd16 = rd16[rd16['type'] == 0]
    rd17 = reader17
    rd17 = rd17[rd17['type'] == 0]
    rd18 = reader18
    rd18 = rd18[rd18['type'] == 0]

    alldata = pd.concat([rd1, rd2,rd3,rd4,rd5,rd6,rd7,rd8,rd9,rd10,rd11, rd12,rd13,rd14,rd15,rd16,rd17,rd18], axis=0, ignore_index=True)
    alldata.to_csv('C:/Users/Sherwin/Desktop/luo/new/test2/out.alldata.csv', index=False)
    dd = alldata[alldata['CHROM'].duplicated(keep='first')]
    dd = dd[dd['POS'].duplicated(keep='first')]
    dd = dd[dd['REF'].duplicated(keep='first')]
    dd= dd[dd['ALT'].duplicated(keep='first')]
    dd.to_csv('C:/Users/Sherwin/Desktop/luo/new/test2/common.csv', index=False)
    # print alldata[alldata['POS'].duplicated(keep='first')],alldata



    # rd = rd[rd['BRF'] < 0.2]//
    # rd= rd[rd['HP'] < 11]//
    # rd = rd[rd['GQ'] > 62]//
    # rd = rd[rd['GOF'] < 19]
    # rd = rd[rd['MGOF'] < 19]//
    # rd = rd[rd['QD'] < 24]
    # rd = rd[rd['TCR'] < 806]//
    # rd = rd[rd['TCF'] < 742]//
    # rd = rd[rd['TC'] < 1500]
    # rd = rd[rd['MMLQ'] > 23]
    # rd = rd[rd['WE'] < 2.5e8]
    # rd = rd[rd['WS'] < 1.9e8]
    # rd = rd[rd['MQ'] > 25]pp
    # rd = rd[rd['HapScore'] < 3]pp
    # rd = rd[rd['SbPval'] > 0.27]pp
    # rd = rd[rd['VAFN'] <0.013]pp
    # rd = rd[rd['VAFC'] < 0.01]
    # rd = rd[rd['ACN'] < 3.5]pp
    # rd = rd[rd['AF'] > 2.1e-3]
    # rd = rd[rd['SBR'] > -0.61]
    # # rd = rd[rd['NV'] < 200]
    # rdS = rd[rd['FILTER'] == '[]']
    # # ds_t = rd.drop(rdS.index.values)
    # tv = rd[rd['type'] == 1]
    # rdS = rdS[rdS['AF'] < 0.05]
    # rdS = rdS[rdS['AF'] > 0.00065]
    # # rdS = rdS[rdS['AF'] > 0.0005]
    # # rdS = rdS[rdS['DP'] < 4500]
    # # rdS = rdS[rdS['MQ'] > 52]
    # # rdS = rdS[rdS['SBF'] > 1.0e-3]
    # # rdS = rdS[rdS['HIAF'] > 3.5e-4]
    # # rdS = rdS[rdS['HICOV'] > 315]
    # # rdS = rdS[rdS['HICOV'] < 4460]
    # # rdS = rdS[rdS['VD'] < 4]
    # rdS = rdS[rdS['VD'] > 3]
    # ds = rdS[rdS['type'] == 1]
    # rdS = rdS[rdS['altbiasl'] != 0]
    # rdS = rdS[rdS['altbiasr'] != 0]
    # # rdS = rdS[rdS['SBR'] > - 0.978]
    # ds_all = rdS
    # ps = rdS[rdS['type'] == 1]
    # ds_t = rdS.drop(ps.index.values)
    # ds_t.to_csv('C:/Users/Sherwin/Desktop/luo/new/out.208001984fD_AF10-50ng.c1m4g1.csv', index=False)
    # ds_all.to_csv('C:/Users/Sherwin/Desktop/luo/new/out.208001984fD_AF10-50ng.c1m4g1_all.csv', index=False)
    # print ds_all['type'].size,ds['type'].size,ps['type'].size,tv['type'].size,ps['type'].size/tv['type'].size,ps['type'].size/ds_all['type'].size
def pre_data_all(files):
    reader1 = pd.read_csv(files[0])
    reader2 = pd.read_csv(files[1])
    reader3 = pd.read_csv(files[2])
    reader4 = pd.read_csv(files[3])
    reader5 = pd.read_csv(files[4])
    reader6 = pd.read_csv(files[5])
    reader7 = pd.read_csv(files[6])
    reader8 = pd.read_csv(files[7])
    reader9 = pd.read_csv(files[8])
    reader10 = pd.read_csv(files[9])
    reader11 = pd.read_csv(files[10])
    reader12 = pd.read_csv(files[11])
    reader13 = pd.read_csv(files[12])
    reader14 = pd.read_csv(files[13])
    reader15 = pd.read_csv(files[14])
    reader16 = pd.read_csv(files[15])
    reader17 = pd.read_csv(files[16])
    reader18 = pd.read_csv(files[17])

    rd1 = reader1
    # rd1 = rd1[rd1['type'] == 0]
    rd2 = reader2
    # rd2 = rd2[rd2['type'] == 0]
    rd3 = reader3
    # rd3 = rd3[rd3['type'] == 0]
    rd4 = reader4
    # rd4 = rd4[rd4['type'] == 0]
    rd5 = reader5
    # rd5 = rd5[rd5['type'] == 0]
    rd6 = reader6
    # rd6 = rd6[rd6['type'] == 0]
    rd7 = reader7
    # rd7 = rd7[rd7['type'] == 0]
    rd8 = reader8
    # rd8 = rd8[rd8['type'] == 0]
    rd9 = reader9
    # rd9 = rd9[rd9['type'] == 0]
    rd10 = reader10
    # rd10 = rd10[rd10['type'] == 0]
    rd11 = reader11
    # rd11 = rd11[rd11['type'] == 0]
    rd12 = reader12
    # rd12 = rd12[rd12['type'] == 0]
    rd13 = reader13
    # rd13 = rd13[rd13['type'] == 0]
    rd14 = reader14
    # rd14 = rd14[rd14['type'] == 0]
    rd15 = reader15
    # rd15 = rd15[rd15['type'] == 0]
    rd16 = reader16
    # rd16 = rd16[rd16['type'] == 0]
    rd17 = reader17
    # rd17 = rd17[rd17['type'] == 0]
    rd18 = reader18
    # rd18 = rd18[rd18['type'] == 0]

    alldata = pd.concat([rd1, rd2,rd3,rd4,rd5,rd6,rd7,rd8,rd9,rd10,rd11, rd12,rd13,rd14,rd15,rd16,rd17,rd18], axis=0, ignore_index=True)
    alldata.to_csv('C:/Users/Sherwin/Desktop/luo/new/test2/alldata.csv', index=False)

def black_list(files):
    reader1 = pd.read_csv(files[0])
    reader2 = pd.read_csv(files[1])
    reader3 = pd.read_csv(files[2])
    reader4 = pd.read_csv(files[3])
    reader5 = pd.read_csv(files[4])
    reader6 = pd.read_csv(files[5])
    rd1 = reader1
    # rd1 = rd1[rd1['type'] == 0]
    rd2 = reader2
    # rd2 = rd2[rd2['type'] == 0]
    rd3 = reader3
    # rd3 = rd3[rd3['type'] == 0]
    rd4 = reader4
    rd5 = reader5
    rd6 = reader6

    alldata = pd.concat([rd1, rd2, rd3, rd4, rd5, rd6], axis=0,ignore_index=True)
    alldata.to_csv('C:/Users/Sherwin/Desktop/luo/01.sscs_c1m3g0.result/black.csv', index=False)



if __name__ == '__main__':

    file1 = 'C:/Users/Sherwin/Desktop/luo/new/test2/208001985fD_AF10-20ng.c1m4g1.csv'
    file2 = 'C:/Users/Sherwin/Desktop/luo/new/test2/208001985fD_AF10-20ng.c1m8g3.csv'
    file3 = 'C:/Users/Sherwin/Desktop/luo/new/test2/208001988fD_AF05-20ng.c1m4g1.csv'
    file4 = 'C:/Users/Sherwin/Desktop/luo/new/test2/208001988fD_AF05-20ng.c1m8g3.csv'
    file5 = 'C:/Users/Sherwin/Desktop/luo/new/test2/208001989fD_AF05-20ng.c1m4g1.csv'
    file6 = 'C:/Users/Sherwin/Desktop/luo/new/test2/208001989fD_AF05-20ng.c1m8g3.csv'
    file7 = 'C:/Users/Sherwin/Desktop/luo/new/test2/208001992fD_AF01-50ng.c1m4g1.csv'
    file8 = 'C:/Users/Sherwin/Desktop/luo/new/test2/208001992fD_AF01-50ng.c1m8g3.csv'
    file9 = 'C:/Users/Sherwin/Desktop/luo/new/test2/208001993fD_AF01-50ng.c1m4g1.csv'
    file10 = 'C:/Users/Sherwin/Desktop/luo/new/test2/208001993fD_AF01-50ng.c1m8g3.csv'
    file11 = 'C:/Users/Sherwin/Desktop/luo/new/test2/208001994fD_AF01-20ng.c1m4g1.csv'
    file12 = 'C:/Users/Sherwin/Desktop/luo/new/test2/208001994fD_AF01-20ng.c1m8g3.csv'
    file13 = 'C:/Users/Sherwin/Desktop/luo/new/test2/208001995fD_AF01-20ng.c1m4g1.csv'
    file14 = 'C:/Users/Sherwin/Desktop/luo/new/test2/208001995fD_AF01-20ng.c1m8g3.csv'
    file15 = 'C:/Users/Sherwin/Desktop/luo/new/test2/208001998fD_AF00-50ng.c1m4g1.csv'
    file16 = 'C:/Users/Sherwin/Desktop/luo/new/test2/208001998fD_AF00-50ng.c1m8g3.csv'
    file17 = 'C:/Users/Sherwin/Desktop/luo/new/test2/208001999fD_AF00-20ng.c1m4g1.csv'
    file18 = 'C:/Users/Sherwin/Desktop/luo/new/test2/208001999fD_AF00-20ng.c1m8g3.csv'

    files = [file1,file2,file3,file4,file5,file6,file7,file8,file9,file10,file11,file12,file13,file14,file15,file16,file17,file18]
    # pre_data_all(files)

    file1_b = 'C:/Users/Sherwin/Desktop/luo/new/test2/208001998fD_AF00-50ng.c1m4g1.csv'
    file2_b = 'C:/Users/Sherwin/Desktop/luo/new/test2/208001998fD_AF00-50ng.c1m8g3.csv'
    file3_b = 'C:/Users/Sherwin/Desktop/luo/new/test2/208001999fD_AF00-20ng.c1m4g1.csv'
    file4_b = 'C:/Users/Sherwin/Desktop/luo/new/test2/208001999fD_AF00-20ng.c1m8g3.csv'
    file5_b = 'C:/Users/Sherwin/Desktop/luo/01.sscs_c1m3g0.result/208001998fD_AF00-50ng.c1m3g0.csv'
    file6_b = 'C:/Users/Sherwin/Desktop/luo/01.sscs_c1m3g0.result/208001999fD_AF00-20ng.c1m3g0.csv'
    files_b = [file1_b,file2_b,file3_b,file4_b,file5_b,file6_b]
    black_list(files_b)