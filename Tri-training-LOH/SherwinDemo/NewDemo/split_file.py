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
    sensitivity = 0
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


def tupaend(record, nlt):
    nlt = nlt + (record,)


# return a,c,d
def Assess(pvcf, new_vcffile, threads, logger):
    new_vcfreader = vcf.Reader(open(pvcf, 'r'))
    # m_vcfreader = pysam.VariantFile(m_vcf)
    vcf_writer = vcf.Writer(open(new_vcffile, 'w'), new_vcfreader)
    rec = new_vcfreader.next()
    # rec.add_info('biao',2)
    # print rec.INFO['BRF']
    vcf_writer.write_record(rec)
    i = 0
    nr = 4217200
    n = nr/100
    l1 = []
    for record in new_vcfreader:
        if i < n:
            l1.append(record)

        i = i + 1

        vcf_writer.write_record(record)
        copy_record = record

    vcf_writer.close()

    mlt = ()
    nlt = ()
    relt = []
    nelt = []
    p = threads
    n = 0
    manager = Manager()
    return_dict = manager.dict()

    pl = Pool(p)

    print 'start'
    for record in new_vcfreader:
        nlt = nlt + (record,)
    # for record in new_vcfreader:
    #	    print record
    #   pl.apply_async(tupaend, args=(record,nlt))
    # pl.close()
    # pl.join()

    # v = -1
    print 'start'
    # for record in new_vcfreader:
    # v = v + 1
    # process = multiprocessing.Process(target=self.tupappend, args=(record,v))
    # process.start()
    # nelt.append(process)

    print "Sub-process(es) done."

    for record2 in m_vcfreader.fetch():
        if 'PASS' in record2.filter.keys():
            mlt = mlt + (record2,)
            n = n + 1
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
    lk = []
    sum_ls = []
    for i in range(p):
        lk.append(return_dict[i])
    sum_ls = np.sum(lk, axis=0)
    sensitivity = sum_ls[0] / n
    logger.info('FET>5 and VAFN < 0.02: %s ,platypus: %s ,VAFC < 0.01: %s ,mutect2: %s, sensitivity: %s',
                sum_ls[1], sum_ls[0], sum_ls[2], n, sensitivity)


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

    Assess(vcf_file, knowns_file, p_thread, logger)

    logger.info('\n[ end time: %s]', time.asctime(time.localtime(time.time())))
