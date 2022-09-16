#!/usr/bin/python
# coding=utf-8
import argparse
import getopt
import multiprocessing
import os
import re
import sys
import vcf
import numpy as np

def RWMAF(mutectMAF,platyusMAF,onlySites1,onlySites2,overlapSites):
    fr1 = open(mutectMAF,'r') #如果文件不是uft-8编码方式，读取文件可能报错
    fr2 = open(platyusMAF, 'r')  # 如果文件不是uft-8编码方式，读取文件可能报错
    fw1 = open(onlySites1, 'w') #清空文件内容再写
    fw2 = open(onlySites2, 'w')  # 清空文件内容再写
    fw3 = open(overlapSites, 'w')  # 清空文件内容再写
    # # print(f.read()) #返回一个字符串，读取文件所有内容
    # # print(f.readlines()) #返回list，文件的每一行作为list的一个字符串元素
    # # print(f.readline()) #读取一行
    n = 0
    j = 0
    li1 = []
    li2 = []
    header = []
    overlapSitesList1 = []
    overlapSitesList2 = []
    for buff1 in fr1.readlines():
        li1.append(buff1)
    for buff2 in fr2.readlines():
        li2.append(buff2)
    for buff1 in li1:
        buff1 = buff1.rstrip()
        buff1 = buff1.strip('"')
        # buff = buff.replace('GL', 'GLL')
        if "#" not in buff1 and "Hugo_Symbol" not in buff1:
            buff1 = buff1.replace('"','')
            buffList1 = buff1.split()
            for buff2 in li2:
                buff2 = buff2.rstrip()
                buff2 = buff2.strip('"')
                # buff = buff.replace('GL', 'GLL')
                if "#" not in buff2 and "Hugo_Symbol" not in buff2:
                    buff2 = buff2.replace('"', '')
                    buffList2 = buff2.split()
                    if buffList1[5] == buffList2[5] and buffList1[6] == buffList2[6]:
                        overlapSitesList1.append(buffList1)
                        overlapSitesList2.append(buffList2)
                        break

    for site1 in li1:
        site1 = site1.rstrip()
        site1 = site1.strip('"')
        # buff = buff.replace('GL', 'GLL')
        if "#" not in site1 and "Hugo_Symbol" not in site1:
            site1 = site1.replace('"', '')
            site1 = site1.split()
            if site1 not in overlapSitesList1:
                newBuff1 = '\t'.join(site1) + '\n'
                fw1.write(newBuff1)
        else:
            site1 = site1.rstrip()
            site1 = site1.strip('"')
            site1 = site1.replace('"', '')
            site1 = site1.split()
            newBuff1 = '\t'.join(site1) + '\n'
            fw1.write(newBuff1)
    for site2 in li2:
        site2 = site2.rstrip()
        site2 = site2.strip('"')
        # buff = buff.replace('GL', 'GLL')
        if "#" not in site2 and "Hugo_Symbol" not in site2:
            site2 = site2.replace('"', '')
            site2 = site2.split()
            if site2 not in overlapSitesList2:
                newBuff2 = '\t'.join(site2) + '\n'
                fw2.write(newBuff2)
        else:
            site2 = site2.rstrip()
            site2 = site2.strip('"')
            site2 = site2.replace('"', '')
            site2 = site2.split()
            newBuff2 = '\t'.join(site2) + '\n'

            fw2.write(newBuff2)
            fw3.write(newBuff2)
    for site3 in overlapSitesList1:
        newBuff3 = '\t'.join(site3) + '\n'
        fw3.write(newBuff3)
    fw1.close()
    fw2.close()
    fw3.close()

            # print buffList[5],buffList[6],buffList[5]
            # buffList[8] = "GT:GLL:GOF:GQ:DP:AD:ONV:AF"
            # AFStr = "VAFC"
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # parser.add_argument('-v1', '--maf1', help='input mutect maf1 file', required=True)
    # parser.add_argument('-v2', '--maf2', help='input platyus maf2 file', required=True)
    # parser.add_argument('-o1', '--out1', help='output sites only in maf1', required=True)
    # parser.add_argument('-o2', '--out2', help='output sites only in maf2', required=True)
    # parser.add_argument('-o3', '--out3', help='output sites both in maf1 and maf2', required=True)
    # args = parser.parse_args()
    # mutectMAF = os.path.abspath(args.maf1)
    # platyusMAF = os.path.abspath(args.maf2)
    # onlySites1 = os.path.abspath(args.out1)
    # onlySites2 = os.path.abspath(args.out2)
    # overlapSites = os.path.abspath(args.out3)

    mutectMAF = 'C:/Users/Sherwin/Desktop/maf/m2.somatic.maf'
    platyusMAF = 'C:/Users/Sherwin/Desktop/maf/somatic_filter.maf'

    onlySites1 = 'C:/Users/Sherwin/Desktop/maf/onlySites1.maf'
    onlySites2 = 'C:/Users/Sherwin/Desktop/maf/onlySites2.maf'
    overlapSites = 'C:/Users/Sherwin/Desktop/maf/overlapSites.maf'
    # standerVcf(vcf_file, out_file)
    RWMAF(mutectMAF,platyusMAF,onlySites1,onlySites2,overlapSites)
