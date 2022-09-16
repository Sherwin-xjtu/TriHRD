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
        rec = vcf_reader.next()
        # rec.add_info('biao',2)
        # print rec.INFO['BRF']
        vcf_writer.write_record(rec)
        i = 0

        for record in vcf_reader:
            i = i + 1
            if i != 1:
                if record.CHROM == copy_record.CHROM and record.POS == copy_record.POS and record.ALT == copy_record.ALT and record.REF == copy_record.REF:
                    pass
                else:
                    if len(record.REF) > 2:
                        for altv in record.ALT:
                            altvs = altv.sequence
                            if len(altvs) > 2 and record.REF[1:-1] == altvs[1:-1]:
                                new_pos = record.POS + len(record.REF[1:-1]) + 1
                                if record.REF[0] != altvs[0]:
                                    new_record1 = copy.copy(record)
                                    new_record1.REF = record.REF[0]
                                    new_record1.ALT = altvs[0]
                                    vcf_writer.write_record(new_record1)
                                new_record2 = copy.copy(record)
                                if record.REF[-1] != altvs[-1]:
                                    new_record2.REF = record.REF[-1]
                                    new_record2.ALT = altvs[-1]
                                    new_record2.POS = new_pos
                                    vcf_writer.write_record(new_record2)

                    else:
                        vcf_writer.write_record(record)
            else:
                vcf_writer.write_record(record)
            copy_record = record

        vcf_writer.close()
        self.logger.info("Duplication completed!")

    def Assess(self, pvcf, m_vcf):
        new_vcfreader = vcf.Reader(open(pvcf, 'r'))
        m_vcfreader = pysam.VariantFile(m_vcf)

        nlt = []
        mlt = []
        n = 0
        a = 0
        b = 0
        c = 0
        d = 0
        sensitivity = 0
        for record in new_vcfreader:
            nlt.append(record)

        for recc in m_vcfreader.fetch():

            if recc.filter == [] or recc.filter == 'PASS':
                n = n + 1
                mlt.append(recc)
        for record2 in mlt:
            for record1 in nlt:
                if record1.CHROM == record2.chrom and record1.POS == record2.pos:
                    c = c + 1
                    if 'FET' in record1.INFO:
                        if record1.INFO['FET'][0] > 5 and record1.INFO['VAFN'][0] < 0.02:
                            a = a + 1
                            if record1.INFO['VAFC'][0] < 0.01:
                                d = d + 1
                if record1.CHROM == record2.chrom and record1.POS == record2.pos and record1.ALT == record2.alts and record1.REF == record2.ref and record1.FILTER == record2.filter:
                    b = b + 1

        self.logger.info('FET>5 and VAFN < 0.02: %s ,platypus: %s ,VAFC < 0.01: %s ,mutect2: %s', a, c, d, n)

    def processing(self):
        invcf = self.inputvcf
        ovcf = self.outvcf

        self.Dupliate(invcf, ovcf)
        # self.Assess(ovcf, mvcf)


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
