#!/usr/bin/python
# coding=utf-8
import pylab as pl
import numpy as np
from scipy import stats

n = 10
k = np.arange(n+1)
print k
pcoin = stats.binom.pmf(k, n, 0.5)
print pcoin
# pl.stem(k, pcoin, basefmt="k-")
# pl.margins(0.1)


n = 10
k = 6
p = np.linspace(0, 1, 100)

pbeta = stats.beta.pdf(p, k+3, n-k+1)
pl.plot(p, pbeta, label="k=5", lw=2)
pl.show()