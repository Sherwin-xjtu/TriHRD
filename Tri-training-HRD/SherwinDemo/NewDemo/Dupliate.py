#!/usr/bin/python
# coding=utf-8
from __future__ import division
import logging
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

class DupliateAndAssess:
    def __init__(self, args):
        self.inputvcf = args[0]
        self.outvcf = args[1]
        self.logger = args[2]

    def Dupliate(self, vcffile, new_vcffile):
        vcf_reader = vcf.Reader(open(vcffile, 'r'))
        vcf_writer = vcf.Writer(open(new_vcffile, 'w'), vcf_reader)
        # rec.add_info('biao',2)
        # print rec.INFO['BRF']

        record_ = []
        for record in vcf_reader:
            if len(record.REF) >1:
                if len(record.REF) == 2:
                    for altv in record.ALT:
                        altvs = altv.sequence
                        if len(altvs) == 2:
                            new_pos = record.POS + len(record.REF[1:-1]) + 1
                            if record.REF[0] != altvs[0]:
                                new_record1 = copy.copy(record)
                                new_record1.REF = record.REF[0]
                                new_record1.ALT = altvs[0]
                                tmpli = []
                                tmpli.append(new_record1.POS)
                                tmpli.append(new_record1.REF)
                                tmpli.append(new_record1.ALT)
                                if tmpli not in record_:
                                    record_.append(tmpli)
                                    vcf_writer.write_record(new_record1)
                            if record.REF[-1] != altvs[-1]:
                                new_record2 = copy.copy(record)
                                new_record2.REF = record.REF[-1]
                                new_record2.ALT = altvs[-1]
                                new_record2.POS = new_pos
                                tmpli = []
                                tmpli.append(new_record2.POS)
                                tmpli.append(new_record2.REF)
                                tmpli.append(new_record2.ALT)
                                if tmpli not in record_:
                                    record_.append(tmpli)
                                    vcf_writer.write_record(new_record2)

                elif len(record.REF) > 2:
                    for altv in record.ALT:
                        altvs = altv.sequence
                        if len(altvs) > 2 and record.REF[1:-1] == altvs[1:-1]:
                            new_pos = record.POS + len(record.REF[1:-1]) + 1
                            if record.REF[0] != altvs[0]:
                                new_record1 = copy.copy(record)
                                new_record1.REF = record.REF[0]
                                new_record1.ALT = altvs[0]
                                tmpli = []
                                tmpli.append(new_record1.POS)
                                tmpli.append(new_record1.REF)
                                tmpli.append(new_record1.ALT)
                                if tmpli not in record_:
                                    record_.append(tmpli)
                                    vcf_writer.write_record(new_record1)
                            if record.REF[-1] != altvs[-1]:
                                new_record2 = copy.copy(record)
                                new_record2.REF = record.REF[-1]
                                new_record2.ALT = altvs[-1]
                                new_record2.POS = new_pos
                                tmpli = []
                                tmpli.append(new_record2.POS)
                                tmpli.append(new_record2.REF)
                                tmpli.append(new_record2.ALT)
                                if tmpli not in record_:
                                    record_.append(tmpli)
                                    vcf_writer.write_record(new_record2)
            else:
                tmpli = []
                tmpli.append(record.POS)
                tmpli.append(record.REF)
                tmpli.append(record.ALT)
                if tmpli not in record_:
                    record_.append(tmpli)
                    vcf_writer.write_record(record)

        vcf_writer.close()
        self.logger.info("Duplication completed!")

    def processing(self):
        invcf = self.inputvcf
        ovcf = self.outvcf

        self.Dupliate(invcf, ovcf)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--vcf', help='input vcf file of which need to be duplicated or assessed', required=True)
    parser.add_argument('-out', '--out', help='output vcf file of which has being duplicated or assessed',
                        required=True)
    # parser.add_argument('-k', '--knowns', help='input the truth sites vcf files', required=True)
    # parser.add_argument('-ol', '--outl', help='output labeled vcf file',required=True)
    # parser.add_argument('-ou', '--outu', help='output unlabled vcf file', required=True)
    # parser.add_argument('-l', '--logging_file', help='the logging file',required=True)

    # 创建一个logger
    logger = logging.getLogger('mylogger')
    logger.setLevel(logging.DEBUG)
    # 创建一个handler，用于写入日志文件
    fh = logging.FileHandler('Sherwin.log', 'w')
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

    args = parser.parse_args()
    vcf_file = os.path.abspath(args.vcf)
    # knowns_file = os.path.abspath(args.knowns)
    out_file = os.path.abspath(args.out)
    # log_file=os.path.abspath(args.logging_file)

    # logger.info('\n[ the number of process is  %s]',pro_num)
    logger.info('\n[ start time: %s]', time.asctime(time.localtime(time.time())))
    args_ = [vcf_file, out_file, logger]
    DupliateAndAssess = DupliateAndAssess(args_)
    DupliateAndAssess.processing()
    logger.info('\n[ end time: %s]', time.asctime(time.localtime(time.time())))
