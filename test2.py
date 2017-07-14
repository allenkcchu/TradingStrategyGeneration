# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 14:35:33 2017

@author: Allen
"""

import matplotlib.pyplot as plt;
import numpy as np;

iniP = np.random.uniform(-5,5,size=(2,9));
iniV = np.random.uniform(0.1,0.5,size=(2,9));
Boundary = [-5,5];

#plt.plot(iniP[1],iniP[0],'bo');
t = 0;
P = iniP+iniV*t;
V = iniV;
plt.close('all');
fig=plt.figure();
plt.ion();
plt.show();
#ax = fig.add_subplot(111);
#line = ax.plot(P[1,:], P[0,:], 'bo');
while t<=100:
    fig.clear();
    plt.axis([-5,5,-5,5]);
    Ptmp = P+V;
    Vtmp = V;
    for i in range(np.size(Ptmp,0)):
        for j in range(np.size(Ptmp,1)):
            if Ptmp[i,j]>5:
                P[i,j] = 2*Boundary[1]-Ptmp[i,j];
                V[i,j] = -1*Vtmp[i,j];
            elif Ptmp[i,j]<-5:
                P[i,j] = 2*Boundary[0]-Ptmp[i,j];
                V[i,j] = -1*Vtmp[i,j];
            else:
                P = Ptmp;
                V = Vtmp;
    t = t+1;
    plt.plot(P[1,:],P[0,:],'bo');
#    fig.canvas.draw();
    plt.pause(0.001);