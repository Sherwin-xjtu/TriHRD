import pandas as pd

# label_data = pd.read_csv('../dealData/data/label_data_normal.csv')
# # label = label_data.loc[:,['pt']]
# # print label
# # features = label_data.iloc[:,1:-1]
# # print features


import pandas as pd
import numpy as np
import vcf
from numpy import *

ll = ('aa','cc')
if 'a' in ll:
    print 'Sherwin'

ld = {'sherwin':22,
      'age':33}

print ld['sherwin']
print NaN+1+2

# train = pd.read_csv("../dealData/data/180727_L01.csv")
# print train
# label_data = train.sample(n=10)
# print train.drop(label_data.index.values)

lsi = [1,2,3]
for i in range(3):
    M_jk = [lsi[x] for x in range(3) if x != i]
    print M_jk


def genModel(i, L):
    switch = {
        0: L,
        1: L+1,
        2: L+2
    }
    return switch.get(i)
print genModel(3,8)


y_1 = [1,1,1,0]
y_2 = [0,0,1,0]
y_3 = [1,0,0,1]
y = np.array([y_1,y_2,y_3])
y_pre = list(map(sum,zip(*y)))
def f(x):
    if x>1:
        return 1
    else:
        return 0
y_pre = list(map(f,y_pre))
print y_pre

stt = 'sh,er,win'
if stt.find('shew') !=-1:
    print "Dior"
snvEmptyFeatureString = ',' * stt.count(',')
print snvEmptyFeatureString

print float(2)/float(10)


# train.fillna(train.mean()).to_csv('../dealData/data/Test_L__072302_t_11.csv',index = False)