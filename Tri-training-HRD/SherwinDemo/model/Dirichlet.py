#!/usr/bin/python
# coding=utf-8
import re
import warnings

warnings.filterwarnings("ignore")
from scipy import stats
import pandas as pd
import numpy

from scipy.stats import dirichlet

import matplotlib.pyplot as plt
import numpy as np

TOL = 1.48e-8


def test_dirichret_distribution():
    print (dirichlet.pdf([0.6, 0.3, 0.1], [3, 2, 1]))
    print (dirichlet.logpdf([0.6, 0.3, 0.1], [1, 2, 3]))


if __name__ == '__main__':
    # scipy.stats库
    test_dirichret_distribution()  # beta分布