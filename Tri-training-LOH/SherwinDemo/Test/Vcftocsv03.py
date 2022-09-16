#!/usr/bin/python
# coding=utf-8

from __future__ import division  # 用于/相除的时候,保留真实结果.小数
# import pysam
import argparse
import logging
import vcf
# import pysam
import pandas as pd
import numpy as np
from numpy import *
# from log_config import Config
import csv, os, argparse, string, sys, multiprocessing, logging, functools, time, signal, re

sys.dont_write_bytecode = True
csv.register_dialect("line_terminator", lineterminator="\n")
VERSION = '1.0.1'


class Process_data:
    def __init__(self, args):
        self.data_vcf = args[0]
        self.m_vcf = args[1]
        self.labeled_path = args[2]
        self.Y_list = []
        self.CHROM_list = []
        self.POS_list = []
        self.REF_list = []
        self.ALT_list = []
        self.DP_list = []
        self.AF_list = []

    def compvcf(self, m_reader, record):
        filter_type = 0
        ts = record.POS in m_reader['POS'].values
        if ts:
            print record.POS
            a = m_reader[(m_reader.POS == record.POS )].index
            c = a.values[0]
            CHROM = str(m_reader.iloc[c].CHROM)
            if m_reader.iloc[c].REF == record.REF and CHROM == record.CHROM:
                filter_type = 1
                # print record,m_reader.iloc[c]
                return filter_type
                # for altv in record.ALT:
                #     altvs = altv.sequence
                #     print altvs,m_reader.iloc[c].ALT
                #
                #     if altvs in (m_reader.iloc[c]).ALT:
                #
                #         filter_type = 1
                #         return filter_type
                #     else:
                #         return filter_type
            else:
                return filter_type
        else:
            return filter_type

    def processing_datas(self, vcf_in,m_reader):
        for rec in vcf_in:
            POS = rec.POS
            CHROM = rec.CHROM
            REF = rec.REF
            ALT = rec.ALT
            self.CHROM_list.append(CHROM)
            self.POS_list.append(POS)
            self.REF_list.append(REF)
            self.ALT_list.append(ALT)
            type_ = self.compvcf(m_reader,rec)
            self.Y_list.append(type_)


    def processing(self):
        data_vcf = self.data_vcf
        m_vcf = self.m_vcf
        labeled_path = self.labeled_path
        vcf_in = vcf.Reader(open(data_vcf, 'r'))
        m_reader = pd.read_csv(m_vcf)
        self.processing_datas(vcf_in,m_reader)
        CHROM_list_str = map(str, self.CHROM_list)
        REF_list_str = map(str, self.REF_list)
        ALT_list_str = map(str, self.ALT_list)
        dataframe_L = pd.DataFrame({'CHROM': CHROM_list_str,
                                    'POS': self.POS_list,
                                    'REF': REF_list_str,
                                    'ALT': ALT_list_str,
                                    'type': self.Y_list
                                    },
                                   columns=['CHROM', 'POS', 'REF', 'ALT',  'type'])
        dataframe_L.to_csv(labeled_path, index=False, sep=',')

if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # parser.add_argument('-v', '--vcf', help='input vcf file', required=True)
    # parser.add_argument('-k', '--knowns', help='input csv file', required=True)
    # parser.add_argument('-o', '--out', help='output labeled csv file', required=True)
    #
    # args = parser.parse_args()
    # vcf_file = os.path.abspath(args.vcf)
    # m_file = os.path.abspath(args.knowns)
    # labeled_file = os.path.abspath(args.out)

    vcf_file = 'C:/Users/Sherwin/Desktop/TMB/somatic_raw.vcf'
    m_file = 'C:/Users/Sherwin/Desktop/TMB/Reference.csv'
    labeled_file = 'C:/Users/Sherwin/Desktop/TMB/label.csv'
    args_ = [vcf_file,m_file, labeled_file]
    process_data = Process_data(args_)
    process_data.processing()

