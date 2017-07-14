# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 13:55:44 2017

@author: Allen
"""
import time
import numpy as np
import matplotlib.pyplot as plt
 
plt.close('all');
fig=plt.figure()
#plt.axis([0,10,0,1])        #設調座標軸
 
plt.xlabel('x-axis')        #x軸名稱
plt.ylabel('y-axis')        #y軸名稱
plt.title('Title')          #標題
plt.grid(axis = 'y')        #y 軸增加 grid 虛線
plt.ion()                   #啟用互動模式，即時繪圖一定要設
#plt.show()                  #顯示圖表
#ax = fig.add_subplot(111)   #新增一個繪圖區域
x = []
y1 = []
y2 = []
i = 0
#line1, = ax.plot(x, y1, 'o-', lw=3) #新增一條線寬為 3 的縣
#line2, = ax.plot(x, y2, 'ro')       #新增一條紅線
while i <100:
    plt.pause(0.01);
#    time.sleep(0.05)                #模擬量測 
    tmp_y=np.random.random()        #產生 0~1 的亂數
    x.append(i)
    y1.append(tmp_y)
    y2.append(np.sin(i * np.pi / 90.0))
    plt.subplot(211);plt.plot(x,y1,'r');
    plt.subplot(212);plt.plot(x,y2,'b');
#    line1.set_data(x, y1)  
#    line2.set_data(x, y2)
    i+=1
#    ax.relim()                          #重算座標軸
#    ax.autoscale_view(True,True,True)   #重繪座標軸
    fig.canvas.draw()                   #重繪
 
     
#plt.savefig('c:\\plot.png',dpi=300,format='png')    #結果存檔
  
#raw_input('press Enter to close')       #暫停等 Enter 結束程式