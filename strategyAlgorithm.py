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

def targetFunction(data,particleParams,plot):
    # particleParams:Benable/Bbparams/Bcomparison/Senable/Sbparams/Scomparison/level
    averageLevel = particleParams[6];

    # Standarize data
    BBU,BBD = bollingerBand(np.transpose(data[6,:].astype(np.float)),averageLevel);
    volume = np.transpose(data[1,:]).astype(np.float);
    # raw price
    p0 = np.transpose(data[6,averageLevel:].astype(np.float));
    # moving average
    p1 = movingAverage(np.transpose(data[6,:].astype(np.float)),averageLevel);
    # OBV
    p2 = onBalanceVolume(0.5*(np.transpose(data[4,averageLevel:]).astype(np.float)+np.transpose(data[5,averageLevel:]).astype(np.float)),volume,5);
    # increasing ratio
    p3 = (np.transpose(data[6,averageLevel:].astype(np.float))-np.transpose(data[3,averageLevel:].astype(np.float)))/np.transpose(data[6,averageLevel:].astype(np.float));
    # bandwidth
    p4 = BBU-BBD;
    # band-percentage
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

    bcon = [];
    if np.any(particleParams[0]):
        for N,i in enumerate(particleParams[0]):
            if particleParams[0][N]:
                if particleParams[2][N] == -2:
                    tmp = (pmod[N,:] <= particleParams[1][N]);
                elif particleParams[2][N] == -1:
                    tmp = (pmod[N,:] < particleParams[1][N]);
                elif particleParams[2][N] == 0:
                    tmp = (pmod[N,:] == particleParams[1][N]);
                elif particleParams[2][N] == 1:
                    tmp = (pmod[N,:] > particleParams[1][N]);
                elif particleParams[2][N] == 2:
                    tmp = (pmod[N,:] >= particleParams[1][N]);

                if len(bcon) == 0:
                    bcon = tmp;
                else:
                    bcon = np.vstack((bcon,tmp));

        try:
            if np.size(np.shape(bcon)) == 1:
                bpts = bcon;
            else:
                bpts = np.all(bcon,0);
        except:
            pass;
    else:
        bpts = np.ones((np.size(pmod,1)))==0

    scon = [];
    if np.any(particleParams[3]):
        for N,i in enumerate(particleParams[3]):
            if particleParams[3][N]:
                if particleParams[5][N] == -2:
                    tmp = (pmod[N,:] <= particleParams[4][N]);
                elif particleParams[5][N] == -1:
                    tmp = (pmod[N,:] < particleParams[4][N]);
                elif particleParams[5][N] == 0:
                    tmp = (pmod[N,:] == particleParams[4][N]);
                elif particleParams[5][N] == 1:
                    tmp = (pmod[N,:] > particleParams[4][N]);
                elif particleParams[5][N] == 2:
                    tmp = (pmod[N,:] >= particleParams[4][N]);

                if len(scon) == 0:
                    scon = tmp;
                else:
                    scon = np.vstack((scon,tmp));

        try:
            if np.size(np.shape(scon)) == 1:
                spts = scon;
            else:
                spts = np.all(scon,0);
        except:
            pass;
    else:
        spts = np.ones((np.size(pmod,1)))==0

    if plot == 1:
        plt.figure();plt.plot(time0,price0);
    for i in time0:
        if bpts[i]:
            (capital,share,v) = Trade('buy',praw[0,i],1,capital,share);
            if v and plot == 1:
                plt.plot(time0[i],price0[i],'bo');
        if spts[i]:
            (capital,share,v) = Trade('sell',praw[0,i],1,capital,share);
            if v and plot == 1:
                plt.plot(time0[i],price0[i],'rx');

    if share > 0:
        evalReturn = (capital+praw[0,i]*share*0.1-C)/C*100;
    else:
        evalReturn = (capital-C)/C*100;

    if plot == 1:
        print("Return rate = %2.2f%%" % (evalReturn));
        print("Share in hand: %d" % share);

    return evalReturn

if __name__ == '__main__':
    plt.close('all');
    plot = 1;
    database = np.load('170508_Database.npy');
    database = database.item();
    data = database['0056'];


    # searchingTime/particleAmount
#    iteration = 50;
    Period = 10;
    Number = 20;
    lowerBound = -5;
    upperBound = 5;
    groupRule = list([Period,Number,[lowerBound,upperBound]]);
    # velocity of bpts/spts
    Nv = np.random.uniform(-0.1,0.1,(2,6,groupRule[1]));
    # position of bpts/spts
    Np = np.random.uniform(-5,5,(2,6,groupRule[1]));
    # particle personality
    Nw = np.random.uniform(0,0.5,(2,groupRule[1]));
    Nw = np.concatenate((np.reshape(1-np.sum(Nw,0),(1,groupRule[1])),Nw),0);
    # b-enables/b-operators/s-enables/s-operators/statistical level
    nProperties = [(np.random.randint(0,2,(2,6,groupRule[1]))==1),np.random.randint(-2,3,(2,6,groupRule[1])),np.random.randint(5,51,groupRule[1])];

    # initial best memory
    NbestPosition = np.array(Np);
    NbestReturn = np.zeros((groupRule[1]));
    for N in range(groupRule[1]):
        NbestReturn[N] = targetFunction(data,list([nProperties[0][0,:,N],Np[0,:,N],nProperties[1][0,:,N],nProperties[0][1,:,N],Np[1,:,N],nProperties[1][1,:,N],nProperties[2][N]]),0);




    if plot != 0:
        fig = plt.figure();
    Titerate = 0;
    error = np.sum(np.sum(np.sum((Np-np.repeat(np.reshape(np.mean(Np,2),(Np.shape[0],Np.shape[1],1)),groupRule[1],2))**2,2),1),0);
    Time = np.array([]);
    Error = np.array([]);
    convergeError = 10;
    while(~(Titerate>1000 or convergeError<1e-1)):
        T = 0;
        while(T<groupRule[0]):
            for N in range(groupRule[1]):
                particle = list([nProperties[0][0,:,N],Np[0,:,N],nProperties[1][0,:,N],nProperties[0][1,:,N],Np[1,:,N],nProperties[1][1,:,N],nProperties[2][N]]);
                evalReturn = targetFunction(data,particle,0);
                if evalReturn>NbestReturn[N]:
                    NbestReturn[N] = evalReturn;
                    NbestPosition[:,:,N] = Np[:,:,N];


                for N,i in enumerate(Np+Nv):
                    for M,j in enumerate(i):
                        for L,k in enumerate(j):
                            if k<groupRule[2][0]:
                                Np[N,M,L] = 2*groupRule[2][0]-k
                                Nv[N,M,L] = -Nv[N,M,L];
                            elif k>groupRule[2][1]:
                                Np[N,M,L] = 2*groupRule[2][1]-k;
                                Nv[N,M,L] = -Nv[N,M,L];
                            else:
                                Np[N,M,L] = k;

            if plot == 1:
                fig.clear();
                plt.plot(Np[0,0,:],Np[1,0,:],'bo',ms = 20);
                plt.axis([-5,5,-5,5]);
                plt.pause(1e-5);
            T = T+1;
            Titerate = Titerate+1;
            error = np.sum(np.sum(np.sum((Np-np.repeat(np.reshape(np.mean(Np,2),(Np.shape[0],Np.shape[1],1)),groupRule[1],2))**2,2),1),0);
            Time = np.hstack((Time,Titerate));
            Error = np.hstack((Error,error));
            if plot == 2:
                plt.plot(Time,Error,'b-');plt.pause(1e-5);
            print("Time: %d" % (Titerate));
            if Titerate>50:
                convergeError = abs(error-np.sum(Error[-50:])/50);
                print(convergeError);
            
#            print(np.sum(np.sum(np.sum((Np-np.repeat(np.reshape(np.mean(Np,2),(Np.shape[0],Np.shape[1],1)),groupRule[1],2))**2,2),1),0));
#            print(T);

        # Modify velocity
        selfDv = (NbestPosition-Np)/(10*groupRule[0]);
        GbestPosition = NbestPosition[:,:,np.where(NbestReturn == np.max(NbestReturn))[0]][:,:,0];
        GbestPosition = np.reshape(GbestPosition,(np.shape(GbestPosition)[0],np.shape(GbestPosition)[1],1));
        GbestPosition = np.repeat(GbestPosition,groupRule[1],2);
        globalDv = (GbestPosition-Np)/(10*groupRule[0]);
        intefereFactor = np.random.normal(0,np.float(groupRule[2][1])/(100*groupRule[0]),np.shape(Np));

#        Nv = 0.1*Nv+0.3*selfDv+0.6*globalDv;
        for N in range(groupRule[1]):
            Nv[:,:,N] = 0.09*Nv[:,:,N] + 0.01*intefereFactor[:,:,N] + 0.3*selfDv[:,:,N] + 0.6*globalDv[:,:,N];

        


    N = np.where(NbestReturn == np.max(NbestReturn))[0][0];
    particle = list([nProperties[0][0,:,N],NbestPosition[0,:,N],nProperties[1][0,:,N],nProperties[0][1,:,N],NbestPosition[1,:,N],nProperties[1][1,:,N],nProperties[2][N]]);
    evalReturn = targetFunction(data,particle,1);