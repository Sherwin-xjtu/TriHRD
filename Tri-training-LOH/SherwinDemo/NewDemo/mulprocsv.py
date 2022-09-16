#!/usr/bin/python
# coding=utf-8
from __future__ import division
import logging
import numpy as np
from multiprocessing import *
# from multiprocessing import Pool
import pysam
import math
import argparse
import logging
import vcf
import os
import pandas as pd
import shutil
import pandas as pd
import copy
import csv, os, argparse, string, sys, multiprocessing, logging, functools, time, signal, re

sys.dont_write_bytecode = True
csv.register_dialect("line_terminator", lineterminator="\n")
VERSION = '1.0.1'


# from pysam import VariantFile
# vcf_in  = VariantFile("/Volumes/TOSHIBA EXT 1/data/platypus/190018206_TN.vcf", "r")
# # # vcf_out = VariantFile("/Volumes/TOSHIBA EXT 1/data/platypus/test_out.vcf", "w", header=vcf_in.header)
# for record in vcf_in.fetch():
#             # GQ = record.samples['normal']['GQ']
#             POS = record.pos
# #             REF = record.ref

def spfu(listTemp, n):
    for i in range(0, len(listTemp), n):
        yield listTemp[i:i + n]


def compvcf(mlt, nlt, k, return_dict):
    a = 0
    c = 0
    d = 0
    for record2 in mlt:
        for record1 in nlt:
            if record1.CHROM == record2.chrom and record1.POS == record2.pos:
                c = c + 1
                if 'FET' in record1.INFO:
                    if record1.INFO['FET'][0] > 5 and record1.INFO['VAFN'][0] < 0.02:
                        a = a + 1
                        if record1.INFO['VAFC'][0] < 0.01:
                            d = d + 1
    li = [c, a, d]
    return_dict[k] = li

def Assess(pvcf, mlt, threads):
    new_vcfreader = vcf.Reader(open(pvcf, 'r'))
    nlt = []
    relt = []
    p = threads
    manager = multiprocessing.Manager()
    return_dict = manager.dict()

    print('start')
    for record in new_vcfreader:
        nlt.append(record)

    one_lenth = int(len(nlt) / int(p)) + 1
    nlt_arr = spfu(nlt, one_lenth)
    k = -1

    print("start multiprocessing")
    for i in nlt_arr:
        k = k + 1
        process = multiprocessing.Process(target=compvcf, args=(mlt, i, k, return_dict))
        process.start()
        relt.append(process)
    print("end multiprocessing")
    for process in relt:
        process.join()
    return return_dict

def getPathFile(path):
    '''
    name:getPathFile
    function:获取所给文件夹下所有vcf文件路径
    path：所给文件夹路径
    '''
    Path = []
    try:
        pathDir = os.listdir(path)
        for allDir in pathDir:
            child = os.path.join('%s/%s' % (path, allDir))
            # 跳过文件夹以及非流量包文件，将后缀名改为自己需要的文件类型即可实现自己的过滤
            if os.path.isfile(child) and (".vcf" in str(allDir) or (".vcf.gz" in str(allDir))):
                Path.append(child)
    except:
        pass
    return Path

def split_file(vcffile,labeled_file,p_thread):
    i = 0  # 设置计数器
    vcf_reader = vcf.Reader(open(vcffile, 'r'))
    b = os.path.dirname(labeled_file)
    os.mkdir(b + '/temp')
    dir_path = b+'/temp/'

    with open(vcffile) as f:
        text = f.read()

    f1 = open(vcffile, 'r')
    hi = 0
    for line in f1.readlines():
        if line.startswith('#'):
            hi = hi + 1
        else:
            break
    toLength = len(text.splitlines())-hi
    avLength = math.ceil(toLength/p_thread)
    while i < toLength:  # 这里12345表示文件行数，如果不知道行数可用每行长度等其他条件来判断
        vcf_writer = vcf.Writer(open(dir_path+'tmp' + str(i) + '.vcf', 'w'), vcf_reader)
        # with open('newfile'+str(i),'w') as f1:
        for j in range(0, avLength):  # 这里设置每个子文件的大小
            if i < toLength:  # 这里判断是否已结束，否则最后可能报错
                # f1.writelines(f.readline())
                vcf_writer.write_record(vcf_reader.next())
                i = i + 1
            else:
                break
    return dir_path

def readBed(bedFile):
    fr = open(bedFile,'r') #如果文件不是uft-8编码方式，读取文件可能报错
    bed = {}
    tmpBuff = ''
    posList = []
    bedList = []

    for buff in fr:
        buff = buff.rstrip()
        # buff = buff.strip('"')
        buffList = buff.split()
        if tmpBuff == buffList[0]:
            posList.append(int(buffList[1]))
            posList.append(int(buffList[2]))
            bedList.append(posList)
            posList = []
        else:
            if len(bedList) != 0:
                bed[tmpBuff] = bedList
                bedList = []
            tmpBuff = buffList[0]
            posList.append(int(buffList[1]))
            posList.append(int(buffList[2]))
            bedList.append(posList)
            posList = []
    fr.close()
    return bed

def encodeType(record,bed):
    pos = record.POS
    chrom = record.CHROM
    enType = 0
    if chrom in bed.keys():
        for p in bed[chrom]:
            if pos >=p[0] and pos <=p[1]:
                enType = 1
    return enType

def get_ref(rec,HG):
    chrom = rec.CHROM
    pos = rec.POS
    start = pos-2
    end = pos +1
    fastafile = pysam.Fastafile(HG)
    result=fastafile.fetch(chrom, start, end)
    fastafile.close()
    return result

def processingVariants(vcfFile, blackFile, dupFile, refFile,dir_path):
    vcf_in = vcf.Reader(open(vcfFile, 'rb'))
    CHROM_list = []
    POS_list = []
    REF_list = []
    ALT_list = []
    DP_list = []
    AD_list = []
    AF_list = []
    encode_list = []
    segdup_list = []
    refTriCon_list = []
    for rec in vcf_in:
        if rec.is_snp:
            POS = rec.POS
            CHROM = rec.CHROM
            REF = rec.REF
            ALT = rec.ALT
            DP = rec.DP
            AD = rec.AD
            AF = rec.AF
            blackBed = readBed(blackFile)
            ENCODE = encodeType(rec, blackBed)
            dupBed = readBed(dupFile)
            segDup = encodeType(rec, dupBed)
            refTriCon = get_ref(rec, refFile)
            CHROM_list.append(CHROM)
            POS_list.append(POS)
            REF_list.append(REF)
            ALT_list.append(ALT)
            DP_list.append(DP)
            AD_list.append(AD)
            AF_list.append(AF)
            encode_list.append(ENCODE)
            segdup_list.append(segDup)
            refTriCon_list.append(refTriCon)
    # 字典中的key值即为csv中列名
    dataframe_L = pd.DataFrame({'CHROM': CHROM_list,
                                'POS': POS_list,
                                'REF': REF_list,
                                'ALT': ALT_list,
                                'DP': DP_list,
                                'AD': AD_list,
                                'AF': AF_list,
                                'ENCODE': encode_list,
                                'segDup': segdup_list,
                                'refTriCon': refTriCon_list,
                                },
                               columns=['CHROM', 'POS', 'REF', 'ALT', 'DP', 'AD', 'AF', 'ENCODE', 'segDup',
                                        'refTriCon'])
    temp_path = dir_path+'tmp' + vcfFile + '.csv'
    dataframe_L.to_csv(temp_path, index=False, sep=',')


def mergeCsv(dir_path,labeled_file):
    files = os.listdir(dir_path)  # 获取文件夹下所有文件名
    df1 = pd.read_csv(dir_path + files[0], encoding='gbk')  # 读取首个csv文件，保存到df1中

    for file in files[1:]:
        df2 = pd.read_csv(dir_path + file, encoding='gbk')  # 打开csv文件，注意编码问题，保存到df2中
        df1 = pd.concat([df1, df2], axis=0, ignore_index=True)  # 将df2数据与df1合并

    # df1 = df1.drop_duplicates()   #去重
    # df1 = df1.reset_index(drop=True) #重新生成index
    data = df1
    data.to_csv(labeled_file, index=False)  # 将结果保存为新的csv文件

def mian(vcf_file, black_file, segDup_file, fa_file, labeled_file, p_thread):

    dir_path = split_file(vcf_file,labeled_file,p_thread)
    all_file_path = getPathFile(dir_path)  # 获取目录下所有vcf or vcf.gz文件路径
    tempdir = os.path.dirname(labeled_file)
    tempdir_path = tempdir + '/temp1/'
    os.mkdir(tempdir_path)

    relt = []
    for avFile in all_file_path:  # 遍历处理
        process = multiprocessing.Process(target=processingVariants, args=(avFile, black_file, segDup_file, fa_file, labeled_file))
        process.start()
        relt.append(process)
    for process in relt:
        process.join()

    mergeCsv(tempdir_path,labeled_file)
    shutil.rmtree(dir_path)
    shutil.rmtree(tempdir_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--vcf', help='input vcf file', required=True)
    parser.add_argument('-b', '--blacklist', help='input encode blacklist file', required=True)
    parser.add_argument('-d', '--segDup', help='input a known segmental duplication file', required=True)
    parser.add_argument('-f', '--fasta', help='input fasta file', required=True)
    parser.add_argument('-o', '--out', help='output labeled csv file', required=True)
    parser.add_argument('-p', '--threads', help='Number of multiprocesses threads', required=True, type=int)

    # # 创建一个logger
    logger = logging.getLogger('mylogger')
    logger.setLevel(logging.DEBUG)
    # 创建一个handler，用于写入日志文件
    fh = logging.FileHandler('sherwin_assess.log', 'w')
    fh.setLevel(logging.DEBUG)
    # # 再创建一个handler，用于输出到控制台
    # ch = logging.StreamHandler()
    # ch.setLevel(logging.DEBUG)
    # # 定义handler的输出格式
    formatter = logging.Formatter('[%(asctime)s][%(thread)d][%(filename)s][%(levelname)s] %(message)s')
    fh.setFormatter(formatter)
    # ch.setFormatter(formatter)
    # # 给logger添加handler
    logger.addHandler(fh)
    # logger.addHandler(ch)

    # args1 = parser.parse_args()
    # vcf_file = os.path.abspath(args1.vcf)
    # knowns_file = os.path.abspath(args1.knowns)
    args = parser.parse_args()
    vcf_file = os.path.abspath(args.vcf)
    black_file = os.path.abspath(args.blacklist)
    segDup_file = os.path.abspath(args.segDup)
    fa_file = os.path.abspath(args.fasta)
    labeled_file = os.path.abspath(args.out)
    p_thread = args.threads

    # log_file=os.path.abspath(args.logging_file)

    # logger.info('\n[ the number of process is  %s]',pro_num)
    logger.info('\n[ start time: %s]', time.asctime(time.localtime(time.time())))

    mian(vcf_file, black_file, segDup_file, fa_file, labeled_file, p_thread)

    logger.info('\n[ end time: %s]', time.asctime(time.localtime(time.time())))
