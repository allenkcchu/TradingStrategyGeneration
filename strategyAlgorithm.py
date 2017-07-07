# -*- coding: utf-8 -*-
"""
Created on Fri Jul 07 16:07:53 2017

@author: Allen
"""

import numpy as np;
import matplotlib.pyplot as plt;

database = np.load('170508_Database.npy');
database = database.item();

closePriceArray = [];
for i in sorted(database.keys()):
    print(i)
    if len(closePriceArray) == 0:
        closePriceArray = np.hstack((closePriceArray,database[i][6,:]));
    else:
        closePriceArray = np.vstack((closePriceArray,database[i][6,:]));

r = np.corrcoef(closePriceArray.astype(np.float));