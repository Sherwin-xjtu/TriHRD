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
        self.tp_vcf = args[0]
        self.fp_vcf = args[1]
        self.tp_out = args[2]
        self.fp_out = args[3]
        # self.unlabeled_path = args[4]
        self.Y_tp_list = []
        self.X_tp_CHROM_list = []
        self.X_tp_POS_list = []
        self.X_tp_QUAL_list = []
        self.X_tp_MQ_list = []
        self.X_tp_QD_list = []
        self.X_tp_FS_list = []
        self.X_tp_MQRankSum_list = []
        self.X_tp_ReadPosRankSum_list = []
        self.X_tp_AF_list = []
        self.X_tp_AC_list = []
        self.X_tp_HaplotypeScore_list = []
        self.X_tp_BaseQRankSum_list = []

        self.Y_fp_list = []
        self.X_fp_CHROM_list = []
        self.X_fp_POS_list = []
        self.X_fp_QUAL_list = []
        self.X_fp_MQ_list = []
        self.X_fp_QD_list = []
        self.X_fp_FS_list = []
        # self.X_fp_SOR_list = []
        self.X_fp_MQRankSum_list = []
        self.X_fp_ReadPosRankSum_list = []
        self.X_fp_AF_list = []
        self.X_fp_AC_list = []
        self.X_fp_HaplotypeScore_list = []
        self.X_fp_BaseQRankSum_list = []

    # 读取已标记数据并且分割训练集和测试集
    # def read_labeled(self):
    # ['__class__', '__delattr__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__',
    #  '__gt__', '__hash__', '__init__', '__le__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__',
    #  '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__',
    #  'alleles', 'alts', 'chrom', 'contig', 'copy', 'filter', 'format', 'header', 'id', 'info', 'pos', 'qual',
    #  'ref', 'rid', 'rlen', 'samples', 'start', 'stop', 'translate']
    def processing_tp_datas(self, vcf_in, tag):
        for rec in vcf_in.fetch():
            POS = rec.pos
            QUAL = rec.qual
            chrom = rec.chrom
            info_dict = rec.info
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
            # if 'SOR' in info_dict.keys():
            #     self.X_tp_SOR_list.append(info_dict['SOR'])
            # else:
            #     self.X_tp_SOR_list.append(NaN)
            if 'MQRankSum' in info_dict.keys():
                self.X_tp_MQRankSum_list.append(info_dict['MQRankSum'])
            else:
                self.X_tp_MQRankSum_list.append(NaN)
            if 'ReadPosRankSum' in info_dict.keys():
                self.X_tp_ReadPosRankSum_list.append(info_dict['ReadPosRankSum'])
            else:
                self.X_tp_ReadPosRankSum_list.append(NaN)
            if 'AF' in info_dict.keys():
                self.X_tp_AF_list.append(info_dict['AF'])
            else:
                self.X_tp_AF_list.append(NaN)
            if 'AC' in info_dict.keys():
                self.X_tp_AC_list.append(info_dict['AC'])
            else:
                self.X_tp_AC_list.append(NaN)
            if 'HaplotypeScore' in info_dict.keys():
                self.X_tp_HaplotypeScore_list.append(info_dict['HaplotypeScore'])
            else:
                self.X_tp_HaplotypeScore_list.append(NaN)
            if 'BaseQRankSum' in info_dict.keys():
                self.X_tp_BaseQRankSum_list.append(info_dict['BaseQRankSum'])
            else:
                self.X_tp_BaseQRankSum_list.append(NaN)
            self.Y_tp_list.append(tag)

    def processing_fp_datas(self, vcf_in, tag):
        for rec in vcf_in.fetch():
            POS = rec.pos
            QUAL = rec.qual
            chrom = rec.chrom
            info_dict = rec.info
            self.X_fp_CHROM_list.append(chrom)
            self.X_fp_POS_list.append(POS)
            self.X_fp_QUAL_list.append(QUAL)
            if 'MQ' in info_dict.keys():
                self.X_fp_MQ_list.append(info_dict['MQ'])
            else:
                self.X_fp_MQ_list.append(NaN)
            if 'QD' in info_dict.keys():
                self.X_fp_QD_list.append(info_dict['QD'])
            else:
                self.X_fp_QD_list.append(NaN)
            if 'FS' in info_dict.keys():
                self.X_fp_FS_list.append(info_dict['FS'])
            else:
                self.X_fp_FS_list.append(NaN)
            # if 'SOR' in info_dict.keys():
            #     self.X_fp_SOR_list.append(info_dict['SOR'])
            # else:
            #     self.X_fp_SOR_list.append(NaN)
            if 'MQRankSum' in info_dict.keys():
                self.X_fp_MQRankSum_list.append(info_dict['MQRankSum'])
            else:
                self.X_fp_MQRankSum_list.append(NaN)
            if 'ReadPosRankSum' in info_dict.keys():
                self.X_fp_ReadPosRankSum_list.append(info_dict['ReadPosRankSum'])
            else:
                self.X_fp_ReadPosRankSum_list.append(NaN)

            if 'AF' in info_dict.keys():
                self.X_fp_AF_list.append(info_dict['AF'])
            else:
                self.X_fp_AF_list.append(NaN)
            if 'AC' in info_dict.keys():
                self.X_fp_AC_list.append(info_dict['AC'])
            else:
                self.X_tp_AC_list.append(NaN)
            if 'HaplotypeScore' in info_dict.keys():
                self.X_fp_HaplotypeScore_list.append(info_dict['HaplotypeScore'])
            else:
                self.X_fp_HaplotypeScore_list.append(NaN)
            if 'BaseQRankSum' in info_dict.keys():
                self.X_fp_BaseQRankSum_list.append(info_dict['BaseQRankSum'])
            else:
                self.X_fp_BaseQRankSum_list.append(NaN)
            self.Y_fp_list.append(tag)

    def processing(self):
        tp_vcf = self.tp_vcf
        fp_vcf = self.fp_vcf
        tp_out_csv = self.tp_out
        fp_out_csv = self.fp_out
        vcf_in_tp = pysam.VariantFile(tp_vcf)
        vcf_in_fp = pysam.VariantFile(fp_vcf)

        self.processing_tp_datas(vcf_in_tp, 1)
        self.processing_fp_datas(vcf_in_fp, 0)


        Y_tp_list_str = map(str, self.Y_tp_list)
        X_tp_CHROM_list_str = map(str, self.X_tp_CHROM_list)
        X_tp_POS_list_str = map(str, self.X_tp_POS_list)
        X_tp_QUAL_list_str = map(str, self.X_tp_QUAL_list)
        X_tp_MQ_list_str = map(str, self.X_tp_MQ_list)
        X_tp_QD_list_str = map(str, self.X_tp_QD_list)
        X_tp_ReadPosRankSum_list_str = map(str, self.X_tp_ReadPosRankSum_list)
        X_tp_FS_list_str = map(str, self.X_tp_FS_list)
        # X_tp_SOR_list_str = map(str, self.X_tp_SOR_list)
        X_tp_MQRankSum_list_str = map(str, self.X_tp_MQRankSum_list)
        X_tp_AC_list_str = map(str, self.X_tp_AC_list)
        X_tp_AF_list_str = map(str, self.X_tp_AF_list)
        X_tp_HaplotypeScore_list_str = map(str, self.X_tp_HaplotypeScore_list)
        X_tp_BaseQRankSum_list_str = map(str, self.X_tp_BaseQRankSum_list)

        Y_fp_list_str = map(str, self.Y_fp_list)
        X_fp_CHROM_list_str = map(str, self.X_fp_CHROM_list)
        X_fp_POS_list_str = map(str, self.X_fp_POS_list)
        X_fp_QUAL_list_str = map(str, self.X_fp_QUAL_list)
        X_fp_MQ_list_str = map(str, self.X_fp_MQ_list)
        X_fp_QD_list_str = map(str, self.X_fp_QD_list)
        X_fp_ReadPosRankSum_list_str = map(str, self.X_fp_ReadPosRankSum_list)
        X_fp_FS_list_str = map(str, self.X_fp_FS_list)
        # X_fp_SOR_list_str = map(str, self.X_fp_SOR_list)
        X_fp_MQRankSum_list_str = map(str, self.X_fp_MQRankSum_list)
        X_fp_AC_list_str = map(str, self.X_fp_AC_list)
        X_fp_AF_list_str = map(str, self.X_fp_AF_list)
        X_fp_HaplotypeScore_list_str = map(str, self.X_fp_HaplotypeScore_list)
        X_fp_BaseQRankSum_list_str = map(str, self.X_fp_BaseQRankSum_list)

        # 字典中的key值即为csv中列名
        dataframe_fp = pd.DataFrame({'CHROM': X_fp_CHROM_list_str,
                                    'POS': X_fp_POS_list_str,
                                    'QUAL': X_fp_QUAL_list_str,
                                    'MQ': X_fp_MQ_list_str,
                                    'QD': X_fp_QD_list_str,
                                    'ReadPosRankSum': X_fp_ReadPosRankSum_list_str,
                                    'FS': X_fp_FS_list_str,
                                    'MQRankSum': X_fp_MQRankSum_list_str,
                                    'AF': X_fp_AF_list_str,
                                    'AC': X_fp_AC_list_str,
                                    'HaplotypeScore': X_fp_HaplotypeScore_list_str,
                                    'BaseQRankSum': X_fp_BaseQRankSum_list_str,
                                    'type': Y_fp_list_str
                                    },
                                    columns=['CHROM', 'POS', 'QUAL', 'MQ', 'QD', 'ReadPosRankSum', 'FS', 'MQRankSum',
                                             'AF','AC','HaplotypeScore','BaseQRankSum',
                                             'type'])

        # 将DataFrame存储为csv,index表示是否显示行名，default=True
        dataframe_fp.to_csv(fp_out_csv, index=False,sep=',')

        # 字典中的key值即为csv中列名
        dataframe_tp = pd.DataFrame({'CHROM': X_tp_CHROM_list_str,
                                    'POS': X_tp_POS_list_str,
                                    'QUAL': X_tp_QUAL_list_str,
                                    'MQ': X_tp_MQ_list_str,
                                    'QD': X_tp_QD_list_str,
                                    'ReadPosRankSum': X_tp_ReadPosRankSum_list_str,
                                    'FS': X_tp_FS_list_str,
                                    'MQRankSum': X_tp_MQRankSum_list_str,
                                    'AF': X_tp_AF_list_str,
                                    'AC': X_tp_AC_list_str,
                                    'HaplotypeScore': X_tp_HaplotypeScore_list_str,
                                    'BaseQRankSum': X_tp_BaseQRankSum_list_str,
                                    'type': Y_tp_list_str
                                    },
                                   columns=['CHROM', 'POS','QUAL', 'MQ', 'QD', 'ReadPosRankSum', 'FS', 'MQRankSum',
                                            'AF','AC','HaplotypeScore','BaseQRankSum',
                                            'type'])

        # 将DataFrame存储为csv,index表示是否显示行名，default=True
        dataframe_tp.to_csv(tp_out_csv, index=False,sep=',')


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-v1','--vcf1',help='input vcf file',required=True)
    parser.add_argument('-v0', '--vcf0', help='input vcf file', required=True)
    # parser.add_argument('-k1', '--knowns1', help='input the truth sites vcf files', required=True)
    # parser.add_argument('-k2', '--knowns2', help='input the truth sites vcf files', required=True)
    parser.add_argument('-ot', '--out_tp', help='output true positives csv file',required=True)
    parser.add_argument('-of', '--out_fp', help='output false positives csv file', required=True)
    parser.add_argument('-l', '--logging_file', help='the logging file',required=True)

    args = parser.parse_args()
    vcf1_file = os.path.abspath(args.vcf1)
    vcf0_file = os.path.abspath(args.vcf0)
    # knowns_file1 = os.path.abspath(args.knowns1)
    # knowns_file2 = os.path.abspath(args.knowns2)
    tp_file=os.path.abspath(args.out_tp)
    fp_file=os.path.abspath(args.out_fp)
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
    args_ = [vcf1_file,vcf0_file,tp_file,fp_file]
    process_data = Process_data(args_)
    process_data.processing()
    logger.info('\n[ end time: %s]',time.asctime( time.localtime(time.time()) ))
