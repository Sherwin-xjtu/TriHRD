#!/usr/bin/python
# coding=utf-8

import vcf
import multiprocessing
import json
import pandas as pd


data_vcf_reader = vcf.Reader(filename=r'/mnt/X500/farmers/wangxw/tri_training_results/data_vcf/170016612BCD.indel.final.vcf')

dbsnp_138_b37_del100_pos_list = list()
_1000G_phase1_indels_b37_list = list()
Mills_and_1000G_gold_standard_indels_b37_list = list()
data_list = list()
data_L_list = list()
data_U_list = list()

X_L_pos_list = list()
X_L_MQ_list = list()
X_L_QD_list = list()

X_U_pos_list = list()
X_U_MQ_list = list()
X_U_QD_list = list()

Y_list = list()


def load_resources():
    # dbsnp_138_b37_del100_vcf_reader = vcf.Reader(filename=r'/mnt/X500/farmers/wangxw/newResults/gatk_bundle/dbsnp_138.b37.del100.vcf')
    # _1000G_phase1_indels_b37_vcf_reader = vcf.Reader(filename=r'/mnt/X500/farmers/wangxw/newResults/gatk_bundle/1000G_phase1.indels.b37.vcf')
    # Mills_and_1000G_gold_standard_indels_b37_vcf_reader = vcf.Reader(filename=r'/mnt/X500/farmers/wangxw/newResults/gatk_bundle/Mills_and_1000G_gold_standard.indels.b37.vcf')

    # testData_vcf_reader = vcf.Reader(filename=r'C:\Users\Sherwin\Desktop\outtsv\1.vcf')

   # for record in dbsnp_138_b37_del100_vcf_reader:
     #   dbsnp_138_b37_del100_pos_list.append(record.POS)

    #for record in _1000G_phase1_indels_b37_vcf_reader:
      #  _1000G_phase1_indels_b37_list.append(record.POS)

   # for record in Mills_and_1000G_gold_standard_indels_b37_vcf_reader:
    #    Mills_and_1000G_gold_standard_indels_b37_list.append(record.POS)



    re_dict = dict()

    re_dict['dbsnp'] = dbsnp_138_b37_del100_pos_list
    re_dict['1000G'] = _1000G_phase1_indels_b37_list
    re_dict['Mills'] = Mills_and_1000G_gold_standard_indels_b37_list
    # print re_dict['dbsnp']
    # 将数据写进json文件中
    # json_str = json.dumps(re_dict)
   # with open("/mnt/X500/farmers/wangxw/tri_training_results/resources_record_01.json", "w") as f:
    #    json.dump(re_dict, f)

    # 从json文件中加载数据
    with open("/mnt/X500/farmers/wangxw/tri_training_results/resources_record_01.json", 'r') as load_f:
        load_re_dict = json.load(load_f)
    return load_re_dict
    # load_dict['smallberg'] = [8200,{1:[['Python',81],['shirt',300]]}]    添加元素



# if not load_re_dict:
load_re_dict = load_resources()

def process_func(record):
    pos = record.POS
    info_dict = record.INFO
    QD = record.QUAL
    data_list = []
    x_L_list = []
    y_list = []
    x_U_list = []
    if pos in load_re_dict['dbsnp'] or load_re_dict['1000G'] or load_re_dict['Mills']:
        x_L_list.append(pos)
        x_L_list.append(info_dict['MQ'])
        x_L_list.append(QD)    
        y = 1
    else:
        # print "Sheriwn"
        x_U_list.append(pos)
        x_U_list.append(info_dict['MQ'])
        x_U_list.append(QD)

    return x_L_list,y,x_U_list



pool = multiprocessing.Pool(processes=50)
multiprocessing.process
result = list()
count = 0
for line in data_vcf_reader:
    count += 1
    print count
    result.append(pool.apply_async(process_func, [line]))
pool.close()
pool.join()

for res in result:
    (x_L_list, y, x_U_list) = res.get()
    Y_list.append(y)
    if x_L_list != []:
        X_L_pos_list.append(x_L_list[0])
        X_L_MQ_list.append(x_L_list[1])
        X_L_QD_list.append(x_L_list[2])
    if x_U_list != []:
        X_U_pos_list.append(x_U_list[0])
        X_U_MQ_list.append(x_U_list[1])
        X_U_QD_list.append(x_U_list[2])



Y_list_str = map(str, Y_list)
X_L_pos_list_str = map(str,X_L_pos_list)
X_L_MQ_list_str = map(str,X_L_MQ_list)
X_L_QD_list_str = map(str,X_L_QD_list)
X_U_pos_list_str = map(str,X_U_pos_list)
X_U_MQ_list_str = map(str,X_U_MQ_list)
X_U_QD_list_str = map(str,X_U_QD_list)


#字典中的key值即为csv中列名
dataframe_U = pd.DataFrame({'POS':X_U_pos_list_str,'MQ':X_U_MQ_list_str,'QD':X_U_QD_list_str})

#将DataFrame存储为csv,index表示是否显示行名，default=True
dataframe_U.to_csv("/mnt/X500/farmers/wangxw/tri_training_results/resoult_csv/Test_U__071802.csv",index=False,sep=',')



#字典中的key值即为csv中列名
dataframe_L = pd.DataFrame({'POS':X_L_pos_list_str,'MQ':X_L_MQ_list_str,'QD':X_L_QD_list_str,'type':Y_list_str},columns=['POS','MQ','QD','type'])

#将DataFrame存储为csv,index表示是否显示行名，default=True
dataframe_L.to_csv("/mnt/X500/farmers/wangxw/tri_training_results/resoult_csv/Test_L__071802.csv",index=False,sep=',')
