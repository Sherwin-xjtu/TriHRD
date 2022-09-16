#!/usr/bin/python
# coding=utf-8
import argparse
import copy
import logging
import os
from datetime import time

import vcf
from vcf import model

class Base:
    def __init__(self,s,pos):
        self.seq = s
        self.pos = pos

def getNumofCommonSubstr(str1, str2):
    lstr1 = len(str1)
    lstr2 = len(str2)
    record = [[0 for i in range(lstr2 + 1)] for j in range(lstr1 + 1)]  # 多一位
    maxNum = 0  # 最长匹配长度
    p = 0  # 匹配的起始位

    for i in range(lstr1):
        for j in range(lstr2):
            if str1[i] == str2[j]:
                # 相同则累加
                record[i + 1][j + 1] = record[i][j] + 1
                if record[i + 1][j + 1] > maxNum:
                    # 获取最大匹配长度
                    maxNum = record[i + 1][j + 1]
                    # 记录最大匹配长度的终止位置
                    p = i + 1
    return str1[p - maxNum:p], maxNum

def split_snp(str1,str2,record,vcf_writer):
    if (len(str1) != 1 and len(str2) != 1) and (len(str1) == len(str2)):
        for i in range(len(str1)):
            if str1[i] != str2[i]:
                new_record = copy.copy(record)
                new_record.REF = str1[i]
                new_pos = record.POS + i
                new_record.POS = new_pos
                new_record.ALT = [vcf.model._Substitution(str2[i])]
                vcf_writer.write_record(new_record)
            else:
                pass
    else:
        vcf_writer.write_record(record)

def compared(record,vcf_writer):
    for alts in record.ALT:
            alt = alts.sequence
    str1 = record.REF
    str2 = alt
    b = []
    pos = record.POS
    for s in str1:
        b.append(Base(s, pos))
        pos = pos + 1
    cop,n = getNumofCommonSubstr(str1, str2)
    if n != 0 and n != 1:
        str1_arr = str1.split(cop)
        str2_arr = str2.split(cop)
        str1_arr[0] = str1_arr[0] + cop[0]
        str1_arr[1] = cop[-1] + str1_arr[1]
        str2_arr[0] = str2_arr[0] + cop[0]
        str2_arr[1] = cop[-1] + str2_arr[1]
        if (len(str1_arr[0]) != 1 and len(str2_arr[0]) == 1) or (len(str1_arr[0]) == 1 and len(str2_arr[0]) != 1):
            new_record1 = copy.copy(record)
            new_record1.REF = str1_arr[0]
            new_record1.ALT = [vcf.model._Substitution(str2_arr[0])]
            split_snp(str1_arr[0], str2_arr[0], new_record1, vcf_writer)
        elif len(str1_arr[0]) == 1 and len(str2_arr[0]) == 1:
            pass
        else:
            str1_arr10 = str1_arr[0][:-1]
            str2_arr10 = str2_arr[0][:-1]
            cop1l, n1l = getNumofCommonSubstr(str1_arr10, str2_arr10)
            if n1l != 0 and n1l != 1:
                str1_arr0 = str1_arr10.split(cop1l)
                str1_arr0[0] = str1_arr0[0] + cop1l[0]
                str1_arr0[1] = cop1l[-1] + str1_arr0[1]
                str2_arr0 = str2_arr10.split(cop1l)
                str2_arr0[0] = str2_arr0[0] + cop1l[0]
                str2_arr0[1] = cop1l[-1] + str2_arr0[1]
                if (len(str1_arr0[0]) == 1 and len(str2_arr0[0]) != 1) or (len(str1_arr0[0]) != 1 and len(str2_arr0[0]) == 1):
                    new_record1 = copy.copy(record)
                    new_record1.REF = str1_arr0[0]
                    new_record1.ALT = [vcf.model._Substitution(str2_arr0[0])]
                    split_snp(str1_arr0[0], str2_arr0[0], new_record1, vcf_writer)
                    # vcf_writer.write_record(new_record1)
                    if (len(str1_arr0[1]) == 1 and len(str2_arr0[1]) != 1) or (len(str1_arr0[1]) != 1 and len(str2_arr0[1]) == 1):
                        new_record2 = copy.copy(record)
                        new_pos = record.POS
                        new_record2.POS = new_pos + len(str1_arr0[0]) - 2 + n1l
                        new_record2.REF = str1_arr0[1]
                        new_record2.ALT = [vcf.model._Substitution(str2_arr0[1])]
                        # vcf_writer.write_record(new_record2)
                        split_snp(str1_arr0[1], str2_arr0[1], new_record2, vcf_writer)

                    elif len(str1_arr0[1]) == 1 and len(str2_arr0[1]) == 1:
                        pass
                    else:
                        new_record2 = copy.copy(record)
                        new_pos = record.POS
                        new_pos = new_pos + len(str1_arr0[0]) - 2 + n1l + 1
                        new_record2.POS = new_pos
                        new_record2.REF = str1_arr0[1][1:]
                        new_record2.ALT = [vcf.model._Substitution(str2_arr0[1][1:])]
                        # vcf_writer.write_record(new_record2)
                        split_snp(str1_arr0[1][1:], str2_arr0[1][1:], new_record2, vcf_writer)

                elif (len(str1_arr0[0]) == 1 and len(str2_arr0[0]) == 1):
                    pass
                else:
                    new_record1 = copy.copy(record)
                    new_record1.REF = str1_arr0[0][:-1]
                    new_record1.ALT = [vcf.model._Substitution(str2_arr0[0][:-1])]
                    # vcf_writer.write_record(new_record1)
                    split_snp(str1_arr0[0][:-1], str2_arr0[0][:-1], new_record1, vcf_writer)
                    if (len(str1_arr0[1]) == 1 and len(str2_arr0[1]) != 1) or (len(str1_arr0[1]) != 1 and len(str2_arr0[1]) == 1):
                        new_record2 = copy.copy(record)
                        new_pos = record.POS
                        new_record2.POS = new_pos + len(str1_arr0[0]) - 2 + n1l
                        new_record2.REF = str1_arr0[1]
                        new_record2.ALT = [vcf.model._Substitution(str2_arr0[1])]
                        # vcf_writer.write_record(new_record2)
                        split_snp(str1_arr0[1], str2_arr0[1], new_record2, vcf_writer)

                    elif len(str1_arr0[1]) == 1 and len(str2_arr0[1]) == 1:
                        pass
                    else:
                        new_record2 = copy.copy(record)
                        new_pos = record.POS
                        new_pos = new_pos + len(str1_arr0[0]) - 2 + n1l + 1
                        new_record2.POS = new_pos
                        new_record2.REF = str1_arr0[1][1:]
                        new_record2.ALT = [vcf.model._Substitution(str2_arr0[1][1:])]
                        # vcf_writer.write_record(new_record2)
                        split_snp(str1_arr0[1][1:], str2_arr0[1][1:], new_record2, vcf_writer)
                if (len(str1_arr[1]) !=1 and len(str2_arr[1]) == 1) or (len(str1_arr[1]) ==1 and len(str2_arr[1]) != 1):
                    new_record1 = copy.copy(record)
                    new_pos = record.POS
                    new_record1.POS = new_pos + len(str1_arr[0]) - 2 + n
                    new_record1.REF = str1_arr[1]
                    new_record1.ALT = [vcf.model._Substitution(str2_arr[1])]
                    # vcf_writer.write_record(new_record1)
                    split_snp(str1_arr[1], str2_arr[1], new_record1, vcf_writer)

                elif len(str1_arr[1]) ==1 and len(str2_arr[1]) == 1:
                    pass
                else:
                    str1_arr13 = str1_arr[1][1:]
                    str2_arr13 = str2_arr[1][1:]
                    cop1r, n1r = getNumofCommonSubstr(str1_arr13, str2_arr13)
                    if n1r != 0 and n1r != 1:
                        str1_arr3 = str1_arr13.split(cop1r)
                        str1_arr3[0] = str1_arr3[0] + cop1r[0]
                        str1_arr3[1] = cop1r[-1] + str1_arr3[1]
                        str2_arr3 = str2_arr13.split(cop1r)
                        str2_arr3[0] = str2_arr3[0] + cop1r[0]
                        str2_arr3[1] = cop1r[-1] + str2_arr3[1]
                        if (len(str1_arr3[0]) == 1 and len(str2_arr3[0]) != 1) or (len(str1_arr3[0]) != 1 and len(str2_arr3[0]) == 1):
                            new_record1 = copy.copy(record)
                            new_pos = record.POS
                            new_record1.POS = new_pos + len(str1_arr[0])-2 + n + 1
                            new_record1.REF = str1_arr3[0]
                            new_record1.ALT = [vcf.model._Substitution(str2_arr3[0])]
                            # vcf_writer.write_record(new_record1)
                            split_snp(str1_arr3[0], str2_arr3[0], new_record1, vcf_writer)
                            if (len(str1_arr3[1]) != 1 and len(str2_arr3[1]) == 1) or (len(str1_arr3[1]) ==1 and len(str2_arr3[1]) != 1):
                                new_record2 = copy.copy(record)
                                new_pos = record.POS
                                new_record2.POS = new_pos + len(str1_arr[0])-2 + n + len(str1_arr3[0])-1 + n1r
                                new_record2.REF = str1_arr3[1]
                                new_record2.ALT = [vcf.model._Substitution(str2_arr3[1])]
                                # vcf_writer.write_record(new_record2)
                                split_snp(str1_arr3[1], str2_arr3[1], new_record2, vcf_writer)

                            elif len(str1_arr3[1]) == 1 and len(str2_arr3[1]) == 1:
                                pass
                            else:
                                new_record2 = copy.copy(record)
                                new_pos = record.POS
                                new_record2.POS = new_pos + len(str1_arr[0])-2 + n + len(str1_arr3[0])-1 + n1r + 1
                                new_record2.REF = str1_arr3[1][1:]
                                new_record2.ALT = [vcf.model._Substitution(str2_arr3[1][1:])]
                                # vcf_writer.write_record(new_record2)
                                split_snp(str1_arr3[1][1:], str2_arr3[1][1:], new_record2, vcf_writer)

                        elif len(str1_arr3[0]) == 1 and len(str2_arr3[0]) == 1:
                            pass
                        else:
                            new_record1 = copy.copy(record)
                            new_pos = record.POS
                            new_record1.POS = new_pos + len(str1_arr[0]) - 1 + n
                            new_record1.REF = str1_arr3[0][:-1]
                            new_record1.ALT = [vcf.model._Substitution(str2_arr3[0][:-1])]
                            # vcf_writer.write_record(new_record1)
                            split_snp(str1_arr3[0][:-1], str2_arr3[0][:-1], new_record1, vcf_writer)
                            if (len(str1_arr3[1]) != 1 and len(str2_arr3[1]) == 1) or (len(str1_arr3[1]) == 1 and len(str2_arr3[1]) != 1):
                                new_record2 = copy.copy(record)
                                new_pos = record.POS
                                new_record2.POS = new_pos + len(str1_arr[0]) - 2 + n + len(str1_arr3[0]) - 1 + n1r
                                new_record2.REF = str1_arr3[1]
                                new_record2.ALT = [vcf.model._Substitution(str2_arr3[1])]
                                # vcf_writer.write_record(new_record2)
                                split_snp(str1_arr3[1], str2_arr3[1], new_record2, vcf_writer)
                            elif len(str1_arr3[1]) == 1 and len(str2_arr3[1]) == 1:
                                pass
                            else:
                                new_record2 = copy.copy(record)
                                new_pos = record.POS
                                new_record2.POS = new_pos + len(str1_arr[0]) - 2 + n + len(str1_arr3[0]) - 1 + n1r + 1
                                new_record2.REF = str1_arr3[1][1:]
                                new_record2.ALT = [vcf.model._Substitution(str2_arr3[1][1:])]
                                # vcf_writer.write_record(new_record2)
                                split_snp(str1_arr3[1][1:], str2_arr3[1][1:], new_record2, vcf_writer)
                    else:
                        new_record1 = copy.copy(record)
                        new_pos = record.POS + len(str1_arr[0])-2 + n+1
                        new_record1.REF = str1_arr13
                        new_record1.POS = new_pos
                        new_record1.ALT = [vcf.model._Substitution(str2_arr13)]
                        # vcf_writer.write_record(new_record1)
                        split_snp(str1_arr13, str2_arr13, new_record1, vcf_writer)
            else:
                str1_arr1 = str1_arr[0][:-1]
                str2_arr1 = str2_arr[0][:-1]
                new_record1 = copy.copy(record)
                new_record1.REF = str1_arr1
                new_record1.ALT = [vcf.model._Substitution(str2_arr1)]
                # vcf_writer.write_record(new_record1)
                split_snp(str1_arr1, str2_arr1, new_record1, vcf_writer)
                if (len(str1_arr[1]) !=1 and len(str2_arr[1]) == 1) or (len(str1_arr[1]) ==1 and len(str2_arr[1]) != 1):
                    new_record1 = copy.copy(record)
                    new_pos = record.POS
                    new_record1.POS = new_pos + len(str1_arr[0]) - 2 + n
                    new_record1.REF = str1_arr[1]
                    new_record1.ALT = [vcf.model._Substitution(str2_arr[1])]
                    # vcf_writer.write_record(new_record1)
                    split_snp(str1_arr[1], str2_arr[1], new_record1, vcf_writer)
                elif len(str1_arr[1]) ==1 and len(str2_arr[1]) == 1:
                    pass
                else:
                    str1_arr13 = str1_arr[1][1:]
                    str2_arr13 = str2_arr[1][1:]
                    cop1r, n1r = getNumofCommonSubstr(str1_arr13, str2_arr13)
                    if n1r != 0 and n1r != 1:
                        str1_arr3 = str1_arr13.split(cop1r)
                        str1_arr3[0] = str1_arr3[0] + cop1r[0]
                        str1_arr3[1] = cop1r[-1] + str1_arr3[1]
                        str2_arr3 = str2_arr13.split(cop1r)
                        str2_arr3[0] = str2_arr3[0] + cop1r[0]
                        str2_arr3[1] = cop1r[-1] + str2_arr3[1]
                        if (len(str1_arr3[0]) == 1 and len(str2_arr3[0]) != 1) or (len(str1_arr3[0]) != 1 and len(str2_arr3[0]) == 1):
                            new_record1 = copy.copy(record)
                            new_pos = record.POS
                            new_record1.POS = new_pos + len(str1_arr[0]) - 2 + n + 1
                            new_record1.REF = str1_arr3[0]
                            new_record1.ALT = [vcf.model._Substitution(str2_arr3[0])]
                            # vcf_writer.write_record(new_record1)
                            split_snp(str1_arr3[0], str2_arr3[0], new_record1, vcf_writer)
                            if (len(str1_arr3[1]) != 1 and len(str2_arr3[1]) == 1) or (len(str1_arr3[1]) == 1 and len(str2_arr3[1]) != 1):
                                new_record2 = copy.copy(record)
                                new_pos = record.POS
                                new_record2.POS = new_pos + len(str1_arr[0]) - 2 + n + len(str1_arr3[0]) - 1 + n1r
                                new_record2.REF = str1_arr3[1]
                                new_record2.ALT = [vcf.model._Substitution(str2_arr3[1])]
                                # vcf_writer.write_record(new_record2)
                                split_snp(str1_arr3[1], str2_arr3[1], new_record2, vcf_writer)

                            elif len(str1_arr3[1]) == 1 and len(str2_arr3[1]) == 1:
                                pass
                            else:
                                new_record2 = copy.copy(record)
                                new_pos = record.POS
                                new_record2.POS = new_pos + len(str1_arr[0]) - 2 + n + len(str1_arr3[0]) - 1 + n1r + 1
                                new_record2.REF = str1_arr3[1][1:]
                                new_record2.ALT = [vcf.model._Substitution(str2_arr3[1][1:])]
                                # vcf_writer.write_record(new_record2)
                                split_snp(str1_arr3[1][1:], str2_arr3[1][1:], new_record2, vcf_writer)

                        elif len(str1_arr3[0]) == 1 and len(str2_arr3[0]) == 1:
                            pass
                        else:
                            new_record1 = copy.copy(record)
                            new_pos = record.POS
                            new_record1.POS = new_pos + len(str1_arr[0]) - 2 + n + 1
                            new_record1.REF = str1_arr3[0][:-1]
                            new_record1.ALT = [vcf.model._Substitution(str2_arr3[0][:-1])]
                            # vcf_writer.write_record(new_record1)
                            split_snp(str1_arr3[0][:-1], str2_arr3[0][:-1], new_record1, vcf_writer)
                            if (len(str1_arr3[1]) != 1 and len(str2_arr3[1]) == 1) or (len(str1_arr3[1]) == 1 and len(str2_arr3[1]) != 1):
                                new_record2 = copy.copy(record)
                                new_pos = record.POS
                                new_record2.POS = new_pos + len(str1_arr[0]) - 2 + n + len(str1_arr3[0]) - 1 + n1r
                                new_record2.REF = str1_arr3[1]
                                new_record2.ALT = [vcf.model._Substitution(str2_arr3[1])]
                                # vcf_writer.write_record(new_record2)
                                split_snp(str1_arr3[1], str2_arr3[1], new_record2, vcf_writer)
                            elif len(str1_arr3[1]) == 1 and len(str2_arr3[1]) == 1:
                                pass
                            else:
                                new_record2 = copy.copy(record)
                                new_pos = record.POS
                                new_record2.POS = new_pos + len(str1_arr[0]) - 2 + n + len(str1_arr3[0]) - 1 + n1r + 1
                                new_record2.REF = str1_arr3[1][1:]
                                new_record2.ALT = [vcf.model._Substitution(str2_arr3[1][1:])]
                                # vcf_writer.write_record(new_record2)
                                split_snp(str1_arr3[1][1:], str2_arr3[1][1:], new_record2, vcf_writer)
                    else:
                        new_record1 = copy.copy(record)
                        new_pos = record.POS + len(str1_arr[0]) - 2 + n + 1
                        new_record1.REF = str1_arr13
                        new_record1.POS = new_pos
                        new_record1.ALT = [vcf.model._Substitution(str2_arr13)]
                        # vcf_writer.write_record(new_record1)
                        split_snp(str1_arr13, str2_arr13, new_record1, vcf_writer)
    else:
        split_snp(str1, str2, record, vcf_writer)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--vcf', help='input vcf file of which need to be duplicated or assessed', required=True)
    parser.add_argument('-out', '--out', help='output vcf file of which has being duplicated or assessed',
                        required=True)
    parser.add_argument('-k', '--knowns', help='input the truth sites vcf files', required=True)
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
    #
    args = parser.parse_args()
    vcf_file = os.path.abspath(args.vcf)
    knowns_file = os.path.abspath(args.knowns)
    out_file = os.path.abspath(args.out)
    # # log_file=os.path.abspath(args.logging_file)
    #
    # logger.info('\n[ the number of process is  %s]',pro_num)
    logger.info('\n[ start time: %s]', time.asctime(time.localtime(time.time())))
    vcf_file = 'C:/SoftWares/PuTTY/199007051D_199007052D_fisher.vcf'
    out_file = 'C:/SoftWares/PuTTY/199007051D_199007052D_fisher_new.vcf'
    logger = 'C:/SoftWares/PuTTY/NA12878_all.log'
    args_ = [vcf_file, out_file, logger]
    DupliateAndAssess = DupliateAndAssess(args_)
    DupliateAndAssess.processing()
    logger.info('\n[ end time: %s]', time.asctime(time.localtime(time.time())))

    vcffile = 'C:/Users/Sherwin/Desktop/wgs/03.cmpHC/call_v9_split.vcf.gz'
    new_vcffile = 'C:/Users/Sherwin/Desktop/wgs/03.cmpHC/call_v9_split_new.vcf.gz'
    vcf_reader = vcf.Reader(open(vcffile, 'rb'))
    vcf_writer = vcf.Writer(open(new_vcffile, 'wb'), vcf_reader)

    for rec in vcf_reader:
        compared(rec,vcf_writer)
    vcf_writer.close()
