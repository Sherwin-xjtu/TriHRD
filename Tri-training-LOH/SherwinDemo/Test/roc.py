#!/usr/bin/python
# coding=utf-8
import warnings
warnings.filterwarnings("ignore")
import warnings
warnings.filterwarnings(module='sklearn*', action='ignore', category=DeprecationWarning)

from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split

def roc(clf, reader02 ):

    X_test02 = reader02.drop(['type'], 1)
    y_test02 = reader02['type']
    X_test02 = X_test02.values
    y_score02 = clf.predict_proba(X_test02)
    # Compute ROC curve and ROC area for each class
    fpr, tpr, threshold = roc_curve(y_test02, y_score02[:, 1])  ###计算真正率和假正率
    return fpr, tpr, threshold


""" 获取X,Y """


def X_Y(S):
    train = S
    y = train['type']
    x = train.drop(['type'], 1)
    return x, y


""" 准备数据 """

def pre_data(reader):
    X_train, y_train = X_Y(reader)
    X_train, X_tv, y_train, y_tv = train_test_split(X_train, y_train, test_size=0.98, random_state=3)
    return X_train,y_train


if __name__ == "__main__":
    data03 = pd.read_csv('G:/Tri-training-HRD/Alldata/labeled/ILM_INDEL_Test_stander.csv')
    data02 = pd.read_csv('G:/Tri-training-HRD/Alldata/labeled/NA12878-GATK3-chr21_2000.csv')
    data01 = pd.read_csv('G:/Tri-training-HRD/Alldata/labeled/ILM_SNP_Test_stander.csv')

    reader02 = data02.drop(['CHROM', 'POS', 'PL'], 1)
    reader03 = data03
    reader01 = data01

    X_train02, y_train02 = pre_data(reader02)
    clf02 = GaussianNB()
    clf02.fit(X_train02, y_train02)
    fpr02, tpr02, threshold02 = roc(clf02, reader02)
    roc_auc02 = auc(fpr02, tpr02)  ###计算auc的值

    X_train03, y_train03 = pre_data(reader03)
    clf03 = GaussianNB()
    clf03.fit(X_train03, y_train03)
    fpr03, tpr03, threshold03 = roc(clf03, reader03)
    roc_auc03 = auc(fpr03, tpr03)  ###计算auc的值

    X_train01, y_train01 = pre_data(reader01)
    clf01 = GaussianNB()
    clf01.fit(X_train01, y_train01)
    fpr01, tpr01, threshold01 = roc(clf01, reader01)
    roc_auc01 = auc(fpr01, tpr01)  ###计算auc的值

    lw = 2

    # 设置输出的图片大小
    figsize = 10, 10
    figure, ax = plt.subplots(figsize=figsize)
    # plt.figure(figsize=(10, 10))
    # 设置坐标刻度值的大小以及刻度值的字体
    plt.tick_params(labelsize=23)
    labels = ax.get_xticklabels() + ax.get_yticklabels()
    [label.set_fontname('Times New Roman') for label in labels]

    # 设置图例并且设置图例的字体及大小
    font1 = {'family': 'Times New Roman',
             'weight': 'normal',
             'size': 23,
             }

    # 设置横纵坐标的名称以及对应字体格式
    font2 = {'family': 'Times New Roman',
             'weight': 'normal',
             'size': 30,
             }


    plt.plot(fpr02, tpr02, color='darkorange',
             lw=lw, label='ROC curve 02 (area = %0.2f)' % roc_auc02)  ###假正率为横坐标，真正率为纵坐标做曲线
    plt.plot(fpr03, tpr03, color='lime',
             lw=lw, label='ROC curve 03 (area = %0.2f)' % roc_auc03)
    plt.plot(fpr01, tpr01, color='blue',
             lw=lw, label='ROC curve 01 (area = %0.2f)' % roc_auc01)



    plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate', font2)
    plt.ylabel('True Positive Rate', font2)
    plt.title('Receiver operating characteristic example',font2)
    plt.legend(loc=4)

    plt.savefig('G:/ROC/roc.jpg')
    plt.show()