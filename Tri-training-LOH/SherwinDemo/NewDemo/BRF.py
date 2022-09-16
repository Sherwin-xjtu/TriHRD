#!/usr/bin/python
# coding=utf-8
from __future__ import division
import pandas as pd


def pre_data(file_path):
    reader = pd.read_csv(file_path)

    rd  = reader
    a = rd[rd['type'] == 1]
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
    # rd = rd[rd['VAFC'] > 0.01]
    # rd = rd[rd['ACN'] < 3.5]pp
    rd = rd[rd['FET'] > 9.5]
    rd = rd[rd['NR'] > 0]
    rd = rd[rd['NF'] > 0]

    # rd = rd[rd['VAFC'] < 0.01]
    rd = rd[rd['NV'] > 4]
    # rdS = rd[rd['FILTER'] == '[]']
    # ds_t = rd.drop(rdS.index.values)
    rd = rd[rd['VAFC'] > 0.01]
    # rd = rd[rd['VAFC'] < 0.1]
    ps = rd[rd['type'] == 1]
    # ds_t = rd.drop(ps.index.values)
    rd.to_csv('C:/Users/Sherwin/Desktop/TrainSet/out.199007051D_199007052D_pair_sorted_split_duplicated_merge.csv', index=False)
    # rd.to_csv('C:/Users/Sherwin/Desktop/199007047D_199007048D/out.199007047D_199007048D_pair_sorted_split_duplicated_merge.csv',index=False)
    print a.size,rd.size,ps.size


if __name__ == '__main__':
    file_path = 'C:/Users/Sherwin/Desktop/TrainSet/199007051D_199007052D_pair_sorted_split_duplicated_merge.csv'
    pre_data(file_path)