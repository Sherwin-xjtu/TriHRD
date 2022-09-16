#!/usr/bin/python
# coding=utf-8
import getopt
import multiprocessing
import os
import sys

import vcf
import numpy as np


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


def print_pack_f(file_path):
    # '''
    # name:print_pack_f
    # function:打印一个pcap文件中所有数据包的五元组信息
    # file_path：所给pcap文件路径
    # '''
    # file_p = open(file_path)
    # pcap = dpkt.pcap.Reader(file_p)
    # if not pcap:
    #     return
    # print "\n\n*******file:%s*******\n" % file_path
    # for (ts, buf) in pcap:
    #     try:
    #     eth = dpkt.ethernet.Ethernet(buf)  # 解包，物理层
    # if not isinstance(eth.data, dpkt.ip.IP):  # 解包，网络层
    #     continue
    # ip = eth.data
    # src_ip = "%d.%d.%d.%d" % tuple(map(ord, list(ip.src)))
    # dst_ip = "%d.%d.%d.%d" % tuple(map(ord, list(ip.dst)))
    # if (not isinstance(ip.data, dpkt.tcp.TCP)) and (not isinstance(ip.data, dpkt.udp.UDP)):  # 解包，传输层
    #     continue
    # transf = ip.data
    # print "<", src_ip, ":", transf.sport, "-->", dst_ip, ":", transf.dport, ">"
    # except Exception, err:
    # print "[error] %s" % err
    print file_path

def compvcf(mlt, nlt, k, return_dict):
    a = 0
    c = 0
    d = 0
    sensitivity = 0
    for record2 in mlt:
        for record1 in nlt:
            if record1.CHROM == record2.CHROM and record1.POS == record2.POS:
                c = c + 1
                if 'FET' in record1.INFO:
                    if record1.INFO['FET'][0] > 5 and record1.INFO['VAFN'][0] < 0.02:
                        a = a + 1
                        if record1.INFO['VAFC'][0] < 0.01:
                            d = d + 1
    li = [c, a, d]

    return_dict[k] = li
def spfu(listTemp, n):
    for i in range(0, len(listTemp), n):
        yield listTemp[i:i + n]
def Assess(pvcf, mlt, threads):
    new_vcfreader = vcf.Reader(open(pvcf, 'r'))
    nlt = []
    relt = []
    nelt = []
    p = threads
    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    # pl = multiprocessing.Pool(p)

    print 'start'
    for record in new_vcfreader:
        nlt.append(record)
    # for record in new_vcfreader:
    #	    print record
    #   pl.apply_async(tupaend, args=(record,nlt))
    # pl.close()
    # pl.join()

    # v = -1
    # print 'start'
    # for record in new_vcfreader:
    # v = v + 1
    # process = multiprocessing.Process(target=self.tupappend, args=(record,v))
    # process.start()
    # nelt.append(process)

    # print "Sub-process(es) done."


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
    # logger.info('FET>5 and VAFN < 0.02: %s ,platypus: %s ,VAFC < 0.01: %s ,mutect2: %s, sensitivity: %s',
    #             sum_ls[1], sum_ls[0], sum_ls[2], n, sensitivity)

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
def main(vcffile,m_vcf):
    dir_path = split_file(vcffile)
    all_file_path = getPathFile(dir_path)  # 获取目录下所有pcap文件路径
    m_vcfreader = vcf.Reader(open(m_vcf, 'r'))
    n = 0
    mlt = ()
    sum_ls = []
    lk = []
    for record2 in m_vcfreader:
        mlt = mlt + (record2,)
        n = n + 1
    reutrn_result = []
    for file in all_file_path:  # 遍历处理

        result = Assess(file, mlt, 1)  # 单个vcf文件处理，可将本函数替换成自定义的功能，便可实现批量处理
        reutrn_result.append(result)

    for return_dict in reutrn_result:
        for i in return_dict.keys():
            lk.append(return_dict[i])
        sum_ls = np.sum(lk, axis=0)
    sensitivity = sum_ls[0] / n
    print ('FET>5 and VAFN < 0.02: %s ,platypus: %s ,VAFC < 0.01: %s ,mutect2: %s, sensitivity: %s', sum_ls[1], sum_ls[0],sum_ls[2], n, sensitivity)

if __name__ == '__main__':
    #    opts, args = getopt.getopt(sys.argv[1:], "hi:")  # 从命令行获取参数
    #    if not opts:  # 若没有带参数
    #        print "\n\
    # *******************\n\
    # warn! please enter related parameters,enter -h for help!\n\n\
    # *******************\n"
    #    sys.exit()
    input_path = 'C:/Dwork/Tri-training-HRD/Tri-training-HRD/SherwinDemo/NewDemo/'
    n_vcf = 'C:/Users/Sherwin/Desktop/platypus/190018206_TN.vcf'
    m_vcf = 'C:/Users/Sherwin/Desktop/platypus/190018206.m2.vcf'
    # for op, value in opts:
    #     if op == "-i":
    #         input_path = value
    #     elif op == "-h":
    #         usage()  # 帮助信息，只是简单的一个输出函数，输出内容自定义
    # sys.exit()
    main(n_vcf,m_vcf)
