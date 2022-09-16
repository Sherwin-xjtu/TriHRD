#!/usr/bin/python
# coding=utf-8

import pysam
import argparse
import logging
import vcf
import pandas as pd
from numpy import *
from log_config import Config
import csv,os,argparse,string,sys,multiprocessing,logging,functools,time,signal, re
sys.dont_write_bytecode = True
csv.register_dialect("line_terminator",lineterminator="\n")
VERSION='1.0.1'



class Process_data:

    def __init__(self,args):
        self.data_vcf = args[0]
        self.gvcf1 = args[1]
        self.gvcf2 = args[2]
        self.labeled_path = args[3]
        self.unlabeled_path = args[4]
        self.Y_list = []
        self.X_tp_CHROM_list = []
        self.X_tp_POS_list = []
        self.X_tp_QUAL_list = []
        self.X_tp_MQ_list = []
        self.X_tp_QD_list = []
        self.X_tp_FS_list = []
        self.X_tp_SOR_list = []
        self.X_tp_MQRankSum_list = []
        self.X_tp_ReadPosRankSum_list = []

        self.X_fp_CHROM_list = []
        self.X_fp_POS_list = []
        self.X_fp_QUAL_list = []
        self.X_fp_MQ_list = []
        self.X_tp_QD_list = []
        self.X_U_FS_list = []
        self.X_U_SOR_list = []
        self.X_U_MQRankSum_list = []
        self.X_U_ReadPosRankSum_list = []

    # 读取已标记数据并且分割训练集和测试集
    # def read_labeled(self):
    # ['__class__', '__delattr__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__',
    #  '__gt__', '__hash__', '__init__', '__le__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__',
    #  '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__',
    #  'alleles', 'alts', 'chrom', 'contig', 'copy', 'filter', 'format', 'header', 'id', 'info', 'pos', 'qual',
    #  'ref', 'rid', 'rlen', 'samples', 'start', 'stop', 'translate']
    def labeled_datas(self,record, vcf_in, ulable):
        GQ = record.samples['case']['GQ']
        POS = record.pos
        REF = record.ref
        ALTS = record.alts
        QUAL = record.qual
        chrom = record.chrom
        info_dict = record.info
        for rec in vcf_in.fetch(chrom, POS - 1, POS):
            if GQ >= 20:
                if rec.chrom == chrom and rec.ref == REF and set(ALTS).issubset(set(rec.alts)):
                    ulable = False
                    if 'PASS' in rec.filter.keys():
                        self.X_tp_CHROM_list.append(chrom)
                        self.X_tp_POS_list.append(POS)
                        self.X_tp_QUAL_list.append(QUAL)

                        if 'MQ' in info_dict.keys():
                            self.X_tp_MQ_list.append(info_dict['MQ'])
                        else:
                            self.X_tp_MQ_list.append(NaN)
                        if 'QD' in info_dict.keys():
                            self.X_tp_QD_list.append(info_dict['QD'])
                        else:
                            self.X_tp_QD_list.append(NaN)
                        if 'FS' in info_dict.keys():
                            self.X_tp_FS_list.append(info_dict['FS'])
                        else:
                            self.X_tp_FS_list.append(NaN)
                        if 'SOR' in info_dict.keys():
                            self.X_tp_SOR_list.append(info_dict['SOR'])
                        else:
                            self.X_tp_SOR_list.append(NaN)
                        if 'MQRankSum' in info_dict.keys():
                            self.X_tp_MQRankSum_list.append(info_dict['MQRankSum'])
                        else:
                            self.X_tp_MQRankSum_list.append(NaN)
                        if 'ReadPosRankSum' in info_dict.keys():
                            self.X_tp_ReadPosRankSum_list.append(info_dict['ReadPosRankSum'])
                        else:
                            self.X_tp_ReadPosRankSum_list.append(NaN)
                        self.Y_list.append(1)
                    else:
                        self.X_tp_CHROM_list.append(chrom)
                        self.X_tp_POS_list.append(POS)
                        self.X_tp_QUAL_list.append(QUAL)
                        if 'MQ' in info_dict.keys():
                            self.X_tp_MQ_list.append(info_dict['MQ'])
                        else:
                            self.X_tp_MQ_list.append(NaN)
                        if 'QD' in info_dict.keys():
                            self.X_tp_QD_list.append(info_dict['QD'])
                        else:
                            self.X_tp_QD_list.append(NaN)
                        if 'FS' in info_dict.keys():
                            self.X_tp_FS_list.append(info_dict['FS'])
                        else:
                            self.X_tp_FS_list.append(NaN)
                        if 'SOR' in info_dict.keys():
                            self.X_tp_SOR_list.append(info_dict['SOR'])
                        else:
                            self.X_tp_SOR_list.append(NaN)
                        if 'MQRankSum' in info_dict.keys():
                            self.X_tp_MQRankSum_list.append(info_dict['MQRankSum'])
                        else:
                            self.X_tp_MQRankSum_list.append(NaN)
                        if 'ReadPosRankSum' in info_dict.keys():
                            self.X_tp_ReadPosRankSum_list.append(info_dict['ReadPosRankSum'])
                        else:
                            self.X_tp_ReadPosRankSum_list.append(NaN)
                        self.Y_list.append(0)
            else:
                ulable = False
                self.X_tp_CHROM_list.append(chrom)
                self.X_tp_POS_list.append(POS)
                self.X_tp_QUAL_list.append(QUAL)
                if 'MQ' in info_dict.keys():
                    self.X_tp_MQ_list.append(info_dict['MQ'])
                else:
                    self.X_tp_MQ_list.append(NaN)
                if 'QD' in info_dict.keys():
                    self.X_tp_QD_list.append(info_dict['QD'])
                else:
                    self.X_tp_QD_list.append(NaN)
                if 'FS' in info_dict.keys():
                    self.X_tp_FS_list.append(info_dict['FS'])
                else:
                    self.X_tp_FS_list.append(NaN)
                if 'SOR' in info_dict.keys():
                    self.X_tp_SOR_list.append(info_dict['SOR'])
                else:
                    self.X_tp_SOR_list.append(NaN)
                if 'MQRankSum' in info_dict.keys():
                    self.X_tp_MQRankSum_list.append(info_dict['MQRankSum'])
                else:
                    self.X_tp_MQRankSum_list.append(NaN)
                if 'ReadPosRankSum' in info_dict.keys():
                    self.X_tp_ReadPosRankSum_list.append(info_dict['ReadPosRankSum'])
                else:
                    self.X_tp_ReadPosRankSum_list.append(NaN)
                self.Y_list.append(0)
        return ulable

    def processing(self):
        data_vcf = self.data_vcf
        gvcf1 = self.gvcf1
        gvcf2 = self.gvcf2
        labeled_path = self.labeled_path
        unlabeled_path = self.unlabeled_path
        vcf_in_raw = pysam.VariantFile(data_vcf)
        vcf_in1 = pysam.VariantFile(gvcf1)
        vcf_in2 = pysam.VariantFile(gvcf2)

        for record in vcf_in_raw.fetch():
            # GQ = record.samples['normal']['GQ']
            POS = record.pos
            REF = record.ref
            ALTS = record.alts
            QUAL = record.qual
            chrom = record.chrom
            info_dict = record.info
            ulable = True
            x_list = []

            if ulable:
                ulable = self.labeled_datas(record, vcf_in1, ulable)
            if ulable:
                ulable = self.labeled_datas(record, vcf_in2, ulable)

            # if ulable:
            # labeled_datas(record, vcf_in3,ulable)

            if ulable:
                self.X_fp_CHROM_list.append(chrom)
                self.X_fp_POS_list.append(POS)
                self.X_fp_QUAL_list.append(QUAL)
                if 'MQ' in info_dict.keys():
                    self.X_fp_MQ_list.append(info_dict['MQ'])
                else:
                    self.X_fp_MQ_list.append(NaN)
                if 'QD' in info_dict.keys():
                    self.X_tp_QD_list.append(info_dict['QD'])
                else:
                    self.X_tp_QD_list.append(NaN)
                if 'FS' in info_dict.keys():
                    self.X_U_FS_list.append(info_dict['FS'])
                else:
                    self.X_U_FS_list.append(NaN)
                if 'SOR' in info_dict.keys():
                    self.X_U_SOR_list.append(info_dict['SOR'])
                else:
                    self.X_U_SOR_list.append(NaN)
                if 'MQRankSum' in info_dict.keys():
                    self.X_U_MQRankSum_list.append(info_dict['MQRankSum'])
                else:
                    self.X_U_MQRankSum_list.append(NaN)
                if 'ReadPosRankSum' in info_dict.keys():
                    self.X_U_ReadPosRankSum_list.append(info_dict['ReadPosRankSum'])
                else:
                    self.X_U_ReadPosRankSum_list.append(NaN)

        Y_list_str = map(str, self.Y_list)
        X_tp_CHROM_list_str = map(str, self.X_tp_CHROM_list)
        X_tp_POS_list_str = map(str, self.X_tp_POS_list)
        X_tp_QUAL_list_str = map(str, self.X_tp_QUAL_list)
        X_tp_MQ_list_str = map(str, self.X_tp_MQ_list)
        X_tp_QD_list_str = map(str, self.X_tp_QD_list)
        X_tp_ReadPosRankSum_list_str = map(str, self.X_tp_ReadPosRankSum_list)
        X_tp_FS_list_str = map(str, self.X_tp_FS_list)
        X_tp_SOR_list_str = map(str, self.X_tp_SOR_list)
        X_tp_MQRankSum_list_str = map(str, self.X_tp_MQRankSum_list)

        X_fp_CHROM_list_str = map(str, self.X_fp_CHROM_list)
        X_fp_POS_list_str = map(str, self.X_fp_POS_list)
        X_fp_QUAL_list_str = map(str, self.X_fp_QUAL_list)
        X_fp_MQ_list_str = map(str, self.X_fp_MQ_list)
        X_tp_QD_list_str = map(str, self.X_tp_QD_list)
        X_U_ReadPosRankSum_list_str = map(str, self.X_U_ReadPosRankSum_list)
        X_U_FS_list_str = map(str, self.X_U_FS_list)
        X_U_SOR_list_str = map(str, self.X_U_SOR_list)
        X_U_MQRankSum_list_str = map(str, self.X_U_MQRankSum_list)

        # 字典中的key值即为csv中列名
        dataframe_U = pd.DataFrame({'CHROM': X_fp_CHROM_list_str,
                                    'POS': X_fp_POS_list_str,
                                    'QUAL': X_fp_QUAL_list_str,
                                    'MQ': X_fp_MQ_list_str,
                                    'QD': X_tp_QD_list_str,
                                    'ReadPosRankSum': X_U_ReadPosRankSum_list_str,
                                    'FS': X_U_FS_list_str,
                                    'MQRankSum': X_U_MQRankSum_list_str,
                                    'SOR': X_U_SOR_list_str,
                                    },
                                   columns=['CHROM', 'POS',  'QUAL','MQ', 'QD', 'ReadPosRankSum', 'FS', 'MQRankSum',
                                            'SOR'])

        # 将DataFrame存储为csv,index表示是否显示行名，default=True
        dataframe_U.to_csv(unlabeled_path, index=False,sep=',')

        # 字典中的key值即为csv中列名
        dataframe_L = pd.DataFrame({'CHROM': X_tp_CHROM_list_str,
                                    'POS': X_tp_POS_list_str,
                                    'QUAL': X_tp_QUAL_list_str,
                                    'MQ': X_tp_MQ_list_str,
                                    'QD': X_tp_QD_list_str,
                                    'ReadPosRankSum': X_tp_ReadPosRankSum_list_str,
                                    'FS': X_tp_FS_list_str,
                                    'MQRankSum': X_tp_MQRankSum_list_str,
                                    'SOR': X_tp_SOR_list_str,
                                    'type': Y_list_str
                                    },
                                   columns=['CHROM', 'POS','QUAL', 'MQ', 'QD', 'ReadPosRankSum', 'FS', 'MQRankSum',
                                            'SOR',
                                            'type'])

        # 将DataFrame存储为csv,index表示是否显示行名，default=True
        dataframe_L.to_csv(labeled_path, index=False,sep=',')


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-v','--vcf',help='input vcf file',required=True)
    parser.add_argument('-k1', '--knowns1', help='input the truth sites vcf files', required=True)
    parser.add_argument('-k2', '--knowns2', help='input the truth sites vcf files', required=True)
    parser.add_argument('-ol', '--outl', help='output labeled vcf file',required=True)
    parser.add_argument('-ou', '--outu', help='output unlabled vcf file', required=True)
    parser.add_argument('-l', '--logging_file', help='the logging file',required=True)

    args = parser.parse_args()
    vcf_file = os.path.abspath(args.vcf)
    knowns_file1 = os.path.abspath(args.knowns1)
    knowns_file2 = os.path.abspath(args.knowns2)
    labeled_file=os.path.abspath(args.out1)
    unlabeled_file=os.path.abspath(args.outu)
    log_file=os.path.abspath(args.logging_file)
    # f=logging.Formatter('[%(levelname)s %(processName)s %(asctime)s %(funcName)s] %(message)s')
    # h=logging.FileHandler(log_file, 'w')
    # h.setFormatter(f)
    # logger=multiprocessing.get_logger()
    # logger.addHandler(h)
    # logger.setLevel(logging.INFO)
    conf = Config(log_file)
    logger = conf.getLog()
    logger.info("The program Version is %s",VERSION)
    logger.info('\nprogram pre_data started in %s with command: %s', os.getcwd(), ' '.join(sys.argv))
    # logger.info('\n[ the number of process is  %s]',pro_num)
    logger.info('\n[ start time: %s]',time.asctime( time.localtime(time.time()) ))
    args_ = [vcf_file,knowns_file1,knowns_file2,labeled_file,unlabeled_file]
    process_data = Process_data(args_)
    process_data.processing()
    logger.info('\n[ end time: %s]',time.asctime( time.localtime(time.time()) ))