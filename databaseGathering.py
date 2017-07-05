# -*- coding: utf-8 -*-
"""
Created on Thu Jul 06 00:40:39 2017

@author: allen
"""

import pandas as pd;
import numpy as np;
import matplotlib.pyplot as plt;

data = pd.read_html('http://isin.twse.com.tw/isin/C_public.jsp?strMode=2');
data = data[0];
stock = data[:][0];
