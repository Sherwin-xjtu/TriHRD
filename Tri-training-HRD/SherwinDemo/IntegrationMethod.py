# coding=utf-8
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn import neighbors
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_moons
from sklearn.metrics import accuracy_score
import pandas as pd
from sklearn.metrics import classification_report
from sklearn.naive_bayes import GaussianNB
from sklearn import mixture
from sklearn.tree import DecisionTreeClassifier
import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm, datasets
from sklearn.metrics import roc_curve, auc  ###计算roc和auc
from sklearn import cross_validation
from sklearn.model_selection import cross_val_score

from xgboost.sklearn import XGBClassifier
# 导入数据
# X, y = make_moons(n_samples=500, noise=0.30, random_state=42)
# X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)


def bagging_report(M, T):
    y_true = T['type']
    target = ['class 0', 'class 1']
    x = T.drop(['type'], 1)
    x_train = x.values
    y_pred = M.predict(x_train)
    report = classification_report(y_true, y_pred, target_names=target)
    print("三个分类器集成后的性能报告：\n {0}".format(report))


def roc(clf,li):
    # svm = svm.SVC(kernel='linear', probability=True, random_state=random_state)
    X_train = li[0]
    y_train = li[1]
    X_test = li[2]
    y_test = li[3]
    ###通过decision_function()计算得到的y_score的值，用在roc_curve()函数中
    # y_score = clf.fit(X_train, y_train).decision_function(X_test)
    y_score = clf.fit(X_train, y_train).predict_proba(X_test)
    # Compute ROC curve and ROC area for each class
    fpr, tpr, threshold = roc_curve(y_test, y_score[:,1])  ###计算真正率和假正率
    roc_auc = auc(fpr, tpr)  ###计算auc的值
    plt.figure()
    lw = 2
    plt.figure(figsize=(10, 10))
    plt.plot(fpr, tpr, color='darkorange',
             lw=lw, label='ROC curve (area = %0.2f)' % roc_auc)  ###假正率为横坐标，真正率为纵坐标做曲线
    plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic example')
    plt.legend(loc="lower right")
    plt.show()


from sklearn.ensemble import BaggingClassifier
from sklearn.tree import DecisionTreeClassifier
if __name__ == '__main__':
    train = pd.read_csv('../AllData/labeled/trianing_50_data.csv')
    x_train_columns = [x for x in train.columns if x not in ['type']]
    X_train = train[x_train_columns]
    y_train = train['type']

    test = pd.read_csv('../AllData/labeled/test_data.csv')
    x_test_columns = [x for x in test.columns if x not in ['type']]
    X_test = test[x_test_columns]
    y_test = test['type']

    data_list = []
    data_list.append(X_train)
    data_list.append(y_train)
    data_list.append(X_test)
    data_list.append(y_test)

    # 三个基学习器
    dt_clf = DecisionTreeClassifier()
    rf_clf = RandomForestClassifier()
    svm_clf = SVC(probability=True)
    log_clf = LogisticRegression()
    nbrs_clf = neighbors.KNeighborsClassifier()
    nb_clf = GaussianNB()
    GMM_clf = mixture.GMM(n_components=2)
    xgb_clf = XGBClassifier()

    # 投票分类器

    voting_clf = VotingClassifier(estimators=[("xgb_clf",xgb_clf ), ("svc", svm_clf), ("dt",dt_clf )], voting="soft")
    roc(voting_clf,data_list)
    voting_clf.fit( X_train, y_train )
    # bagging_report(voting_clf,test)

    from sklearn.metrics import confusion_matrix

    y_pred = voting_clf.predict(X_test)
    labels = list(set(y_test))
    conf_mat = confusion_matrix(y_test, y_pred, labels=labels)
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

    for clf in ( dt_clf, rf_clf,log_clf,nbrs_clf,svm_clf,nb_clf ,GMM_clf,xgb_clf,voting_clf):
        clf.fit( X_train, y_train )
        y_pred = clf.predict( X_test )
        print( clf.__class__.__name__, accuracy_score(y_test, y_pred) )

    for clf, label in zip([xgb_clf, svm_clf, dt_clf, voting_clf], ['XGBBoosting', 'Random Forest', 'SVM', 'Ensemble']):
        scores = cross_val_score(clf, X_train, y_train, cv=5, scoring='accuracy')
        print("Accuracy: %0.2f (+/- %0.2f) [%s]" % (scores.mean(), scores.std(), label))

    # bag_clf = BaggingClassifier(base_estimator=svm_clf, n_estimators=25, max_samples=49, bootstrap=True, n_jobs=8 )
    # bag_clf.fit( X_train, y_train )
    # y_pred = bag_clf.predict( X_test )
    # pred_score = accuracy_score( y_pred, y_test )
    # print( pred_score )