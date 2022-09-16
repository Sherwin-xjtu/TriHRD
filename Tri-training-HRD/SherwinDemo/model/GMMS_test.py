#!/usr/bin/python
# coding=utf-8
import numpy as np
import pandas as pd
from sklearn.metrics import classification_report
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import MinMaxScaler



def my_confusion_matrix(y_true, y_pred):
    from sklearn.metrics import confusion_matrix
    labels = list(set(y_true))
    conf_mat = confusion_matrix(y_true, y_pred, labels=labels)
    print "confusion_matrix(left labels: y_true, up labels: y_pred):"
    print "labels\t",
    for i in range(len(labels)):
        print labels[i], "\t",
    print
    for i in range(len(conf_mat)):
        print i, "\t",
        for j in range(len(conf_mat[i])):
            print conf_mat[i][j], '\t',
        print
    print



if __name__ == "__main__":
    # os.chdir(os.path.abspath('..'))
    # os.chdir(os.path.abspath('..'))
    # path = os.getcwd()
    # print path+
    reader = pd.read_csv('C:/Users/Sherwin/Desktop/newdata/merge2_test.csv')
    tv_label = reader.drop(['CHROM', 'POS', 'ID', 'REF', 'ALT', 'AD', 'CONTQ',  'MFRL', 'MPOS', 'POPAF', 'UBP', 'DBP', 'UDBP','MBQ', 'MMQ', 'ClippingRankSum', 'type'], 1)
    # print reader['CONTQ']+reader['POS']
    X = tv_label
    gmm = GaussianMixture(n_components=2,max_iter=1000)
    gmm.fit(X)
    labels = gmm.predict(X)
    yy_L = reader['type']
    y_P = labels
    # target = ['false snp','true snp','false indel','true indel']
    target = ['false snp', 'true snp']
    my_confusion_matrix(yy_L, y_P)  # 输出混淆矩阵
    report4 = classification_report(yy_L, y_P, target_names=target)
    print("三个分类器集成后的性能报告(测试集)：\n {0}".format(report4))


