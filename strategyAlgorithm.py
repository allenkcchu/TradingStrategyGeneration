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
    MA = np.zeros((len(data)-averageLevel));
    for N in range(len(data)):
        if N >= averageLevel:
            MA[N-averageLevel] = np.sum(data[N-averageLevel:N])/averageLevel;
    return MA

def bollingerBand(data,averageLevel):
    BB = np.zeros((len(data)-averageLevel));
    for N in range(len(data)):
        if N >= averageLevel:
            BB[N-averageLevel] = np.std(data[N-averageLevel:N])
    MA = movingAverage(data,averageLevel);
    BBU = MA+2.1*BB;
    BBD = MA-2.1*BB;
    return (BBU,BBD)

def onBalanceVolume(data,volume,averageLevel):
    sign = np.hstack((0,np.sign(np.diff(data))));
    OBV = np.zeros((len(data)));
    for N in range(len(data)):
        if N < averageLevel:
            if N == 0:
                OBV[N] = 0;
            else:
                OBV[N] = OBV[N-1]+sign[N]*volume[N];
        else:
            OBV[N] = np.sum(OBV[N-averageLevel:N])/averageLevel+sign[N]*volume[N];

    return OBV

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

database = np.load('170508_Database.npy');
database = database.item();
data = database['2330'];
#closePriceArray = [];
#for i in sorted(database.keys()):
#    if len(closePriceArray) == 0:
#        closePriceArray = np.hstack((closePriceArray,database[i][6,:]));
#    else:
#        closePriceArray = np.vstack((closePriceArray,database[i][6,:]));
#
#r = np.corrcoef(closePriceArray.astype(np.float));


v0 = np.transpose(data[6,:].astype(np.float));
v1 = movingAverage(v0,40);
v2 = 0.5*(np.transpose(data[4,:]).astype(np.float)+np.transpose(data[5,:]).astype(np.float));
v3 = np.transpose(data[1,:]).astype(np.float);
v4_1 = onBalanceVolume(v2,v3,1);
v4_2 = onBalanceVolume(v2,v3,5);
v4_3 = onBalanceVolume(v2,v3,10);

BBU,BBD = bollingerBand(v0,40);
#v0