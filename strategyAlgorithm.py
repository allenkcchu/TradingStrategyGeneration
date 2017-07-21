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
    valid = False;
    fee = 0.001425*price*dAmount;
    if fee <= 0.02:
        fee = 0.02
    tax = 0.003*price*dAmount;
    if trading == 'buy' and principal >= price*dAmount+fee:
        principal = principal-price*dAmount-fee;
        shareAmount = shareAmount+dAmount;
        valid = True;
    elif trading == 'sell' and shareAmount >= dAmount:
        principal = principal+price*dAmount-fee-tax;
        shareAmount = shareAmount-dAmount
        valid = True;
    return (principal,shareAmount,valid)

plt.close('all');
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
p4 = BBU-BBD;
p5 = (p0-BBD)/(BBU-BBD)*100;
praw = np.vstack((p0,p1,p2,p3,p4,p5));
dpraw = np.diff(praw,1);
dpraw = np.hstack((dpraw[:,0].reshape((len(dpraw),1)),dpraw));
std = np.std(praw,1);
mean = np.mean(praw,1);
pmod = np.zeros(np.shape(praw));
for N in range(np.size(praw,0)):
    pmod[N,:] = (praw[N,:]-mean[N])/std[N];


time0 = range(np.size(pmod,1));
price0 = pmod[0,:];
C = 1000;
capital = 1000;
share = 0;
timeB = [];
priceB = [];
timeS = [];
priceS = [];

#bcon1 = (pmod[0,:]<-1);
bcon1 = (praw[0,:]>=praw[1,:]);
bcon2 = (dpraw[1,:]>0);
bcon = np.vstack((bcon1,bcon2));
bpts = np.all(bcon,0);

#scon1 = (pmod[0,:]>1);
scon1 = (praw[0,:]<=praw[1,:])
scon2 = (dpraw[1,:]<0);
scon = np.vstack((scon1,scon2));
spts = np.all(scon,0);

plt.figure();plt.plot(time0,price0);
for i in time0:
    if bpts[i]:
        (capital,share,v) = Trade('buy',praw[0,i],1,capital,share);
        if v:
            print(capital);
            plt.plot(time0[i],price0[i],'bo');
    if spts[i]:
        (capital,share,v) = Trade('sell',praw[0,i],1,capital,share);
        if v:
            print(capital);
            plt.plot(time0[i],price0[i],'rx');

print("Return rate = %2.2f%%" % ((capital-C)/C*100));
print("Share in hand: %d" % share);
