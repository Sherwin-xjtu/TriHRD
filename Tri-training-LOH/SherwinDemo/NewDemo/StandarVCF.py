#!/usr/bin/python
# coding=utf-8
import argparse
import getopt
import multiprocessing
import os
import re
import sys

import vcf
import pysam
import numpy as np


# new_vcfreader = vcf.Reader(open(pvcf, 'r'))
# vcf_writer = vcf.Writer(open(new_vcffile, 'w'), new_vcfreader)
# for rec in new_vcfreader:
#     # rec.add_info('MAF', 1)
#     print rec.samples
#     break
# IN = open('C:/Users/Sherwin/Desktop/TMB/A_TMB_2_10.vcf')
# for buff in IN:
#     buff = buff.rstrip()
#     if buff[0] != '#':
#         c = buff.split()
#         vcf_writer.write_record()
#         break
# #
def standerVcf(pvcf,new_vcffile):
    fr = open(pvcf,'r') #如果文件不是uft-8编码方式，读取文件可能报错
    fw = open(new_vcffile, 'w') #清空文件内容再写
    # # print(f.read()) #返回一个字符串，读取文件所有内容
    # # print(f.readlines()) #返回list，文件的每一行作为list的一个字符串元素
    # # print(f.readline()) #读取一行
    n = 0
    j = 0
    for buff in fr:
        buff = buff.rstrip()
        buff = buff.strip('"')
        buff = buff.replace('GL', 'GLL')
        if "#" not in buff:
            buff = buff.replace('"','')
            buffList = buff.split()

            buffList[8] = "GT:GLL:GOF:GQ:DP:AD:ONV:AF"
            AFStr = "VAFC"
            AFm = re.search(AFStr + "=([^;]+)", buff)
            if AFm:
                AF = AFm.group(1)
            else:
                AF = 0
            NorAFStr = "VAFN"
            NorAFStrm = re.search(NorAFStr + "=([^;]+)", buff)
            if NorAFStrm:
                NorAF = NorAFStrm.group(1)
            else:
                NorAF = 0
            buffList[9] = buffList[9]+":"+AF
            buffList[10] = buffList[10] + ":" + NorAF
            newBuff = '\t'.join(buffList)+'\n'
            fw.write(newBuff)
        else:
            if buff[:8] == "##FORMAT" and n == 0:
                buff = buff.replace('""', '"')

                n +=1
                fw.write('##INFO=<ID=ACN,Number=1,Type=Integer,Description="Not know">' + '\n')
                fw.write('##FORMAT=<ID=DP,Number=.,Type=Integer,Description="Number of reads covering variant location in this sample">'+'\n')
                fw.write('##FORMAT=<ID=AF,Number=.,Type=Float,Description="Variant frequency of cancer">'+'\n')
                fw.write('##FORMAT=<ID=AD,Number=.,Type=Integer,Description="Number of reads containing variant in this sample">'+'\n')
                fw.write('##FORMAT=<ID=ONV,Number=.,Type=Integer,Description="Raw number of reads containing variant in this sample">' + '\n')
                fw.write(buff + '\n')
                # fw.write('##FORMAT=<ID=GLL,Number=.,Type=Float,Description="Genotype log10-likelihoods for AA,AB and BB genotypes, where A = ref and B = variant. Only applicable for bi-allelic sites">' + '\n')

            elif buff[:8] == "##FILTER" and j == 0:
                # print buff[:7]
                j +=1
                fw.write('##contig=<ID=1,length=249250621>'+'\n')
                fw.write('##contig=<ID=2,length=243199373>'+'\n')
                fw.write('##contig=<ID=3,length=198022430>'+'\n')
                fw.write('##contig=<ID=4,length=191154276>'+'\n')
                fw.write('##contig=<ID=5,length=180915260>'+'\n')
                fw.write('##contig=<ID=6,length=171115067>'+'\n')
                fw.write('##contig=<ID=7,length=159138663>'+'\n')
                fw.write('##contig=<ID=8,length=146364022>'+'\n')
                fw.write('##contig=<ID=9,length=141213431>'+'\n')
                fw.write('##contig=<ID=10,length=135534747>'+'\n')
                fw.write('##contig=<ID=11,length=135006516>'+'\n')
                fw.write('##contig=<ID=12,length=133851895>'+'\n')
                fw.write('##contig=<ID=13,length=115169878>'+'\n')
                fw.write('##contig=<ID=14,length=107349540>'+'\n')
                fw.write('##contig=<ID=15,length=102531392>'+'\n')
                fw.write('##contig=<ID=16,length=90354753>'+'\n')
                fw.write('##contig=<ID=17,length=81195210>'+'\n')
                fw.write('##contig=<ID=18,length=78077248>'+'\n')
                fw.write('##contig=<ID=19,length=59128983>'+'\n')
                fw.write('##contig=<ID=20,length=63025520>'+'\n')
                fw.write('##contig=<ID=21,length=48129895>'+'\n')
                fw.write('##contig=<ID=22,length=51304566>'+'\n')
                fw.write('##contig=<ID=X,length=155270560>'+'\n')
                fw.write('##contig=<ID=Y,length=59373566>'+'\n')
                fw.write('##contig=<ID=MT,length=16569>'+'\n')
                fw.write('##contig=<ID=GL000207.1,length=4262>'+'\n')
                fw.write('##contig=<ID=GL000226.1,length=15008>'+'\n')
                fw.write('##contig=<ID=GL000229.1,length=19913>'+'\n')
                fw.write('##contig=<ID=GL000231.1,length=27386>'+'\n')
                fw.write('##contig=<ID=GL000210.1,length=27682>'+'\n')
                fw.write('##contig=<ID=GL000239.1,length=33824>'+'\n')
                fw.write('##contig=<ID=GL000235.1,length=34474>'+'\n')
                fw.write('##contig=<ID=GL000201.1,length=36148>'+'\n')
                fw.write('##contig=<ID=GL000247.1,length=36422>'+'\n')
                fw.write('##contig=<ID=GL000245.1,length=36651>'+'\n')
                fw.write('##contig=<ID=GL000197.1,length=37175>'+'\n')
                fw.write('##contig=<ID=GL000203.1,length=37498>'+'\n')
                fw.write('##contig=<ID=GL000246.1,length=38154>'+'\n')
                fw.write('##contig=<ID=GL000249.1,length=38502>'+'\n')
                fw.write('##contig=<ID=GL000196.1,length=38914>'+'\n')
                fw.write('##contig=<ID=GL000248.1,length=39786>'+'\n')
                fw.write('##contig=<ID=GL000244.1,length=39929>'+'\n')
                fw.write('##contig=<ID=GL000238.1,length=39939>'+'\n')
                fw.write('##contig=<ID=GL000202.1,length=40103>'+'\n')
                fw.write('##contig=<ID=GL000234.1,length=40531>'+'\n')
                fw.write('##contig=<ID=GL000232.1,length=40652>'+'\n')
                fw.write('##contig=<ID=GL000206.1,length=41001>'+'\n')
                fw.write('##contig=<ID=GL000240.1,length=41933>'+'\n')
                fw.write('##contig=<ID=GL000236.1,length=41934>'+'\n')
                fw.write('##contig=<ID=GL000241.1,length=42152>'+'\n')
                fw.write('##contig=<ID=GL000243.1,length=43341>'+'\n')
                fw.write('##contig=<ID=GL000242.1,length=43523>'+'\n')
                fw.write('##contig=<ID=GL000230.1,length=43691>'+'\n')
                fw.write('##contig=<ID=GL000237.1,length=45867>'+'\n')
                fw.write('##contig=<ID=GL000233.1,length=45941>'+'\n')
                fw.write('##contig=<ID=GL000204.1,length=81310>'+'\n')
                fw.write('##contig=<ID=GL000198.1,length=90085>'+'\n')
                fw.write('##contig=<ID=GL000208.1,length=92689>'+'\n')
                fw.write('##contig=<ID=GL000191.1,length=106433>'+'\n')
                fw.write('##contig=<ID=GL000227.1,length=128374>'+'\n')
                fw.write('##contig=<ID=GL000228.1,length=129120>'+'\n')
                fw.write('##contig=<ID=GL000214.1,length=137718>'+'\n')
                fw.write('##contig=<ID=GL000221.1,length=155397>'+'\n')
                fw.write('##contig=<ID=GL000209.1,length=159169>'+'\n')
                fw.write('##contig=<ID=GL000218.1,length=161147>'+'\n')
                fw.write('##contig=<ID=GL000220.1,length=161802>'+'\n')
                fw.write('##contig=<ID=GL000213.1,length=164239>'+'\n')
                fw.write('##contig=<ID=GL000211.1,length=166566>'+'\n')
                fw.write('##contig=<ID=GL000199.1,length=169874>'+'\n')
                fw.write('##contig=<ID=GL000217.1,length=172149>'+'\n')
                fw.write('##contig=<ID=GL000216.1,length=172294>'+'\n')
                fw.write('##contig=<ID=GL000215.1,length=172545>'+'\n')
                fw.write('##contig=<ID=GL000205.1,length=174588>'+'\n')
                fw.write('##contig=<ID=GL000219.1,length=179198>'+'\n')
                fw.write('##contig=<ID=GL000224.1,length=179693>'+'\n')
                fw.write('##contig=<ID=GL000223.1,length=180455>'+'\n')
                fw.write('##contig=<ID=GL000195.1,length=182896>'+'\n')
                fw.write('##contig=<ID=GL000212.1,length=186858>'+'\n')
                fw.write('##contig=<ID=GL000222.1,length=186861>'+'\n')
                fw.write('##contig=<ID=GL000200.1,length=187035>'+'\n')
                fw.write('##contig=<ID=GL000193.1,length=189789>'+'\n')
                fw.write('##contig=<ID=GL000194.1,length=191469>'+'\n')
                fw.write('##contig=<ID=GL000225.1,length=211173>'+'\n')
                fw.write('##contig=<ID=GL000192.1,length=547496>'+'\n')
                fw.write('##contig=<ID=NC_007605,length=171823>'+'\n')
                fw.write('##contig=<ID=hs37d5,length=35477943>'+'\n')
            else:
                buff = buff.replace('""','"')
                fw.write(buff+'\n')
    fw.close()

# new_vcfreader = vcf.Reader(open('C:/Users/Sherwin/Desktop/TMB/A_TMB_2_10_filter_new.vcf', 'r'))
# print new_vcfreader
# for rec in new_vcfreader:
#     print rec.samples

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--vcf', help='input vcf file', required=True)
    # parser.add_argument('-k', '--knowns', help='input vcf file', required=True)
    parser.add_argument('-o', '--out', help='output the stander vcf file', required=True)
    # parser.add_argument('-o2', '--out2', help='output vcf file', required=True)
    # parser.add_argument('-o3', '--out3', help='output vcf file', required=True)
    args = parser.parse_args()
    vcf_file = os.path.abspath(args.vcf)
    # m_file = os.path.abspath(args.knowns)
    out_file = os.path.abspath(args.out)
    # out_file2 = os.path.abspath(args.out2)
    # out_file3 = os.path.abspath(args.out3)

    standerVcf(vcf_file, out_file)