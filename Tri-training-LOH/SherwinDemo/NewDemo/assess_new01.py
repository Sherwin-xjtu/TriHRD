#!/usr/bin/python
# coding=utf-8
from __future__ import division
import logging
import numpy as np
from multiprocessing import *
from multiprocessing import Pool
import pysam
import argparse
import logging
import vcf
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

    print 'start'
    for record in new_vcfreader:
        nlt.append(record)

    one_lenth = int(len(nlt) / int(p)) + 1
    nlt_arr = spfu(nlt, one_lenth)
    k = -1

    print "start multiprocessing"
    for i in nlt_arr:
        k = k + 1
        process = multiprocessing.Process(target=compvcf, args=(mlt, i, k, return_dict))
        process.start()
        relt.append(process)
    print "end multiprocessing"
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

def split_file(vcffile):
    i = 0  # 设置计数器
    vcf_reader = vcf.Reader(open(vcffile, 'r'))
    b = os.path.dirname(vcffile)
    os.mkdir(b + '/temp')
    dir_path = b+'/temp/'

    with open(vcffile) as f:
        text = f.read()

    f1 = file(vcffile, 'r')
    hi = 0
    for line in f1.readlines():
        if line.startswith('#'):
            hi = hi + 1
        else:
            break
    length = len(text.splitlines())-hi
    while i < length:  # 这里12345表示文件行数，如果不知道行数可用每行长度等其他条件来判断
        vcf_writer = vcf.Writer(open(dir_path+'tmp' + str(i) + '.vcf', 'w'), vcf_reader)
        # with open('newfile'+str(i),'w') as f1:
        for j in range(0, 1000):  # 这里设置每个子文件的大小
            if i < length:  # 这里判断是否已结束，否则最后可能报错
                # f1.writelines(f.readline())
                vcf_writer.write_record(vcf_reader.next())
                i = i + 1
            else:
                break
    return dir_path

def mian(vcf_file, knowns_file, p_thread, logger):
    dir_path = split_file(vcf_file)
    all_file_path = getPathFile(dir_path)  # 获取目录下所有pcap文件路径
    m_vcfreader = pysam.VariantFile(knowns_file)
    n = 0
    mlt = ()
    sum_ls = []
    lk = []
    p = p_thread
    for record2 in m_vcfreader.fetch():
        if 'PASS' in record2.filter.keys():
            mlt = mlt + (record2,)
            n = n + 1
    reutrn_result = []
    for file in all_file_path:  # 遍历处理
        result = Assess(file, mlt, p)  # 单个vcf文件处理，可将本函数替换成自定义的功能，便可实现批量处理
        reutrn_result.append(result)

    for return_dict in reutrn_result:
        for i in return_dict.keys():
            lk.append(return_dict[i])
        sum_ls = np.sum(lk, axis=0)
    sensitivity = sum_ls[0] / n
    print ('FET>5 and VAFN < 0.02: %s ,platypus: %s ,VAFC < 0.01: %s ,mutect2: %s, sensitivity: %s', sum_ls[1], sum_ls[0],sum_ls[2], n, sensitivity)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--vcf', help='input vcf file of which need to be assessed', required=True)
    parser.add_argument('-k', '--knowns', help='input the truth sites vcf files', required=True)
    parser.add_argument('-p', '--threads', help='Number of multiprocesses threads', required=True, type=int)
    # parser.add_argument('-ou', '--outu', help='output unlabled vcf file', required=True)
    # parser.add_argument('-l', '--logging_file', help='the logging file',required=True)

    # 创建一个logger
    logger = logging.getLogger('mylogger')
    logger.setLevel(logging.DEBUG)
    # 创建一个handler，用于写入日志文件
    fh = logging.FileHandler('sherwin_assess.log', 'w')
    fh.setLevel(logging.DEBUG)
    # 再创建一个handler，用于输出到控制台
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # 定义handler的输出格式
    formatter = logging.Formatter('[%(asctime)s][%(thread)d][%(filename)s][%(levelname)s] %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # 给logger添加handler
    logger.addHandler(fh)
    logger.addHandler(ch)

    args1 = parser.parse_args()
    vcf_file = os.path.abspath(args1.vcf)
    knowns_file = os.path.abspath(args1.knowns)
    p_thread = args1.threads

    # log_file=os.path.abspath(args.logging_file)

    # logger.info('\n[ the number of process is  %s]',pro_num)
    logger.info('\n[ start time: %s]', time.asctime(time.localtime(time.time())))

    mian(vcf_file, knowns_file, p_thread, logger)

    logger.info('\n[ end time: %s]', time.asctime(time.localtime(time.time())))
