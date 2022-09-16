#!/usr/bin/python
# coding=utf-8

import pysam
import argparse
import logging
import vcf
import pandas as pd
from numpy import *
# from log_config import Config
import csv, os, argparse, string, sys, multiprocessing, logging, functools, time, signal, re

sys.dont_write_bytecode = True
csv.register_dialect("line_terminator", lineterminator="\n")
VERSION = '1.0.1'


class Process_data:

    def __init__(self, args):
        self.data_vcf = args[0]
        self.labeled_path = args[1]
        self.Y_list = []
        self.list = []
        self.CHROM_list = []
        self.POS_list = []
        self.QUAL_list = []
        self.MQ_list = []
        self.QD_list = []
        self.FS_list = []
        self.AF_list = []
        self.CONTQ_list = []
        self.TLOD_list = []
        self.CONTQ_list = []
        self.TLOD_list = []
        self.DP_list = []
        self.REF_list = []
        self.ALT_list = []

    def processing_datas(self, vcf_in):
        for rec in vcf_in.fetch():
            POS = rec.pos
            QUAL = rec.qual
            chrom = rec.chrom
            REF = rec.ref
            ALT = rec.alts
            info_dict = rec.info
            filter = rec.filter
            DP = 0
            AF = 0
            CONTQ = 0
            TLOD = 0
            for key, value in rec.samples.iteritems():
                AF = value['AF']
                DP = value['DP']
            if 'CONTQ' in info_dict.keys():
                CONTQ = info_dict['CONTQ']

            if 'TLOD' in info_dict.keys():
                TLOD = info_dict['TLOD'][0]
            for key, value in filter.iteritems():
                if 'PASS' in key:
                    self.Y_list.append(1)
                    self.AF_list.append(AF[0])
                    self.DP_list.append(DP)
                    self.CHROM_list.append(chrom)
                    self.POS_list.append(POS)
                    self.CONTQ_list.append(CONTQ)
                    self.TLOD_list.append(TLOD)
                    self.REF_list.append(REF)
                    self.ALT_list.append(ALT)

    def processing(self):
        data_vcf = self.data_vcf
        labeled_path = self.labeled_path
        vcf_in = pysam.VariantFile(data_vcf)
        self.processing_datas(vcf_in)

        Y_list_str = map(str, self.Y_list)
        CHROM_list_str = map(str, self.CHROM_list)
        POS_list_str = map(str, self.POS_list)
        AF_list_str = map(str, self.AF_list)
        DP_list_str = map(str, self.DP_list)

        CONTQ_list_str = map(str, self.CONTQ_list)
        TLOD_list_str = map(str, self.TLOD_list)
        REF_list_str = map(str, self.REF_list)
        ALT_list_str = map(str, self.ALT_list)

        # 字典中的key值即为csv中列名
        dataframe_L = pd.DataFrame({'CHROM': CHROM_list_str,
                                    'POS': POS_list_str,
                                    'AF': AF_list_str,
                                    'DP': DP_list_str,
                                    'CONTQ': CONTQ_list_str,
                                    'TLOD': TLOD_list_str,
                                    'REF': REF_list_str,
                                    'ALT': ALT_list_str,
                                    'type': Y_list_str
                                    },
                                   columns=['CHROM', 'POS', 'AF', 'DP','CONTQ', 'TLOD', 'REF', 'ALT', 'type'])

        # 将DataFrame存储为csv,index表示是否显示行名，default=True
        dataframe_L.to_csv(labeled_path, index=False, sep=',')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--vcf', help='input vcf file', required=True)
    parser.add_argument('-o', '--out', help='output labeled csv file', required=True)
    parser.add_argument('-l', '--logging_file', help='the logging file', required=True)

    args = parser.parse_args()
    vcf_file = os.path.abspath(args.vcf)
    labeled_file = os.path.abspath(args.out)
    # log_file=os.path.abspath(args.logging_file)
    # conf = Config(log_file)
    # logger = conf.getLog()
    # logger.info("The program Version is %s",VERSION)
    # logger.info('\nprogram pre_data started in %s with command: %s', os.getcwd(), ' '.join(sys.argv))
    # logger.info('\n[ start time: %s]',time.asctime( time.localtime(time.time()) ))
    args_ = [vcf_file, labeled_file]
    process_data = Process_data(args_)
    process_data.processing()
    # logger.info('\n[ end time: %s]',time.asctime( time.localtime(time.time()) ))
