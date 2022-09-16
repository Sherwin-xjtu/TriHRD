#!/usr/bin/python
# coding=utf-8
import os
import pandas as pd
# import shutil
path = 'C:/Users/Sherwin/Desktop/luo/test/'   #设置csv所在文件夹

files = os.listdir(path)  #获取文件夹下所有文件名

df1 = pd.read_csv(path + files[0],encoding='gbk')  #读取首个csv文件，保存到df1中
b = os.path.dirname(path + files[0])
dir_path = b + '/temp1/'
os.mkdir(dir_path)

for file in files[1:]:
  df2 = pd.read_csv(path + file,encoding='gbk')  #打开csv文件，注意编码问题，保存到df2中
  df1 = pd.concat([df1,df2],axis=0,ignore_index=True)  #将df2数据与df1合并

# df1 = df1.drop_duplicates()   #去重
# df1 = df1.reset_index(drop=True) #重新生成index
data = df1
data.to_csv(dir_path + 'total.csv',index=False) #将结果保存为新的csv文件

# shutil.rmtree(dir_path)