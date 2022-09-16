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

def readBed(bedFiler):
    fr = open(bedFiler,'r') #如果文件不是uft-8编码方式，读取文件可能报错
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
    return bed
if __name__ == '__main__':

    bedFile = 'C:/Users/Sherwin/Desktop/Project/lowfrefilter/blacklist.b37.bed'
    bed = readBed(bedFile)
    if '2' in bed.keys():
        for pos in bed['2']:
            if 739928 >=pos[0] and 739928 <=pos[1]:

                break