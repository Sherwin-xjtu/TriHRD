#!/usr/bin/python
# coding=utf-8
import pandas as pd
import numpy as np
import xgboost as xgb
import operator
import matplotlib.pyplot as plt
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import sys
reload(sys)
sys.setdefaultencoding('gb18030')

def ceate_feature_map(features):  
    outfile = open('xgb_t01.fmap', 'w')
    i = 0  
    for feat in features:  
        outfile.write('{0}\t{1}\tq\n'.format(i, feat))  
        i = i + 1  
    outfile.close()  
  
  
if __name__ == '__main__':  
    # train = pd.read_csv("./data/Test_L_071803_t01.csv")
    #     # # train['CHROM'] = train['CHROM'].astype(int)
    #     # train['CHROM']=train['CHROM'].replace(['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','X','Y'],
    #     #                        [1,2,3,4,5,6,7,8,9,19,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25])
    #     # train.to_csv('./data/Test_L_071803_t02.csv',index = False)
    train = pd.read_csv("./data/Test_L__072302_t_scale.csv")
    params = {  
        'min_child_weight': 5,
        'eta': 0.3,
        'n_estimators': 600,
        'colsample_bytree': 0.75,
        'max_depth': 3,
        'subsample': 0.8,
        'alpha': 1,
        'gamma': 0,
        # 'reg_alpha': 0.05,
        'reg_lambda': 1,
        'silent': 1,  
        'verbose_eval': True,  
        'seed': 0,
        'scale_pos_weight':1,
        # 'learning_rate':0.1

    }
    rounds = 1000
    y = train['type']
    # print type(y)
    X = train.drop(['type'], 1)
    # print X
  
    xgtrain = xgb.DMatrix(X, label=y)  
    bst = xgb.train(params, xgtrain, num_boost_round=rounds)
  
    features = [x for x in train.columns if x not in ['type']]
    ceate_feature_map(features)  
  
    importance = bst.get_fscore(fmap='xgb_t01.fmap')
    print importance
    importance = sorted(importance.items(), key=operator.itemgetter(1))  
    
    df = pd.DataFrame(importance, columns=['feature', 'fscore'])  

    df['fscore'] = df['fscore'] / df['fscore'].sum()
    df.to_csv("./data/feat_importance_t01.csv", index=False)
  
    plt.figure()  
    df.plot(kind='barh', x='feature', y='fscore', legend=False, figsize=(6, 10))  
    plt.title('XGBoost Feature Importance')  
    plt.xlabel('relative importance')  
    plt.show()  




