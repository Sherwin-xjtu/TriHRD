#!/usr/bin/python
# coding=utf-8

import pysam
import vcf
import pandas as pd
from numpy import *

data_vcf = "/mnt/GenePlus001/prod/workspace/IFA20180710002/OncoH/output/180003461BCD/variation/hereditary_snv_indel/180003461BCD.indel.raw.vcf"
gvcf1 = "/mnt/X500/farmers/wangxw/newResults/gatk_bundle/1000G_phase1.indels.b37.vcf.gz"
gvcf2 = "/mnt/X500/farmers/wangxw/newResults/gatk_bundle/1000G_phase1.indels.b37.vcf.gz"
gvcf3 = "/mnt/X500/farmers/wangxw/newResults/gatk_bundle/1000G_phase1.indels.b37.vcf.gz"

vcf_in = pysam.VariantFile(data_vcf)
vcf_in1 = pysam.VariantFile(gvcf1)
vcf_in2 = pysam.VariantFile(gvcf2)
vcf_in3 = pysam.VariantFile(gvcf3)

Y_list = []
X_tp_CHROM_list = []
X_tp_POS_list = []
X_tp_QUAL_list = []
X_tp_MQ_list = []
X_tp_QD_list = []
X_tp_FS_list = []
X_tp_SOR_list = []
X_tp_MQRankSum_list = []
X_tp_ReadPosRankSum_list = []

X_fp_CHROM_list = []
X_fp_POS_list = []
X_fp_QUAL_list = []
X_fp_MQ_list = []
X_tp_QD_list = []
X_U_FS_list = []
X_U_SOR_list = []
X_U_MQRankSum_list = []
X_U_ReadPosRankSum_list = []

# ['__class__', '__delattr__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__',
#  '__gt__', '__hash__', '__init__', '__le__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__',
#  '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__',
#  'alleles', 'alts', 'chrom', 'contig', 'copy', 'filter', 'format', 'header', 'id', 'info', 'pos', 'qual',
#  'ref', 'rid', 'rlen', 'samples', 'start', 'stop', 'translate']


for record in vcf_in.fetch():
    POS = record.pos
    REF = record.ref
    ALTS = record.alts
    QUAL = record.qual
    chrom = record.chrom
    info_dict = record.info
    ulable = True
    x_list = []

    for rec in vcf_in1.fetch(chrom, POS - 1, POS):
        if rec.chrom == chrom and rec.ref == REF and set(ALTS).issubset(set(rec.alts)):
            ulable = False
            if 'PASS' in rec.filter.keys():
                X_tp_CHROM_list.append(chrom)
                X_tp_POS_list.append(POS)
                X_tp_QUAL_list.append(QUAL)

                if 'MQ' in info_dict.keys():
                    X_tp_MQ_list.append(info_dict['MQ'])
                else:
                    X_tp_MQ_list.append(NaN)
                if 'QD' in info_dict.keys():
                    X_tp_QD_list.append(info_dict['QD'])
                else:
                    X_tp_QD_list.append(NaN)
                if 'FS' in info_dict.keys():
                    X_tp_FS_list.append(info_dict['FS'])
                else:
                    X_tp_FS_list.append(NaN)
                if 'SOR' in info_dict.keys():
                    X_tp_SOR_list.append(info_dict['SOR'])
                else:
                    X_tp_SOR_list.append(NaN)
                if 'MQRankSum' in info_dict.keys():
                    X_tp_MQRankSum_list.append(info_dict['MQRankSum'])
                else:
                    X_tp_MQRankSum_list.append(NaN)
                if 'ReadPosRankSum' in info_dict.keys():
                    X_tp_ReadPosRankSum_list.append(info_dict['ReadPosRankSum'])
                else:
                    X_tp_ReadPosRankSum_list.append(NaN)
                Y_list.append(1)
            else:
                X_tp_CHROM_list.append(chrom)
                X_tp_POS_list.append(POS)
                X_tp_QUAL_list.append(QUAL)
                if 'MQ' in info_dict.keys():
                    X_tp_MQ_list.append(info_dict['MQ'])
                else:
                    X_tp_MQ_list.append(NaN)
                if 'QD' in info_dict.keys():
                    X_tp_QD_list.append(info_dict['QD'])
                else:
                    X_tp_QD_list.append(NaN)
                if 'FS' in info_dict.keys():
                    X_tp_FS_list.append(info_dict['FS'])
                else:
                    X_tp_FS_list.append(NaN)
                if 'SOR' in info_dict.keys():
                    X_tp_SOR_list.append(info_dict['SOR'])
                else:
                    X_tp_SOR_list.append(NaN)
                if 'MQRankSum' in info_dict.keys():
                    X_tp_MQRankSum_list.append(info_dict['MQRankSum'])
                else:
                    X_tp_MQRankSum_list.append(NaN)
                if 'ReadPosRankSum' in info_dict.keys():
                    X_tp_ReadPosRankSum_list.append(info_dict['ReadPosRankSum'])
                else:
                    X_tp_ReadPosRankSum_list.append(NaN)
                Y_list.append(0)
    if ulable:
        for rec in vcf_in2.fetch(chrom, POS - 1, POS):
            if rec.chrom == chrom and rec.ref == REF and set(ALTS).issubset(set(rec.alts)):
                ulable = False
                if 'PASS' in rec.filter.keys():
                    X_tp_CHROM_list.append(chrom)
                    X_tp_POS_list.append(POS)
                    X_tp_QUAL_list.append(QUAL)

                    if 'MQ' in info_dict.keys():
                        X_tp_MQ_list.append(info_dict['MQ'])
                    else:
                        X_tp_MQ_list.append(NaN)
                    if 'QD' in info_dict.keys():
                        X_tp_QD_list.append(info_dict['QD'])
                    else:
                        X_tp_QD_list.append(NaN)
                    if 'FS' in info_dict.keys():
                        X_tp_FS_list.append(info_dict['FS'])
                    else:
                        X_tp_FS_list.append(NaN)
                    if 'SOR' in info_dict.keys():
                        X_tp_SOR_list.append(info_dict['SOR'])
                    else:
                        X_tp_SOR_list.append(NaN)
                    if 'MQRankSum' in info_dict.keys():
                        X_tp_MQRankSum_list.append(info_dict['MQRankSum'])
                    else:
                        X_tp_MQRankSum_list.append(NaN)
                    if 'ReadPosRankSum' in info_dict.keys():
                        X_tp_ReadPosRankSum_list.append(info_dict['ReadPosRankSum'])
                    else:
                        X_tp_ReadPosRankSum_list.append(NaN)
                    Y_list.append(1)
                else:
                    X_tp_CHROM_list.append(chrom)
                    X_tp_POS_list.append(POS)
                    X_tp_QUAL_list.append(QUAL)
                    if 'MQ' in info_dict.keys():
                        X_tp_MQ_list.append(info_dict['MQ'])
                    else:
                        X_tp_MQ_list.append(NaN)
                    if 'QD' in info_dict.keys():
                        X_tp_QD_list.append(info_dict['QD'])
                    else:
                        X_tp_QD_list.append(NaN)
                    if 'FS' in info_dict.keys():
                        X_tp_FS_list.append(info_dict['FS'])
                    else:
                        X_tp_FS_list.append(NaN)
                    if 'SOR' in info_dict.keys():
                        X_tp_SOR_list.append(info_dict['SOR'])
                    else:
                        X_tp_SOR_list.append(NaN)
                    if 'MQRankSum' in info_dict.keys():
                        X_tp_MQRankSum_list.append(info_dict['MQRankSum'])
                    else:
                        X_tp_MQRankSum_list.append(NaN)
                    if 'ReadPosRankSum' in info_dict.keys():
                        X_tp_ReadPosRankSum_list.append(info_dict['ReadPosRankSum'])
                    else:
                        X_tp_ReadPosRankSum_list.append(NaN)
                    Y_list.append(0)

    if ulable:
        for rec in vcf_in3.fetch(chrom, POS - 1, POS):
            if rec.chrom == chrom and rec.ref == REF and set(ALTS).issubset(set(rec.alts)):
                ulable = False
                if 'PASS' in rec.filter.keys():
                    X_tp_CHROM_list.append(chrom)
                    X_tp_POS_list.append(POS)
                    X_tp_QUAL_list.append(QUAL)

                    if 'MQ' in info_dict.keys():
                        X_tp_MQ_list.append(info_dict['MQ'])
                    else:
                        X_tp_MQ_list.append(NaN)
                    if 'QD' in info_dict.keys():
                        X_tp_QD_list.append(info_dict['QD'])
                    else:
                        X_tp_QD_list.append(NaN)
                    if 'FS' in info_dict.keys():
                        X_tp_FS_list.append(info_dict['FS'])
                    else:
                        X_tp_FS_list.append(NaN)
                    if 'SOR' in info_dict.keys():
                        X_tp_SOR_list.append(info_dict['SOR'])
                    else:
                        X_tp_SOR_list.append(NaN)
                    if 'MQRankSum' in info_dict.keys():
                        X_tp_MQRankSum_list.append(info_dict['MQRankSum'])
                    else:
                        X_tp_MQRankSum_list.append(NaN)
                    if 'ReadPosRankSum' in info_dict.keys():
                        X_tp_ReadPosRankSum_list.append(info_dict['ReadPosRankSum'])
                    else:
                        X_tp_ReadPosRankSum_list.append(NaN)
                    Y_list.append(1)
                else:
                    X_tp_CHROM_list.append(chrom)
                    X_tp_POS_list.append(POS)
                    X_tp_QUAL_list.append(QUAL)
                    if 'MQ' in info_dict.keys():
                        X_tp_MQ_list.append(info_dict['MQ'])
                    else:
                        X_tp_MQ_list.append(NaN)
                    if 'QD' in info_dict.keys():
                        X_tp_QD_list.append(info_dict['QD'])
                    else:
                        X_tp_QD_list.append(NaN)
                    if 'FS' in info_dict.keys():
                        X_tp_FS_list.append(info_dict['FS'])
                    else:
                        X_tp_FS_list.append(NaN)
                    if 'SOR' in info_dict.keys():
                        X_tp_SOR_list.append(info_dict['SOR'])
                    else:
                        X_tp_SOR_list.append(NaN)
                    if 'MQRankSum' in info_dict.keys():
                        X_tp_MQRankSum_list.append(info_dict['MQRankSum'])
                    else:
                        X_tp_MQRankSum_list.append(NaN)
                    if 'ReadPosRankSum' in info_dict.keys():
                        X_tp_ReadPosRankSum_list.append(info_dict['ReadPosRankSum'])
                    else:
                        X_tp_ReadPosRankSum_list.append(NaN)
                    Y_list.append(0)

    if ulable:
        X_fp_CHROM_list.append(chrom)
        X_fp_POS_list.append(POS)
        X_fp_QUAL_list.append(QUAL)
        if 'MQ' in info_dict.keys():
            X_fp_MQ_list.append(info_dict['MQ'])
        else:
            X_fp_MQ_list.append(NaN)
        if 'QD' in info_dict.keys():
            X_tp_QD_list.append(info_dict['QD'])
        else:
            X_tp_QD_list.append(NaN)
        if 'FS' in info_dict.keys():
            X_U_FS_list.append(info_dict['FS'])
        else:
            X_U_FS_list.append(NaN)
        if 'SOR' in info_dict.keys():
            X_U_SOR_list.append(info_dict['SOR'])
        else:
            X_U_SOR_list.append(NaN)
        if 'MQRankSum' in info_dict.keys():
            X_U_MQRankSum_list.append(info_dict['MQRankSum'])
        else:
            X_U_MQRankSum_list.append(NaN)
        if 'ReadPosRankSum' in info_dict.keys():
            X_U_ReadPosRankSum_list.append(info_dict['ReadPosRankSum'])
        else:
            X_U_ReadPosRankSum_list.append(NaN)

Y_list_str = map(str, Y_list)
X_tp_CHROM_list_str = map(str,X_tp_CHROM_list)
X_tp_POS_list_str = map(str,X_tp_POS_list)
X_tp_QUAL_list_str = map(str,X_tp_QUAL_list)
X_tp_MQ_list_str = map(str,X_tp_MQ_list)
X_tp_QD_list_str = map(str,X_tp_QD_list)
X_tp_ReadPosRankSum_list_str = map(str,X_tp_ReadPosRankSum_list)
X_tp_FS_list_str = map(str,X_tp_FS_list)
X_tp_SOR_list_str = map(str,X_tp_SOR_list)
X_tp_MQRankSum_list_str = map(str,X_tp_MQRankSum_list)

X_fp_CHROM_list_str = map(str,X_fp_CHROM_list)
X_fp_POS_list_str = map(str,X_fp_POS_list)
X_fp_QUAL_list_str = map(str,X_fp_QUAL_list)
X_fp_MQ_list_str = map(str,X_fp_MQ_list)
X_tp_QD_list_str = map(str,X_tp_QD_list)
X_U_ReadPosRankSum_list_str = map(str,X_U_ReadPosRankSum_list)
X_U_FS_list_str = map(str,X_U_FS_list)
X_U_SOR_list_str = map(str,X_U_SOR_list)
X_U_MQRankSum_list_str = map(str,X_U_MQRankSum_list)

#字典中的key值即为csv中列名
dataframe_U = pd.DataFrame({'CHROM':X_fp_CHROM_list_str,
                            'POS':X_fp_POS_list_str,
                            'MQ':X_fp_MQ_list_str,
                            'QD':X_tp_QD_list_str,
                            'ReadPosRankSum':X_U_ReadPosRankSum_list_str,
                            'FS':X_U_FS_list_str,
                            'MQRankSum':X_U_MQRankSum_list_str,
                            'QUAL':X_fp_QUAL_list_str,
                            'SOR':X_U_SOR_list_str,
                            },columns=['CHROM','POS','MQ','QD','ReadPosRankSum','FS','MQRankSum','QUAL','SOR'])

#将DataFrame存储为csv,index表示是否显示行名，default=True
dataframe_U.to_csv("/mnt/X500/farmers/wangxw/tri_training_results/resoult_csv/Test_U__072201.csv",index=False,sep=',')

#字典中的key值即为csv中列名
dataframe_L = pd.DataFrame({'CHROM':X_fp_CHROM_list_str,
                            'POS':X_fp_POS_list_str,
                            'MQ':X_fp_MQ_list_str,
                            'QD':X_tp_QD_list_str,
                            'ReadPosRankSum':X_U_ReadPosRankSum_list_str,
                            'FS':X_U_FS_list_str,
                            'MQRankSum':X_U_MQRankSum_list_str,
                            'QUAL':X_fp_QUAL_list_str,
                            'SOR':X_U_SOR_list_str,
                            'type':Y_list_str
                            },columns=['CHROM','POS','MQ','QD','ReadPosRankSum','FS','MQRankSum','QUAL','SOR','type'])

#将DataFrame存储为csv,index表示是否显示行名，default=True
dataframe_L.to_csv("/mnt/X500/farmers/wangxw/tri_training_results/resoult_csv/Test_L__072201.csv",index=False,sep=',')
