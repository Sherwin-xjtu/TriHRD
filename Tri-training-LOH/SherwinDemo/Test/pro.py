#!/usr/bin/python
# coding=utf-8

import argparse
import logging
import pandas as pd
from numpy import *
import csv,os,argparse,string,sys,multiprocessing,logging,functools,time,signal, re
import vcf
sys.dont_write_bytecode = True
csv.register_dialect("line_terminator",lineterminator="\n")
VERSION='1.0.1'



class Process_data:

    def __init__(self):
        self.Y_list = []
        self.X_L_CHROM_list = []
        self.X_L_POS_list = []
        self.X_L_QUAL_list = []
        self.X_L_MQ_list = []
        self.X_L_QD_list = []
        self.X_L_FS_list = []
        self.X_L_SOR_list = []
        self.X_L_MQRankSum_list = []
        self.X_L_ReadPosRankSum_list = []

        self.X_L_BaseQRankSum_list = []
        self.X_L_GQ_list = []
        self.X_L_DP_list = []
        self.X_L_PL_list = []

    def processing(self):
        vcf_reader = vcf.Reader(filename='C:/Users/Sherwin/Desktop/output/NA12878-GATK3-chr21/tp.vcf')
        labeled_path = 'C:/Users/Sherwin/Desktop/output/NA12878-GATK3-chr21/tp.csv'

        for record in vcf_reader:
            POS = record.POS
            QUAL = record.QUAL
            chrom = record.CHROM
            info_dict = record.INFO
            for samp in record.samples:
                self.X_L_DP_list.append(samp['DP'])
                self.X_L_PL_list.append(samp['PL'])
                self.X_L_GQ_list.append(samp['GQ'])
                break

            self.X_L_CHROM_list.append(chrom)
            self.X_L_POS_list.append(POS)
            self.X_L_QUAL_list.append(QUAL)

            if 'MQ' in info_dict.keys():
                self.X_L_MQ_list.append(info_dict['MQ'])
            else:
                self.X_L_MQ_list.append(NaN)
            if 'QD' in info_dict.keys():
                self.X_L_QD_list.append(info_dict['QD'])
            else:
                self.X_L_QD_list.append(NaN)
            if 'FS' in info_dict.keys():
                self.X_L_FS_list.append(info_dict['FS'])
            else:
                self.X_L_FS_list.append(NaN)
            if 'SOR' in info_dict.keys():
                self.X_L_SOR_list.append(info_dict['SOR'])
            else:
                self.X_L_SOR_list.append(NaN)
            if 'MQRankSum' in info_dict.keys():
                self.X_L_MQRankSum_list.append(info_dict['MQRankSum'])
            else:
                self.X_L_MQRankSum_list.append(NaN)
            if 'ReadPosRankSum' in info_dict.keys():
                self.X_L_ReadPosRankSum_list.append(info_dict['ReadPosRankSum'])
            else:
                self.X_L_ReadPosRankSum_list.append(NaN)
            if 'BaseQRankSum' in info_dict.keys():
                self.X_L_BaseQRankSum_list.append(info_dict['BaseQRankSum'])
            else:
                self.X_L_BaseQRankSum_list.append(NaN)
            self.Y_list.append(1)
        print len(self.X_L_GQ_list)
        Y_list_str = map(str, self.Y_list)
        X_L_CHROM_list_str = map(str, self.X_L_CHROM_list)
        X_L_POS_list_str = map(str, self.X_L_POS_list)
        X_L_QUAL_list_str = map(str, self.X_L_QUAL_list)
        X_L_MQ_list_str = map(str, self.X_L_MQ_list)
        X_L_QD_list_str = map(str, self.X_L_QD_list)
        X_L_ReadPosRankSum_list_str = map(str, self.X_L_ReadPosRankSum_list)
        X_L_FS_list_str = map(str, self.X_L_FS_list)
        X_L_SOR_list_str = map(str, self.X_L_SOR_list)
        X_L_MQRankSum_list_str = map(str, self.X_L_MQRankSum_list)

        X_L_BaseQRankSum_list_str = map(str, self.X_L_BaseQRankSum_list)
        X_L_GQ_list_str = map(str, self.X_L_GQ_list)
        X_L_DP_list_str = map(str, self.X_L_DP_list)
        X_L_PL_list_str = map(str, self.X_L_PL_list)

        # 字典中的key值即为csv中列名
        dataframe_L = pd.DataFrame({'CHROM': self.X_L_CHROM_list,
                                    'POS': self.X_L_POS_list,
                                    'QUAL': self.X_L_QUAL_list,
                                    'MQ': self.X_L_MQ_list,
                                    'QD': self.X_L_QD_list,
                                    'ReadPosRankSum': self.X_L_ReadPosRankSum_list,
                                    'FS': self.X_L_FS_list,
                                    'MQRankSum': self.X_L_MQRankSum_list,
                                    'SOR': self.X_L_SOR_list,
                                    'BaseQRankSum': self.X_L_BaseQRankSum_list,
                                    'GQ': self.X_L_GQ_list,
                                    'DP': self.X_L_DP_list,
                                    'PL': self.X_L_PL_list,
                                    'type': self.Y_list
                                    },
                                   columns=['CHROM', 'POS','QUAL', 'MQ', 'QD', 'ReadPosRankSum', 'FS', 'MQRankSum','SOR', 'BaseQRankSum', 'GQ', 'DP', 'PL', 'type'])

        # 将DataFrame存储为csv,index表示是否显示行名，default=True
        dataframe_L.to_csv(labeled_path, index=False,sep=',')


if __name__=="__main__":
    process_data = Process_data()
    process_data.processing()
 #   logger.info('\n[ end time: %s]',time.asctime( time.localtime(time.time()) ))
