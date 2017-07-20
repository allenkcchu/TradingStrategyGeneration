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
data = database['0056'];
#closePriceArray = [];
#for i in sorted(database.keys()):
#    if len(closePriceArray) == 0:
#        closePriceArray = np.hstack((closePriceArray,database[i][6,:]));
#    else:
#        closePriceArray = np.vstack((closePriceArray,database[i][6,:]));
#
#r = np.corrcoef(closePriceArray.astype(np.float));

averageLevel = 20;
BBU,BBD = bollingerBand(np.transpose(data[6,:].astype(np.float)),averageLevel);
volume = np.transpose(data[1,:]).astype(np.float);
p0 = np.transpose(data[6,averageLevel:].astype(np.float));
p1 = movingAverage(np.transpose(data[6,:].astype(np.float)),averageLevel);
p2 = onBalanceVolume(0.5*(np.transpose(data[4,averageLevel:]).astype(np.float)+np.transpose(data[5,averageLevel:]).astype(np.float)),volume,5);
p3 = (np.transpose(data[6,averageLevel:].astype(np.float))-np.transpose(data[3,averageLevel:].astype(np.float)))/np.transpose(data[6,averageLevel:].astype(np.float));
p4 = (p0-BBD)/(BBU-BBD)*100;
position = np.vstack((p0,p1,p2,p3,p4));
dposition = np.diff(position,1);
std = np.std(position,1);
mean = np.mean(position,1);
pmod = np.zeros(np.shape(position));
for N in range(np.size(position,0)):
    pmod[N,:] = (position[N,:]-mean[N])/std[N];


time1 = [];
price1 = [];
time2 = [];
price2 = [];

fig=plt.figure();
plt.ion();
plt.show();
for N in range(len(p0)):
    fig.clear();
    plt.axis([0,500,-3,3]);
    
    time1.append(N);
    price1.append(pmod[0,N]);
    if pmod[0,N] <= -1:
        time2.append(N);
        price2.append(pmod[0,N]);
        plt.plot(time1,price1,'k',time2,price2,'ro')
    else:
        plt.plot(time1,price1,'k',time2,price2,'ro')
    
    plt.pause(0.01);