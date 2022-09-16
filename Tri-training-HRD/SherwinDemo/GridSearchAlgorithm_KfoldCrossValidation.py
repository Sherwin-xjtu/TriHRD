from sklearn.model_selection import GridSearchCV, KFold, train_test_split
from sklearn.metrics import make_scorer, accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import load_breast_cancer
import pandas as pd
data = load_breast_cancer()

# X_train, X_test, y_train, y_test = train_test_split(
#     data['data'], data['target'], train_size=0.8, random_state=0)

train = pd.read_csv('../AllData/labeled/trianing_data.csv')
x_train_columns = [x for x in train.columns if x not in ['type']]
X_train = train[x_train_columns]
y_train = train['type']

test = pd.read_csv('../AllData/labeled/test_data.csv')
x_test_columns = [x for x in train.columns if x not in ['type']]
X_test = train[x_test_columns]
y_test = train['type']

regressor = DecisionTreeClassifier(random_state=0)
parameters = {'max_depth': range(1, 6),'min_samples_split':range(2,30),
			'min_samples_leaf':range(1,10)}
scoring_fnc = make_scorer(accuracy_score)
kfold = KFold(n_splits=10)

grid = GridSearchCV(regressor, parameters, scoring_fnc, cv=kfold)
grid = grid.fit(X_train, y_train)
reg = grid.best_estimator_
best_parameters = grid.best_estimator_.get_params()
print 'Dior',best_parameters
print('best score: %f' % grid.best_score_)
print('best parameters:')
for key in parameters.keys():
    print('%s: %d' % (key, reg.get_params()[key]))

print('test score: %f' % reg.score(X_test, y_test))

pd.DataFrame(grid.cv_results_).T
