import pysam
import vcf
import pandas as pd

def get_tgp_frequence(chromo, position, frequence_type):
    gvcf = "/mnt/X500/farmers/wangshj/digitalsimulator/tgp_phase3_small_vars.vcf.gz"
    vcf_in = pysam.VariantFile(gvcf)
    chromo = chromo[3:]
    frequence_type = frequence_type + '='
    try:
        for rec in vcf_in.fetch(chromo, position - 1, position):
            this_base = str(rec)
            break
        this_base_array = this_base.split()
        ref_length = len(this_base_array[3])
        alt = this_base_array[4]
        this_base_info_array = this_base_array[7].split(';')
        for this_base_info_element in this_base_info_array:
            if this_base_info_element.startswith(frequence_type):
                frequence = this_base_info_element.split('=')[-1]
                return ref_length, alt, frequence
    except:
        return ""

raw_vcf = "/mnt/X500/farmers/wangxw/newResults/gatk_bundle/1000G_phase1.indels.b37.vcf.gz"
gvcf1 = "/mnt/X500/farmers/wangxw/newResults/gatk_bundle/1000G_phase1.indels.b37.vcf.gz"
gvcf2 = "/mnt/X500/farmers/wangxw/newResults/gatk_bundle/1000G_phase1.indels.b37.vcf.gz"
gvcf3 = "/mnt/X500/farmers/wangxw/newResults/gatk_bundle/1000G_phase1.indels.b37.vcf.gz"

vcf_in = pysam.VariantFile(gvcf1)
vcf_in1 = pysam.VariantFile(gvcf1)
vcf_in2 = pysam.VariantFile(gvcf2)
vcf_in3 = pysam.VariantFile(gvcf3)
Y_list = []
X_tp_POS_list = []
X_tp_MQ_list = []
X_tp_QD_list = []
X_fp_POS_list = []
X_fp_MQ_list = []
X_tp_QD_list = []

for record in vcf_in.fetch():
    POS = record.POS

    chromo = record.CHROM
    info_dict = record.INFO
    QD = record.QUAL
    ulable = True
    x_list = []
    for rec in vcf_in1.fetch(chromo, POS - 1, POS):

        ulable = False
        X_tp_POS_list.append(POS)
        X_tp_MQ_list.append(info_dict['MQ'])
        X_tp_QD_list.append(QD)
        Y_list.append(1)
    if ulable:
        for rec in vcf_in2.fetch(chromo, POS - 1, POS):
            ulable = False
            X_tp_POS_list.append(POS)
            X_tp_MQ_list.append(info_dict['MQ'])
            X_tp_QD_list.append(QD)
            Y_list.append(1)

    if ulable:
        for rec in vcf_in3.fetch(chromo, POS - 1, POS):
            ulable = False
            X_tp_POS_list.append(POS)
            X_tp_MQ_list.append(info_dict['MQ'])
            X_tp_QD_list.append(QD)
            Y_list.append(1)

    if ulable:
        X_fp_POS_list.append(POS)
        X_fp_MQ_list.append(info_dict['MQ'])
        X_tp_QD_list.append(QD)


Y_list_str = map(str, Y_list)
X_tp_POS_list_str = map(str,X_tp_POS_list)
X_tp_MQ_list_str = map(str,X_tp_MQ_list)
X_tp_QD_list_str = map(str,X_tp_QD_list)
X_fp_POS_list_str = map(str,X_fp_POS_list)
X_fp_MQ_list_str = map(str,X_fp_MQ_list)
X_tp_QD_list_str = map(str,X_tp_QD_list)

#字典中的key值即为csv中列名
dataframe_U = pd.DataFrame({'POS':X_fp_POS_list_str,'MQ':X_fp_MQ_list_str,'QD':X_tp_QD_list_str})

#将DataFrame存储为csv,index表示是否显示行名，default=True
dataframe_U.to_csv("/mnt/X500/farmers/wangxw/tri_training_results/resoult_csv/Test_U__071803.csv",index=False,sep=',')

#字典中的key值即为csv中列名
dataframe_L = pd.DataFrame({'POS':X_tp_POS_list_str,'MQ':X_tp_MQ_list_str,'QD':X_tp_QD_list_str,'type':Y_list_str},columns=['POS','MQ','QD','type'])

#将DataFrame存储为csv,index表示是否显示行名，default=True
dataframe_L.to_csv("/mnt/X500/farmers/wangxw/tri_training_results/resoult_csv/Test_L__071803.csv",index=False,sep=',')

