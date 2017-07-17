# -*- coding: utf-8 -*-
"""
Created on Fri Jul 07 16:07:53 2017

@author: Allen
"""

import numpy as np;
import matplotlib.pyplot as plt;

# BB band
# Volume
# MA40

def movingAverage(data,averageLevel):
    dim = np.shape(data);
    if len(dim) == 1:
        MA = np.zeros((1,dim[0]-averageLevel));
        for N in range(averageLevel,dim[0]):
            MA[0,N-averageLevel] = np.sum(data[N-averageLevel:N])/averageLevel;
    else:
        MA = np.zeros((dim[0],dim[1]-averageLevel));
        for N in range(averageLevel,dim[1]):
            MA[:,N-averageLevel] = np.sum(data[:dim[0],N-averageLevel:N],axis=1)/averageLevel;
    return MA

def booleanTunnel(data,averageLevel):
    dim = np.shape(data);
    if len(dim) == 1:
        BB = np.zeros((1,dim[0]-averageLevel));
        for N in range(averageLevel,dim[0]):
            BB[:,N-averageLevel] = np.std(data[N-averageLevel:N]);
    else:
        BB = np.zeros((dim[0],dim[1]-averageLevel));
        for N in range(averageLevel,dim[1]):
            BB[:,N-averageLevel] = np.std(data[:dim[0],N-averageLevel:N],axis=1);
    MA = movingAverage(data,averageLevel);
    BBU = MA+2.1*BB;
    BBD = MA-2.1*BB;
    return (BBU,BBD)

def Trade(trading,price,dAmount,principal,shareAmount):
    fee = 0.001425*price*dAmount;
    if fee <= 0.02:
        fee = 0.02
    tax = 0.003*price*dAmount;
    if trading == 'buy':
        tradingFactor = -1;
        principal = principal+tradingFactor*price*dAmount-fee;
        shareAmount = shareAmount-tradingFactor*dAmount;
    elif trading == 'sell' and shareAmount >= dAmount:
        tradingFactor = 1;
        principal = principal+tradingFactor*price*dAmount-fee-tax;
        shareAmount = shareAmount-tradingFactor*dAmount
    return (principal,shareAmount)

#database = np.load('170508_Database.npy');
#database = database.item();
#data = database['2371'];
#closePriceArray = [];
#for i in sorted(database.keys()):
#    if len(closePriceArray) == 0:
#        closePriceArray = np.hstack((closePriceArray,database[i][6,:]));
#    else:
#        closePriceArray = np.vstack((closePriceArray,database[i][6,:]));
#
#r = np.corrcoef(closePriceArray.astype(np.float));

#v0 = np.transpose(data[6,:].astype(np.float));
#v1 = movingAverage(v0,40);
#BBU,BBD = booleanTunnel(v0,40);
#v0