import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
# %matplotlib inline

test = pd.read_csv('../AllData/labeled/test_data.csv')
x_test_columns = [x for x in test.columns if x not in ['type']]
X_test = test[x_test_columns]
# 'CHROM','POS','QUAL','MQ','QD','ReadPosRankSum','FS','MQRankSum','AF','AC','HaplotypeScore','BaseQRankSum'
X_test = X_test.drop(['ReadPosRankSum','FS','MQRankSum'],1)
y_test = test['type']
y_test = np.array(y_test)
X_test = np.array(X_test)
plt.scatter(X_test[:, 0], X_test[:, 1], marker='o', c=y_test)
plt.show()