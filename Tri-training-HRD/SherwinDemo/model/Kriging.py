import pyKriging
from pyKriging.krige import kriging
from pyKriging.samplingplan import samplingplan
import numpy as np

# The Kriging model starts by defining a sampling plan, we use an optimal Latin Hypercube here
# sp = samplingplan(2)
# X = sp.optimallhc(20)
X = np.array([[0.143158979,0.167],[0.143007460,0.197],[0.143324036,0.203],[0.143235865,0.749],[0.143226496,170],[0.165933477,0.052],[0.165933576,0.313],[0.182444038,0.51],[0.185310218,0.1012],[0.185312027,0.272]])

# Next, we define the problem we would like to solve
testfun = pyKriging.testfunctions().branin
y = testfun(X)
y = np.array([0.555999994278,0.97000002861,0.990000009537,0.981999993323999,0.5,0.574000000954,0.430000007153,0.944000005722,0.467999994755,0.467000007629])
# Now that we have our initial data, we can create an instance of a Kriging model
k = kriging(X, y, testfunction=testfun, name='simple')
k.train()
newpoints = [0.153249550,0.555]
print k.predict(newpoints),k.predict_var(newpoints),testfun(X)


# Now, five infill points are added. Note that the model is re-trained after each point is added
# numiter = 5
# for i in range(numiter):
#     print 'Infill iteration {0} of {1}....'.format(i + 1, numiter)
#     newpoints = k.infill(1)
#     for point in newpoints:
#         k.addPoint(point, testfun(point)[0])
#     k.train()

# And plot the results
# k.plot()