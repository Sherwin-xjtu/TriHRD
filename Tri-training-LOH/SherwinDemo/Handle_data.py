#!/usr/bin/python
# coding=utf-8
import pandas as pd
import numpy as np
from sklearn import preprocessing
import csv

def l_standardization(input_path,l1_output_path,l0_output_path,u_output_path,lt1_output_path,lt0_output_path):
    unlabeled_path = u_output_path
    labeled1_path = l1_output_path
    labeled0_path = l0_output_path
    labeledt1_path = lt1_output_path
    labeledt0_path = lt0_output_path
    Yt1_list = []
    Xt_L1_CHROM_list = []
    Xt_L1_POS_list = []
    Xt_L1_QUAL_list = []
    Xt_L1_MQ_list = []
    Xt_L1_QD_list = []
    Xt_L1_FS_list = []
    Xt_L1_SOR_list = []
    Xt_L1_MQRankSum_list = []
    Xt_L1_ReadPosRankSum_list = []

    Yt0_list = []
    Xt_L0_CHROM_list = []
    Xt_L0_POS_list = []
    Xt_L0_QUAL_list = []
    Xt_L0_MQ_list = []
    Xt_L0_QD_list = []
    Xt_L0_FS_list = []
    Xt_L0_SOR_list = []
    Xt_L0_MQRankSum_list = []
    Xt_L0_ReadPosRankSum_list = []

    Y1_list = []
    X_L1_CHROM_list = []
    X_L1_POS_list = []
    X_L1_QUAL_list = []
    X_L1_MQ_list = []
    X_L1_QD_list = []
    X_L1_FS_list = []
    X_L1_SOR_list = []
    X_L1_MQRankSum_list = []
    X_L1_ReadPosRankSum_list = []

    Y0_list = []
    X_L0_CHROM_list = []
    X_L0_POS_list = []
    X_L0_QUAL_list = []
    X_L0_MQ_list = []
    X_L0_QD_list = []
    X_L0_FS_list = []
    X_L0_SOR_list = []
    X_L0_MQRankSum_list = []
    X_L0_ReadPosRankSum_list = []



    X_fp_CHROM_list = []
    X_fp_POS_list = []
    X_fp_QUAL_list = []
    X_fp_MQ_list = []
    X_tp_QD_list = []
    X_U_FS_list = []
    X_U_SOR_list = []
    X_U_MQRankSum_list = []
    X_U_ReadPosRankSum_list = []

    f = open(input_path, mode='r')  # mode读取模式，采用b的方式处理可以省去很多问题，encoding编码方式
    reader = csv.reader(f)  # 获取输入数据。把每一行数据转化成了一个list，list中每个元素是一个字符串
    for row in reader:  # 按行读取文件。一行读取为字符串，在使用分割符（默认逗号）分割成字符串列表，对于包含逗号，并使用""标志的字符串不进行分割
        if row[0] == 'CHROM':
            continue
        else:
            if row[9] == '1' and len(X_L1_CHROM_list) < 100:
                print row[6]
                X_L1_CHROM_list.append(row[0])
                X_L1_POS_list.append(row[1])
                X_L1_QUAL_list.append(row[2])
                X_L1_MQ_list.append(row[3])
                X_L1_QD_list.append(row[4])
                X_L1_ReadPosRankSum_list.append(row[5])
                X_L1_FS_list.append(row[6])
                X_L1_MQRankSum_list.append(row[7])
                X_L1_SOR_list.append(row[8])
                Y1_list.append(1)
                continue

            if row[9] == '0' and len(X_L0_CHROM_list) < 100:
                X_L0_CHROM_list.append(row[0])
                X_L0_POS_list.append(row[1])
                X_L0_QUAL_list.append(row[2])
                X_L0_MQ_list.append(row[3])
                X_L0_QD_list.append(row[4])
                X_L0_ReadPosRankSum_list.append(row[5])
                X_L0_FS_list.append(row[6])
                X_L0_MQRankSum_list.append(row[7])
                X_L0_SOR_list.append(row[8])
                Y0_list.append(0)
                continue

            if row[9] == '1' and len(Xt_L1_CHROM_list) < 1500:
                Xt_L1_CHROM_list.append(row[0])
                Xt_L1_POS_list.append(row[1])
                Xt_L1_QUAL_list.append(row[2])
                Xt_L1_MQ_list.append(row[3])
                Xt_L1_QD_list.append(row[4])
                Xt_L1_ReadPosRankSum_list.append(row[5])
                Xt_L1_FS_list.append(row[6])
                Xt_L1_MQRankSum_list.append(row[7])
                Xt_L1_SOR_list.append(row[8])
                Yt1_list.append(1)
                continue

            if row[9] == '0' and len(Xt_L0_CHROM_list) < 1500:
                Xt_L0_CHROM_list.append(row[0])
                Xt_L0_POS_list.append(row[1])
                Xt_L0_QUAL_list.append(row[2])
                Xt_L0_MQ_list.append(row[3])
                Xt_L0_QD_list.append(row[4])
                Xt_L0_ReadPosRankSum_list.append(row[5])
                Xt_L0_FS_list.append(row[6])
                Xt_L0_MQRankSum_list.append(row[7])
                Xt_L0_SOR_list.append(row[8])
                Yt0_list.append(0)
                continue

        X_fp_CHROM_list.append(row[0])
        X_fp_POS_list.append(row[1])
        X_fp_QUAL_list.append(row[2])
        X_fp_MQ_list.append(row[3])
        X_tp_QD_list.append(row[4])
        X_U_ReadPosRankSum_list.append(row[5])
        X_U_FS_list.append(row[6])
        X_U_MQRankSum_list.append(row[7])
        X_U_SOR_list.append(row[8])
        continue


    Yt1_list_str = map(str,Yt1_list)
    Xt_L1_CHROM_list_str = map(str,Xt_L1_CHROM_list)
    Xt_L1_POS_list_str = map(str,Xt_L1_POS_list)
    Xt_L1_QUAL_list_str = map(str,Xt_L1_QUAL_list)
    Xt_L1_MQ_list_str = map(str,Xt_L1_MQ_list)
    Xt_L1_QD_list_str = map(str,Xt_L1_QD_list)
    Xt_L1_ReadPosRankSum_list_str = map(str,Xt_L1_ReadPosRankSum_list)
    Xt_L1_FS_list_str = map(str,Xt_L1_FS_list)
    Xt_L1_SOR_list_str = map(str,Xt_L1_SOR_list)
    Xt_L1_MQRankSum_list_str = map(str,Xt_L1_MQRankSum_list)

    Yt0_list_str = map(str, Yt0_list)
    Xt_L0_CHROM_list_str = map(str, Xt_L0_CHROM_list)
    Xt_L0_POS_list_str = map(str, Xt_L0_POS_list)
    Xt_L0_QUAL_list_str = map(str, Xt_L0_QUAL_list)
    Xt_L0_MQ_list_str = map(str, Xt_L0_MQ_list)
    Xt_L0_QD_list_str = map(str, Xt_L0_QD_list)
    Xt_L0_ReadPosRankSum_list_str = map(str, Xt_L0_ReadPosRankSum_list)
    Xt_L0_FS_list_str = map(str, Xt_L0_FS_list)
    Xt_L0_SOR_list_str = map(str, Xt_L0_SOR_list)
    Xt_L0_MQRankSum_list_str = map(str, Xt_L0_MQRankSum_list)

    Y1_list_str = map(str, Y1_list)
    X_L1_CHROM_list_str = map(str, X_L1_CHROM_list)
    X_L1_POS_list_str = map(str, X_L1_POS_list)
    X_L1_QUAL_list_str = map(str, X_L1_QUAL_list)
    X_L1_MQ_list_str = map(str, X_L1_MQ_list)
    X_L1_QD_list_str = map(str, X_L1_QD_list)
    X_L1_ReadPosRankSum_list_str = map(str, X_L1_ReadPosRankSum_list)
    X_L1_FS_list_str = map(str, X_L1_FS_list)
    X_L1_SOR_list_str = map(str, X_L1_SOR_list)
    X_L1_MQRankSum_list_str = map(str, X_L1_MQRankSum_list)

    Y0_list_str = map(str, Y0_list)
    X_L0_CHROM_list_str = map(str, X_L0_CHROM_list)
    X_L0_POS_list_str = map(str, X_L0_POS_list)
    X_L0_QUAL_list_str = map(str, X_L0_QUAL_list)
    X_L0_MQ_list_str = map(str, X_L0_MQ_list)
    X_L0_QD_list_str = map(str, X_L0_QD_list)
    X_L0_ReadPosRankSum_list_str = map(str, X_L0_ReadPosRankSum_list)
    X_L0_FS_list_str = map(str, X_L0_FS_list)
    X_L0_SOR_list_str = map(str, X_L0_SOR_list)
    X_L0_MQRankSum_list_str = map(str, X_L0_MQRankSum_list)


    X_fp_CHROM_list_str = map(str,X_fp_CHROM_list)
    X_fp_POS_list_str = map(str,X_fp_POS_list)
    X_fp_QUAL_list_str = map(str,X_fp_QUAL_list)
    X_fp_MQ_list_str = map(str,X_fp_MQ_list)
    X_tp_QD_list_str = map(str,X_tp_QD_list)
    X_U_ReadPosRankSum_list_str = map(str,X_U_ReadPosRankSum_list)
    X_U_FS_list_str = map(str,X_U_FS_list)
    X_U_SOR_list_str = map(str,X_U_SOR_list)
    X_U_MQRankSum_list_str = map(str,X_U_MQRankSum_list)

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
                               columns=['CHROM', 'POS', 'QUAL', 'MQ', 'QD', 'ReadPosRankSum', 'FS', 'MQRankSum',
                                        'SOR'])

    # 将DataFrame存储为csv,index表示是否显示行名，default=True
    dataframe_U.to_csv(unlabeled_path, index=False, sep=',')

    # 字典中的key值即为csv中列名
    dataframe_L1 = pd.DataFrame({'CHROM': X_L1_CHROM_list_str,
                                'POS': X_L1_POS_list_str,
                                'QUAL': X_L1_QUAL_list_str,
                                'MQ': X_L1_MQ_list_str,
                                'QD': X_L1_QD_list_str,
                                'ReadPosRankSum': X_L1_ReadPosRankSum_list_str,
                                'FS': X_L1_FS_list_str,
                                'MQRankSum': X_L1_MQRankSum_list_str,
                                'SOR': X_L1_SOR_list_str,
                                'type': Y1_list_str
                                },
                               columns=['CHROM', 'POS', 'QUAL', 'MQ', 'QD', 'ReadPosRankSum', 'FS', 'MQRankSum',
                                        'SOR',
                                        'type'])

    # 将DataFrame存储为csv,index表示是否显示行名，default=True
    dataframe_L1.to_csv(labeled1_path, index=False, sep=',')

    dataframe_L0 = pd.DataFrame({'CHROM': X_L0_CHROM_list_str,
                                 'POS': X_L0_POS_list_str,
                                 'QUAL': X_L0_QUAL_list_str,
                                 'MQ': X_L0_MQ_list_str,
                                 'QD': X_L0_QD_list_str,
                                 'ReadPosRankSum': X_L0_ReadPosRankSum_list_str,
                                 'FS': X_L0_FS_list_str,
                                 'MQRankSum': X_L0_MQRankSum_list_str,
                                 'SOR': X_L0_SOR_list_str,
                                 'type': Y0_list_str
                                 },
                                columns=['CHROM', 'POS', 'QUAL', 'MQ', 'QD', 'ReadPosRankSum', 'FS', 'MQRankSum',
                                         'SOR',
                                         'type'])

    # 将DataFrame存储为csv,index表示是否显示行名，default=True
    dataframe_L0.to_csv(labeled0_path, index=False, sep=',')

    dataframe_Lt1 = pd.DataFrame({'CHROM': Xt_L1_CHROM_list_str,
                                 'POS': Xt_L1_POS_list_str,
                                 'QUAL': Xt_L1_QUAL_list_str,
                                 'MQ': Xt_L1_MQ_list_str,
                                 'QD': Xt_L1_QD_list_str,
                                 'ReadPosRankSum': Xt_L1_ReadPosRankSum_list_str,
                                 'FS': Xt_L1_FS_list_str,
                                 'MQRankSum': Xt_L1_MQRankSum_list_str,
                                 'SOR': Xt_L1_SOR_list_str,
                                 'type': Yt1_list_str
                                 },
                                columns=['CHROM', 'POS', 'QUAL', 'MQ', 'QD', 'ReadPosRankSum', 'FS', 'MQRankSum',
                                         'SOR',
                                         'type'])

    # 将DataFrame存储为csv,index表示是否显示行名，default=True
    dataframe_Lt1.to_csv(labeledt1_path, index=False, sep=',')

    dataframe_Lt0 = pd.DataFrame({'CHROM': Xt_L0_CHROM_list_str,
                                 'POS': Xt_L0_POS_list_str,
                                 'QUAL': Xt_L0_QUAL_list_str,
                                 'MQ': Xt_L0_MQ_list_str,
                                 'QD': Xt_L0_QD_list_str,
                                 'ReadPosRankSum': Xt_L0_ReadPosRankSum_list_str,
                                 'FS': Xt_L0_FS_list_str,
                                 'MQRankSum': Xt_L0_MQRankSum_list_str,
                                 'SOR': Xt_L0_SOR_list_str,
                                 'type': Yt0_list_str
                                 },
                                columns=['CHROM', 'POS', 'QUAL', 'MQ', 'QD', 'ReadPosRankSum', 'FS', 'MQRankSum',
                                         'SOR',
                                         'type'])

    # 将DataFrame存储为csv,index表示是否显示行名，default=True
    dataframe_Lt0.to_csv(labeledt0_path, index=False, sep=',')




if __name__=="__main__":

    l_input_path = "../dealData/data/180807_L01.csv"
    l1_output_path = "../dealData/data_processing/180807_L1.csv"
    l0_output_path = "../dealData/data_processing/180807_L0.csv"
    u_output_path = "../dealData/data_processing/180807_U.csv"
    lt1_output_path = "../dealData/data_processing/180807_Lt1.csv"
    lt0_output_path = "../dealData/data_processing/180807_Lt0.csv"
    l_standardization(l_input_path,l1_output_path,l0_output_path,u_output_path,lt1_output_path,lt0_output_path)

    labeled1 = pd.read_csv('../dealData/data_processing/180807_L1.csv')
    labeled0 = pd.read_csv('../dealData/data_processing/180807_L0.csv')
    res = pd.concat([labeled1, labeled0], axis=0)
    res.to_csv('../dealData/data_processing/180807_L.csv', index=False)

    labeledt1 = pd.read_csv('../dealData/data_processing/180807_Lt1.csv')
    labeledt0 = pd.read_csv('../dealData/data_processing/180807_Lt0.csv')
    res = pd.concat([labeledt1, labeledt0], axis=0)
    res.to_csv('../dealData/data_processing/180807_Lt.csv', index=False)
