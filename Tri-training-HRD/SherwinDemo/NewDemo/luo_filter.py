#!/usr/bin/python
# coding=utf-8
from __future__ import division
import pandas as pd


def VD3(file,black):
    reader = pd.read_csv(file)
    br = pd.read_csv(black)

    rd = reader

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
    # rd = rd[rd['NV'] < 200]
    rdS = rd[rd['FILTER'] == '[]']
    # ds_t = rd.drop(rdS.index.values)
    tv = rd[rd['type'] == 1]
    rdS = rdS[rdS['AF'] < 0.05]
    # rdS = rdS[rdS['AF'] > 0.00065]
    rdS = rdS[rdS['AF'] > 0.0005]
    # rdS = rdS[rdS['DP'] < 4500]
    # rdS = rdS[rdS['MQ'] > 52]
    # rdS = rdS[rdS['SBF'] > 1.0e-3]
    # rdS = rdS[rdS['HIAF'] > 3.5e-4]
    # rdS = rdS[rdS['HICOV'] > 315]
    # rdS = rdS[rdS['HICOV'] < 4460]
    # rdS = rdS[rdS['VD'] < 4]
    rdS = rdS[rdS['VD'] > 3]
    ds = rdS[rdS['type'] == 1]
    rdS = rdS[rdS['altbiasl'] != 0]
    rdS = rdS[rdS['altbiasr'] != 0]
    # rdS = rdS[rdS['SBR'] > - 0.978]
    ds_all = rdS
    ds_allt = rdS[rdS['type'] == 0]
    r = 0
    for j, v in enumerate(ds_allt.values):
        for i, row in enumerate(br.values):
            # index = rd.index[i]
            if v[0] == row[0] and v[1] == row[1] and v[3] == row[3] and v[4] == row[4]:
                r = r+1
                print v, row
                break
    ps = rdS[rdS['type'] == 1]
    ds_t = rdS.drop(ps.index.values)
    ds_t.to_csv('C:/Users/Sherwin/Desktop/luo/new/test1/out.208001987fD_AF05-50ng.c1m8g3.csv', index=False)
    ds_all.to_csv('C:/Users/Sherwin/Desktop/luo/new/test1/out.208001987fD_AF05-50ng.c1m8g3_all.csv', index=False)
    n = ds_all['type'].size - r
    print n,ds_all['type'].size,ds['type'].size,ps['type'].size,tv['type'].size,ps['type'].size/tv['type'].size,ps['type'].size/n


def NoVD(file,black):
    reader = pd.read_csv(file)
    br = pd.read_csv(black)

    rd = reader

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
    # rd = rd[rd['NV'] < 200]
    rdS = rd[rd['FILTER'] == '[]']
    # ds_t = rd.drop(rdS.index.values)
    tv = rd[rd['type'] == 1]
    rdS = rdS[rdS['AF'] < 0.05]
    # rdS = rdS[rdS['AF'] > 0.00065]
    rdS = rdS[rdS['AF'] > 0.0005]
    rdS = rdS[rdS['DP'] < 4500]
    # rdS = rdS[rdS['MQ'] > 52]
    # rdS = rdS[rdS['SBF'] > 1.0e-3]
    # rdS = rdS[rdS['HIAF'] > 3.5e-4]
    rdS = rdS[rdS['HICOV'] > 305]
    rdS = rdS[rdS['HICOV'] < 3600]
    rdS = rdS[rdS['VD'] < 18]
    # rdS = rdS[rdS['VD'] > 3
    ds = rdS[rdS['type'] == 1]
    # rdS = rdS[rdS['altbiasl'] != 0]
    # rdS = rdS[rdS['altbiasr'] != 0]
    rdS = rdS[rdS['SBR'] > - 0.975]
    rdS = rdS[rdS['SBR'] < 0.47]
    ds_all = rdS
    ds_allt = rdS[rdS['type'] == 0]
    r = 0
    for j, v in enumerate(ds_allt.values):
        for i, row in enumerate(br.values):
            # index = rd.index[i]
            if v[0] == row[0] and v[1] == row[1] and v[3] == row[3] and v[4] == row[4]:
                r = r+1
                print v, row
                break
    ps = rdS[rdS['type'] == 1]
    ds_t = rdS.drop(ps.index.values)
    ds_t.to_csv('C:/Users/Sherwin/Desktop/luo/new/test2/out.208001992fD_AF01-50ng.c1m4g1.csv', index=False)
    ds_all.to_csv('C:/Users/Sherwin/Desktop/luo/new/test2/out.208001992fD_AF01-50ng.c1m4g1_all.csv', index=False)
    n = ds_all['type'].size - r
    print n,ds_all['type'].size,ds['type'].size,ps['type'].size,tv['type'].size,ps['type'].size/tv['type'].size,ps['type'].size/n


if __name__ == '__main__':
    file = 'C:/Users/Sherwin/Desktop/luo/new/test1/208001988fD_AF05-20ng.c1m4g1.csv'
    black = 'C:/Users/Sherwin/Desktop/luo/new/black1.csv'

    file_ = 'C:/Users/Sherwin/Desktop/luo/new/test2/208001992fD_AF01-50ng.c1m4g1.csv'
    black_ = 'C:/Users/Sherwin/Desktop/luo/new/test2/black.csv'


    # VD3(file,black_)

    NoVD(file_, black_)