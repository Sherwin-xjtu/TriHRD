#!/usr/bin/python
# coding=utf-8
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import mglearn
from sklearn.naive_bayes import GaussianNB
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_recall_curve,average_precision_score

reader = pd.read_csv('C:/Users/Sherwin/Desktop/NA12878-GATK3-chr21_2000.csv')
# reader_v = pd.read_csv('C:/Users/Sherwin/Desktop/output/NA12878-GATK3-chr21/NA12878-GATK3-chr21_validation.csv')


yt = reader['type']
xt = reader.drop(['type','CHROM','POS','PL'], 1)
X_train,X_test,y_train,y_test = train_test_split(xt,yt,test_size =0.97 ,random_state=1)

x_test = X_test.values
y_test = y_test.values.ravel()
X_train = X_train.values
y_train = y_train.values.ravel()
svc = SVC(probability=True,C=1000,gamma='scale').fit(X_train,y_train)
rf = RandomForestClassifier()
nf = GaussianNB()
rf.fit(X_train,y_train)
nf.fit(X_train,y_train)
pre_y = svc.predict(x_test)
confusion = confusion_matrix(y_test, pre_y)
print "Confusion matrix:\n{}".format(confusion)
print svc.score(X_train,y_train),svc.score(x_test,y_test)
print rf.score(X_train,y_train),rf.score(x_test,y_test)

precision,recall,thresholds = precision_recall_curve(y_test,svc.decision_function(x_test))

precision_rf,recall_rf,thresholds_rf = precision_recall_curve(y_test,rf.predict_proba(x_test)[:,1])
plt.plot(precision,recall,label="svc")
close_zero = np.argmin(np.abs(thresholds))
plt.plot(precision[close_zero],recall[close_zero],'o', markersize=10,
         label="threshold zero svc",fillstyle="none",c='k',mew=2)

close_default_rf = np.argmin(np.abs(thresholds_rf - 0.5))
plt.plot(precision_rf,recall_rf,label="rf")
plt.plot(precision[close_default_rf],recall[close_default_rf],'^', markersize=10,
         label="threshold rf 0.5 ",fillstyle="none",c='k',mew=2)


# plt.plot(precision,recall,label='precision recall curve')
plt.xlabel('Precision')
plt.ylabel('Recall')
plt.legend(loc="best")

ap_rf = average_precision_score(y_test,rf.predict_proba(x_test)[:,1])
ap_svc = average_precision_score(y_test,svc.decision_function(x_test))
print "Average precision of random forest: {:.3f}".format(ap_rf)
print "Average precision of svc: {:.3f}".format(ap_svc)
plt.savefig("C:/Users/Sherwin/Desktop/temp.png")

plt.show()