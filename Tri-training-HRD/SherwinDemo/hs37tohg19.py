#!/usr/bin/python
# coding=utf-8
import vcf

# data_vcf_reader = vcf.Reader(filename=r'C:/Users/Sherwin/Desktop/STANDARD_NA12878.vcf')
# # writer = vcf.Writer('wb','C:/Users/Sherwin/Desktop/STANDARD_NA12878.vcf', lineterminator='n')
# for record in data_vcf_reader:
#     chrom = record.CHROM
#     record.CHROM = 'chr'+chrom
#
#     print  record.CHROM

from pysam import VariantFile
bcf_in  = VariantFile("/mnt/X500/farmers/wangxw/tri_training_results/data/STANDARD_NA12878.vcf", "r")
bcf_out = VariantFile("/mnt/X500/farmers/wangxw/tri_training_results/data/STANDARD_NA12878_out.vcf", "w", header=bcf_in.header)
for rec in bcf_in.fecth():
    dir(rec)
    bcf_out.write(rec)
