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

    def compvcf(self, mlt, record):
        a = 0
        c = 0
        d = 0
        filter_type = 0
        for record2 in mlt:
            # for record1 in record:
            if record.CHROM == record2.CHROM and record.POS == record2.POS:
                a = a + 1
                filter_type = 1
                return filter_type
        if filter_type == 0:
            return filter_type
    def processing_datas(self, vcf_in, m_vcf):

        n = 0
        mlt = ()
        sum_ls = []
        lk = []
        # p = p_thread
        for record2 in m_vcf:
            # if 'PASS' in record2.filter.keys():
            mlt = mlt + (record2,)
            n = n + 1

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

            GQ = rec.samples[0]['GQ']
            NR = rec.samples[0]['NR']
            NV = np.mean(rec.samples[0]['NV'])
            GOF = rec.samples[0]['GOF']

            BRF = info_dict['BRF']
            FR = info_dict['FR']
            HP = info_dict['HP']
            HapScore = info_dict['HapScore']
            MGOF = info_dict['MGOF']
            MMLQ = info_dict['MMLQ']
            MQ = info_dict['MQ']
            NF = info_dict['NF']
            PP = info_dict['PP']
            QD = info_dict['QD']
            SbPval = info_dict['SbPval']
            TC = info_dict['TC']
            TCF = info_dict['TCF']
            TCR = info_dict['TCR']
            TR = info_dict['TR']
            WE = info_dict['WE']
            WS = info_dict['WS']
            if 'FET' in info_dict:
                FET = info_dict['FET'][0]
            else:
                FET = 0
            if 'VAFN' in info_dict:
                VAFN = info_dict['VAFN']
            else:
                VAFN = 0
            if 'VAFC' in info_dict:
                VAFC = info_dict['VAFC']
            else:
                VAFC = 0
            if 'ACN' in info_dict:
                ACN = info_dict['ACN']
            else:
                ACN = 0

            self.BRF_list.append(BRF)
            self.FR_list.append(FR)
            self.CHROM_list.append(CHROM)
            self.POS_list.append(POS)
            self.QUAL_list.append(QUAL)
            self.HP_list.append(HP)
            self.HapScore_list.append(HapScore)
            self.REF_list.append(REF)
            self.ALT_list.append(ALT)
            self.MGOF_list.append(MGOF)
            self.MMLQ_list.append(MMLQ)
            self.MQ_list.append(MQ)
            self.NF_list.append(NF)
            self.PP_list.append(PP)
            self.QD_list.append(QD)
            self.SbPval_list.append(SbPval)
            self.TC_list.append(TC)
            self.TCF_list.append(TCF)
            self.TCR_list.append(TCR)
            self.TR_list.append(TR)
            self.WE_list.append(WE)
            self.WS_list.append(WS)
            self.FET_list.append(FET)
            self.VAFC_list.append(VAFC)
            self.ACN_list.append(ACN)
            self.VAFN_list.append(VAFN)
            self.FILTER_list.append(FILTER)
            self.GQ_list.append(GQ)
            self.NR_list.append(NR)
            self.NV_list.append(NV)
            self.GOF_list.append(GOF)

            if ID == None:
                self.ID_list.append('.')
            else:
                self.ID_list.append(ID)

            type_ = self.compvcf(mlt, rec)

            self.Y_list.append(type_)

    def processing(self):
        data_vcf = self.data_vcf
        m_vcf = self.m_vcf
        labeled_path = self.labeled_path
        vcf_in = vcf.Reader(open(data_vcf, 'rb'))
        m_vcf = vcf.Reader(open(m_vcf, 'rb'))
        self.processing_datas(vcf_in, m_vcf)
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
                                    'BRF': self.BRF_list,
                                    'FR': self.FR_list,
                                    'HP': self.HP_list,
                                    'HapScore': self.HapScore_list,
                                    'MGOF': self.MGOF_list,
                                    'MMLQ': self.MMLQ_list,
                                    'MQ': self.MQ_list,
                                    'PP': self.PP_list,
                                    'QD': self.QD_list,
                                    'SbPval': self.SbPval_list,
                                    'TC': self.TC_list,
                                    'TCF': self.TCF_list,
                                    'TCR': self.TCR_list,
                                    'TR': self.TR_list,
                                    'WE': self.WE_list,
                                    'WS': self.WS_list,
                                    'NF': self.NF_list,
                                    'NR': self.NR_list,
                                    'NV': self.NV_list,
                                    'GQ': self.GQ_list,
                                    'GOF': self.GOF_list,
                                    'FET': self.FET_list,
                                    'VAFN': self.VAFN_list,
                                    'VAFC': self.VAFC_list,
                                    'ACN': self.ACN_list,
                                    'FILTER': self.FILTER_list,
                                    'type': self.Y_list
                                    },
                                   columns=['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'BRF', 'FR', 'HP', 'HapScore',
                                            'MGOF', 'MMLQ', 'MQ', 'PP', 'QD', 'SbPval', 'TC', 'TCF', 'TCR', 'TR', 'WE',
                                            'WS',
                                            'NF', 'NR', 'NV', 'GQ', 'GOF', 'FET', 'VAFN', 'VAFC', 'ACN', 'FILTER',
                                            'type'])

        # 将DataFrame存储为csv,index表示是否显示行名，default=True
        dataframe_L.to_csv(labeled_path, index=False, sep=',')



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--vcf', help='input vcf file', required=True)
    parser.add_argument('-k', '--knowns', help='input vcf file', required=True)
    parser.add_argument('-o', '--out', help='output labeled csv file', required=True)
    parser.add_argument('-l', '--logging_file', help='the logging file', required=True)

    # args = parser.parse_args()
    # vcf_file = os.path.abspath(args.vcf)
    # m_file = os.path.abspath(args.knowns)
    # labeled_file = os.path.abspath(args.out)

    vcf_file = 'C:/Users/Sherwin/Desktop/199007051D_199007052D/199007051D_199007052D_fisher_splited_new_merge.vcf.gz'
    m_file = 'C:/Users/Sherwin/Desktop/199007051D_199007052D/somatic_filtered_PASS.vcf'
    labeled_file = 'C:/Users/Sherwin/Desktop/199007051D_199007052D/199007051D_199007052D_fisher_splited_new_merge.csv'




    # log_file=os.path.abspath(args.logging_file)
    # conf = Config(log_file)
    # logger = conf.getLog()
    # logger.info("The program Version is %s",VERSION)
    # logger.info('\nprogram pre_data started in %s with command: %s', os.getcwd(), ' '.join(sys.argv))
    # logger.info('\n[ start time: %s]',time.asctime( time.localtime(time.time()) ))
    args_ = [vcf_file, m_file, labeled_file]
    process_data = Process_data(args_)
    process_data.processing()
    # logger.info('\n[ end time: %s]',time.asctime( time.localtime(time.time()) ))
