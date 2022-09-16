# coding=utf-8

from __future__ import division  # 用于/相除的时候,保留真实结果.小数
# import pysam
import argparse
import gzip
import logging
import vcf
# import pysam
import pandas as pd
import numpy as np
from numpy import *
import tabix
# from log_config import Config
import csv, os, argparse, string, sys, multiprocessing, logging, functools, time, signal, re

sys.dont_write_bytecode = True
csv.register_dialect("line_terminator", lineterminator="\n")
VERSION = '1.0.1'


class Process_data:
    def __init__(self, args):
        self.data_vcf = args[0]
        self.m_vcf = args[1]
       # self.labeled_path = args[2]
        self.Y_list = []
        self.CHROM_list = []
        self.POS_list = []
        self.QUAL_list = []
        self.MQ_list = []
        self.QD_list = []
        self.BRF_list = []
        self.FR_list = []
        self.HP_list = []
        self.HapScore_list = []
        self.MGOF_list = []
        self.NF_list = []
        self.NR_list = []
        self.PP_list = []
        self.SC_list = []
        self.SbPval_list = []
        self.TC_list = []
        self.TCF_list = []
        self.TCR_list = []
        self.TR_list = []
        self.WE_list = []
        self.WS_list = []
        self.NV_list = []
        self.GQ_list = []
        self.ID_list = []
        self.REF_list = []
        self.ALT_list = []
        self.MMLQ_list = []
        self.GOF_list = []
        self.FET_list = []
        self.VAFN_list = []
        self.VAFC_list = []
        self.ACN_list = []
        self.FILTER_list = []

    def compvcf(self, mlt, record):
        a = 0
        filter_type = 0
        for record2 in mlt:
            if record.CHROM == record2.CHROM and record.POS == record2.POS:
                a = a + 1
                filter_type = 1
                return filter_type
        if filter_type == 0:
            return filter_type
    def processing_datas(self, vcf_in, m_vcf):
        j = 0
        n = 0
        for record in vcf_in:
            print record.CHROM, record.POS, record.POS +1
        #
        #     records = m_vcf.query(record.CHROM, record.POS, record.POS +1)
        #     for rec in records:
        #         rec_ref = rec[3]
        #         rec_alts = rec[4].split(',')
        #         for alt in record.ALT:
        #             alt_seq = alt.sequence
        #             if alt_seq in rec_alts and rec_ref == record.REF:
        #                 j = j+1
        # print j
    def processing(self):
        data_vcf = self.data_vcf
        m_vcf = self.m_vcf
     #   labeled_path = self.labeled_path
        vcf_in = vcf.Reader(open(data_vcf, 'rb'))
        #m_vcf = vcf.Reader(open(m_vcf, 'rb'))
        m_vcf = tabix.open(m_vcf)
        self.processing_datas(vcf_in, m_vcf)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--vcf', help='input vcf file', required=True)
    parser.add_argument('-k', '--knowns', help='input vcf file', required=True)
    parser.add_argument('-o', '--out', help='output labeled csv file', required=False)
    parser.add_argument('-l', '--logging_file', help='the logging file', required=False)

    args = parser.parse_args()
    vcf_file = os.path.abspath(args.vcf)
    m_file = os.path.abspath(args.knowns)
    
    # log_file=os.path.abspath(args.logging_file)
    # conf = Config(log_file)
    # logger = conf.getLog()
    # logger.info("The program Version is %s",VERSION)
    # logger.info('\nprogram pre_data started in %s with command: %s', os.getcwd(), ' '.join(sys.argv))
    # logger.info('\n[ start time: %s]',time.asctime( time.localtime(time.time()) ))
    args_ = [vcf_file, m_file]
    process_data = Process_data(args_)
    process_data.processing()
    # logger.info('\n[ end time: %s]',time.asctime( time.localtime(time.time()) ))
