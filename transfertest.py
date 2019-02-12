# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 21:56:38 2019

@author: Asus
"""

import pandas as pd
import numpy as np
from sklearn import datasets, linear_model
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
from scipy import stats


dataset = pd.read_csv('person.csv')
X = dataset.iloc[:, [1,2,3,4]].values
y = dataset.iloc[:, 0].values

X = sm.add_constant(X)

MNlogit_mod = sm.MNLogit(y, X)

my_xnames = ['const', 'numstar', 'avgstar', 'cliqueden', 'totnodes']
MNlogit_mod.data.xnames = my_xnames

MNlogit_fit = MNlogit_mod.fit()
print(MNlogit_fit.summary())
print(MNlogit_fit.pred_table())

my_exog= ['numstar', 'avgstar', 'cliqueden', 'totnodes']
mfx = MNlogit_fit.get_margeff(atexog = my_exog)
print(mfx.summary())