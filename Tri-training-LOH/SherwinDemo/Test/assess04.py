# coding=utf-8

from __future__ import division  # 用于/相除的时候,保留真实结果.小数
# import pysam
import argparse
import gzip
import logging
import vcf
# import pysam
import pandas as pd
import numpy as np
from numpy import *
import tabix
import pysam
# from log_config import Config
import csv, os, argparse, string, sys, multiprocessing, logging, functools, time, signal, re

sys.dont_write_bytecode = True
csv.register_dialect("line_terminator", lineterminator="\n")
VERSION = '1.0.1'


class Process_data:
    def __init__(self, args):
        self.data_vcf = args[0]
        self.m_vcf = args[1]
        self.out_vcf1 = args[2]
        self.out_vcf2 = args[3]
        self.out_vcf3 = args[4]
    def compvcf(self,nlt,mlt,vcf_writer1,vcf_writer2,vcf_writer3,n,n1):
        li = []
        lt = []
        j = 0
        sensitivity = 0
        specificity = 0
        for record1 in nlt:
            for record in mlt:
                if record.pos == record1.POS and record.chrom == record1.CHROM and record.ref == record1.REF:
                    for ra in record1.ALT:
                        ra = ra.sequence
                        if ra in record.alts:
                            record1.add_info('MAF',record.samples[0]['AF'])
                            lt.append(record1)
                            j += 1
                            li.append(record)
                            break
        for rec1 in mlt:
            if rec1 not in li:
                vcf_writer1.write(rec1)
        for rec2 in nlt:
            if rec2 not in lt:
                vcf_writer2.write_record(rec2)
        for rec3 in lt:
            vcf_writer3.write_record(rec3)
            sensitivity = j/n
            specificity = j/n1
        print ('platypus: %s ,mutect2: %s, sensitivity: %s'%(j, n, sensitivity))	
    def processing_datas(self, vcf_in, mt_vcf,n):
        j = 0
        sensitivity = 0
        cc =0
        for record in vcf_in:
            try:
                pos = record.POS
                t = record.POS+1
                records = mt_vcf.querys(record.CHROM+':'+str(pos)+'-'+str(t))
                for rec in records:
                    rec_ref = rec[3]
                    rec_alts = rec[4].split(',')
                    for alt in record.ALT:
                        alt_seq = alt.sequence
                        if alt_seq in rec_alts and rec_ref == record.REF:
                            j = j+1
			
            except tabix.TabixError:
                continue
        sensitivity = j/n
        print ('platypus: %s ,mutect2: %s, sensitivity: %s'%(j, n, sensitivity))
 
    def processing(self):
        data_vcf = self.data_vcf
        m_vcf = self.m_vcf
        mreader = pysam.VariantFile(m_vcf,'rb')
        vcf_in = vcf.Reader(open(data_vcf, 'rb'))
	
        out_vcf1 = self.out_vcf1
        out_vcf2 = self.out_vcf2
        out_vcf3 = self.out_vcf3
        vcf_writer1 = pysam.VariantFile(out_vcf1, "w", header=mreader.header)
        vcf_writer2 = vcf.Writer(open(out_vcf2, 'w'), vcf_in)
        vcf_writer3 = vcf.Writer(open(out_vcf3, 'w'), vcf_in)
        n = 0
        n1= 0
        
        mlt = []
        nlt = []
        for rec in mreader.fetch():
            if rec.samples[0]['AF'][0] > 0.02 and rec.samples[1]['AD'][1] == 0 and rec.samples[0]['AD'][1] > 4:
                for alt in rec.alts:
                    # remove indel with too much length
                    if abs(len(rec.ref)-len(alt)) < 10:
	    	        mlt.append(rec)
	    	        n = n +1	
	for rec1 in vcf_in:
	    nlt.append(rec1)
            n1 = n1 + 1
        #mt_vcf = tabix.open(m_vcf)
        #self.processing_datas(vcf_in, mt_vcf,n)
	#vcf_in1 = vcf.Reader(open(data_vcf, 'rb'))
        self.compvcf(nlt,mlt,vcf_writer1,vcf_writer2,vcf_writer3,n,n1)
	vcf_writer1.close()
	vcf_writer2.close()
	vcf_writer3.close()



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--vcf', help='input vcf file', required=True)
    parser.add_argument('-k', '--knowns', help='input vcf file', required=True)
    parser.add_argument('-o1', '--out1', help='output vcf file', required=True)
    parser.add_argument('-o2', '--out2', help='output vcf file', required=True)
    parser.add_argument('-o3', '--out3', help='output vcf file', required=True)
    args = parser.parse_args()
    vcf_file = os.path.abspath(args.vcf)
    m_file = os.path.abspath(args.knowns)
    out_file1 = os.path.abspath(args.out1)
    out_file2 = os.path.abspath(args.out2)
    out_file3 = os.path.abspath(args.out3)
    
    logger = logging.getLogger('mylogger')
    logger.setLevel(logging.DEBUG)
    # 创建一个handler，用于写入日志文件
    fh = logging.FileHandler('assess.log', 'w')
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
    #logger.info('\nprogram pre_data started in %s with command: %s', os.getcwd(), ' '.join(sys.argv))
    #logger.info('\n[ start time: %s]',time.asctime( time.localtime(time.time()) ))
    args_ = [vcf_file, m_file,out_file1,out_file2,out_file3]
    process_data = Process_data(args_)
    process_data.processing()
    print 'Assessment has completed!'
    #logger.info('\n[ end time: %s]',time.asctime( time.localtime(time.time()) ))
