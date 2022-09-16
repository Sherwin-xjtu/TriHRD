#!/usr/bin/python
# coding=utf-8

from __future__ import division  # 用于/相除的时候,保留真实结果.小数
# import pysam
import argparse
import logging
import vcf
import pysam
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

        self.DP_list = []
        self.VD_list = []
        self.AF_list = []
        self.PMEAN_list = []
        self.PSTD_list = []
        self.QUAL_list = []
        self.QSTD_list = []
        self.SBF_list = []
        self.ODDRATIO_list = []
        self.MQ_list = []
        self.SN_list = []
        self.HIAF_list = []
        self.ADJAF_list = []
        self.SHIFT3_list = []
        self.MSI_list = []
        self.MSILEN_list = []
        self.NM_list = []
        self.HICNT_list = []
        self.HICOV_list = []
        self.DUPRATE_list = []
        self.SPLITREAD_list = []
        self.SPANPAIR_list = []

        self.MIN_DP = 30
        self.MIN_GDP = 30  # min germline depth
        self.MIN_MMQ = 45
        self.MIN_MBQ = 20
        self.MIN_SEQQ = 30
        self.MIN_CONTQ = 35
        self.MIN_STRANDQ = 40
        self.MIN_GERMQ = 5
        self.MAX_ECNT = 2
        self.MIN_MPOS = 10
        self.MAX_IDL = 15
        self.MAX_DP = 1000
        self.MAX_MFRL1 = 250
        self.MAX_MFRL2 = 260
        self.MIN_TLOD = 10
        self.MIN_SBR = -0.25
        self.MIN_SEQQ_HOT = 5
        self.MIN_FR_HOT = 2
        self.MIN_FRS_HOT = 10
        # paired call filters
        self.MIN_PAIR_SEQQ = 20
        self.MIN_PAIR_CONTQ = 27
        self.MIN_PAIR_STRANDQ = 20
        self.MIN_STRANDQ_AF = 0.05
        self.GENDER_THRESHOLD = 0.09
        # filters for GAF
        self.MAX_GERMQ = 93  # M2 default
        self.MIN_GERM_FR = 5
        # germline range for autosomes
        self.MIN_GAF = 0.1
        self.MAX_GAF = 0.9
        self.GAF_THRESHOLD = 0.1
        self.PON_THRESHOLD = 2
        # AF range for somatic mutations in paired call
        self.MAX_SAF = 0.95
        self.MIN_SAF = 0.01
        self.WRN_LDP = 500
        self.UP = 0
        self.DOWN = 1
        self.SINGLE = 0
        self.PAIRED = 1
        self.p_ARM = 1
        self.q_ARM = 0
        self.EXPAR = 1
        self.TRUNK = 1024
        self.FLANK = 5e+7
        self.SIGPV = 5
        self.POWER = 2
        self.BAFIDX = 2.59
        self.AFADJ = 0.6744897501960817

    def compvcf(self, m_reader, record):
        filter_type = 0
        ts = record.POS in m_reader['POS'].values
        if ts:
            a = m_reader[(m_reader.POS == record.POS )].index
            c = a.values[0]
            CHROM = str(m_reader.iloc[c]).CHROM
            if m_reader.iloc[c].REF == record.REF and CHROM == record.CHROM:
                for altv in record.ALT:
                    altvs = altv.sequence
                    if (m_reader.iloc[c]).ALT == altvs:
                        filter_type = 1
                        return filter_type
                    else:
                        return filter_type
            else:
                return filter_type
        else:
            return filter_type

    def processing_datas(self, vcf_in,m_reader):

        n = 0
        mlt = ()
        sum_ls = []
        lk = []
        for rec in vcf_in:
            POS = rec.POS
            QUAL = rec.QUAL
            CHROM = rec.CHROM
            REF = rec.REF
            ALT = rec.ALT
            info_dict = rec.INFO
            FILTER = rec.FILTER
            DP = 0
            BRF = 0
            FR = []
            HP = 0
            HapScore = 0
            MGOF = 0
            MMLQ = 0
            MQ = 0
            NF = []
            NR = []
            PP = []
            QD = 0
            SbPval = 0
            TC = 0
            TCF = 0
            TCR = 0
            TR = []
            WE = 0
            WS = 0
            ID = rec.ID
            self.DP_list.append(info_dict['DP'])
            self.VD_list.append(info_dict['VD'])
            self.AF_list.append(info_dict['AF'])
            self.PMEAN_list.append(info_dict['PMEAN'])
            self.PSTD_list.append(info_dict['PSTD'])
            self.QUAL_list.append(info_dict['QUAL'])
            self.QSTD_list.append(info_dict['QSTD'])
            self.SBF_list.append(info_dict['SBF'])
            self.ODDRATIO_list.append(info_dict['ODDRATIO'])
            self.MQ_list.append(info_dict['MQ'])
            self.SN_list.append(info_dict['SN'])
            self.HIAF_list.append(info_dict['HIAF'])
            self.ADJAF_list.append(info_dict['ADJAF'])
            self.MSILEN_list.append(info_dict['MSILEN'])
            self.NM_list.append(info_dict['NM'])
            self.HICNT_list.append(info_dict['HICNT'])
            self.HICOV_list.append(info_dict['HICOV'])
            self.DUPRATE_list.append(info_dict['DUPRATE'])
            self.SPLITREAD_list.append(info_dict['SPLITREAD'])
            self.SPANPAIR_list.append(info_dict['SPANPAIR'])
            if ID == None:
                self.ID_list.append('.')
            else:
                self.ID_list.append(ID)
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
        ID_list_str = map(str, self.ID_list)

        dataframe_L = pd.DataFrame({'CHROM': CHROM_list_str,
                                    'POS': self.POS_list,
                                    'ID': ID_list_str,
                                    'REF': REF_list_str,
                                    'ALT': ALT_list_str,
                                    'QUAL': self.QUAL_list,
                                    'DP': self.DP_list,
                                    'AF': self.AF_list,
                                    'PMEAN': self.PMEAN_list,
                                    'PSTD': self.PSTD_list,
                                    'QSTD': self.QSTD_list,
                                    'SBF': self.SBF_list,
                                    'ODDRATIO': self.ODDRATIO_list,
                                    'MQ': self.MQ_list,
                                    'SN': self.SN_list,
                                    'HIAF': self.HIAF_list,
                                    'ADJAF': self.ADJAF_list,
                                    'MSILEN': self.MSILEN_list,
                                    'NM': self.NM_list,
                                    'HICNT': self.HICNT_list,
                                    'HICOV': self.HICOV_list,
                                    'DUPRATE': self.DUPRATE_list,
                                    'SPLITREAD': self.SPLITREAD_list,
                                    'SPANPAIR': self.SPANPAIR_list,
                                    'FILTER': self.FILTER_list,
                                    'type': self.Y_list
                                    },
                                   columns=['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'DP', 'AF', 'PMEAN', 'PSTD','QSTD', 'SBF',
                                            'ODDRATIO', 'MQ', 'SN', 'HIAF','ADJAF', 'MSILEN', 'NM', 'HICNT', 'HICOV', 'DUPRATE','SPLITREAD', 'SPANPAIR', 'FILTER', 'type'])
        dataframe_L.to_csv(labeled_path, index=False, sep=',')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--vcf', help='input vcf file', required=True)
    parser.add_argument('-k', '--knowns', help='input vcf file', required=True)
    parser.add_argument('-o', '--out', help='output labeled csv file', required=True)
    parser.add_argument('-l', '--logging_file', help='the logging file', required=True)

    args = parser.parse_args()
    vcf_file = os.path.abspath(args.vcf)
    m_file = os.path.abspath(args.knowns)
    labeled_file = os.path.abspath(args.out)
    args_ = [vcf_file,m_file, labeled_file]
    process_data = Process_data(args_)
    process_data.processing()

