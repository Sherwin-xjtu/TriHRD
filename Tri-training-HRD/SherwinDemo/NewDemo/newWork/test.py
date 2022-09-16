#!/usr/bin/python
# coding=utf-8
import pymc3 as pm

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

np.random.seed(123)

alpha=1
sigma=1
beta =[1, 2.5]

N=100

X1=np.random.randn(N)
X2=np.random.randn(N)

Y=alpha + beta[0]*X1 + beta[1]*X2 + np.random.randn(N)*sigma
#
# fig1,ax1 = plt.subplots(1, 2, figsize=(10,4))
# ax1[0].scatter(X1, Y);ax1[0].set_xlabel('X1');ax1[0].set_ylabel('Y')
# ax1[1].scatter(X2, Y);ax1[1].set_xlabel('X2');ax1[1].set_ylabel('Y')
#
# fig2 = plt.figure(2)
# ax2 = Axes3D(fig2)
# ax2.scatter(X1,X2,Y)
# ax2.set_xlabel('X1')
# ax2.set_ylabel('X2')
# ax2.set_zlabel('Y')
# plt.show()


basic_model = pm.Model()
with basic_model:
    alpha=pm.Normal('alpha',mu=0,sd=10)
    beta=pm.Normal('beta',mu=0,sd=10,shape=2)
    sigma=pm.HalfNormal('sigma',sd=1)

    mu=alpha+beta[0]*X1+beta[1]*X2

    Y_obs=pm.Normal('Y_obs',mu=mu,sd=sigma,observed=Y)

# X, y = linear_training_data()
# with pm.Model() as linear_model:
#     weights = pm.Normal('weights', mu=0, sigma=1)
#     noise = pm.Gamma('noise', alpha=2, beta=1)
#     y_observed = pm.Normal('y_observed',
#                 mu=X.dot(weights),
#                 sigma=noise,
#                 observed=y)
#
#     prior = pm.sample_prior_predictive()
#     posterior = pm.sample()
#     posterior_pred = pm.sample_posterior_predictive(posterior)

# import matplotlib.pyplot as plt
# import numpy as np
# import scipy.stats as st
# plt.style.use('seaborn-darkgrid')
# x = np.linspace(0, 20, 200)
# alphas = [1., 2., 3., 7.5]
# betas = [.5, .5, 1., 1.]
# for a, b in zip(alphas, betas):
#     pdf = st.gamma.pdf(x, a, scale=1.0/b)
#
#     plt.plot(x, pdf, label=r'$\alpha$ = {}, $\beta$ = {}'.format(a, b))
# plt.xlabel('x', fontsize=12)
# plt.ylabel('f(x)', fontsize=12)
# plt.legend(loc=1)
# plt.show()