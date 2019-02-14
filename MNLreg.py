# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 21:56:38 2019

@author: Asus
"""

import pandas as pd
import statsmodels.api as sm


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

my_exog= ['const', 'numstar', 'avgstar', 'cliqueden', 'totnodes']
mfx = MNlogit_fit.get_margeff(at='overall', atexog = my_exog)
print(mfx.summary())
