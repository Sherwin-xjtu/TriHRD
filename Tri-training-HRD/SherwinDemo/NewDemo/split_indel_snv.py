#!/usr/bin/python
# coding=utf-8
import  pandas as pd


variants = pd.read_csv('C:/Users/Sherwin/Desktop/NewResults/Result7/ILM_INDEL_Test_stander/ILM_INDEL_Test_stander.csv')

indel = variants[variants['Target']=='indel']

indel.to_csv('C:/Users/Sherwin/Desktop/NewResults/Result7/ILM_INDEL_Test_stander/ILM_INDEL_Test_stander.csv', index=False)
snv = variants.drop(indel.index.values)
snv.to_csv('C:/Users/Sherwin/Desktop/NewResults/Result7/ILM_INDEL_Test_stander/ILM_INDEL_Test_stander.csv', index=False)