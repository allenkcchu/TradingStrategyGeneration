# -*- coding: utf-8 -*-
"""
Created on Thu Jul 06 00:40:39 2017

@author: allen
"""

import pandas as pd;
import numpy as np;
#import matplotlib.pyplot as plt;
#import grs;
from bs4 import BeautifulSoup as bs;
#import requests as rq;
import time;
import datetime;
from selenium import webdriver;

def month2code(month):
    if month == 'Jan':
        code = 1;
    elif month == 'Feb':
        code = 2;
    elif month == 'Mar':
        code = 3;
    elif month == 'Apr':
        code = 4;
    elif month == 'May':
        code = 5;
    elif month == 'Jun':
        code = 6;
    elif month == 'Jul':
        code = 7;
    elif month == 'Aug':
        code = 8;
    elif month == 'Sep':
        code = 9;
    elif month == 'Oct':
        code = 10;
    elif month == 'Nov':
        code = 11;
    elif month == 'Dec':
        code = 12;

    return code

def date2epoch(date):
    return int(time.mktime(datetime.datetime.strptime(date, '%Y-%m-%d').timetuple()))

def epoch2date(epoch):
    return time.strftime('%Y-%m-%d', time.localtime(epoch))

def fetchLatestStockCode():
    data = pd.read_html('http://isin.twse.com.tw/isin/C_public.jsp?strMode=2');
    data = data[0];
    stock = data[:][0];
    stockCode = [];
    for i in stock:
        i = i.encode('utf-8');
        print(i);
        if len(i.split('　')) == 2:
            stockCode.append(i.split('　')[0]);

    return stockCode

def execute_times(driver,times):
    for i in range(times + 1):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);");
        time.sleep(3);


def fetchingData(driver,stockCode,start,stop,database):
    url = 'https://finance.yahoo.com/quote/%s.tw/history?period1=%s&period2=%s&interval=1d&filter=history&frequency=1d' % (stockCode,start,stop);
    driver.get(url);
    time.sleep(2);
    execute_times(driver,20);
    soup = bs(driver.page_source, "lxml");

    head = [];
    thead = soup.find_all('thead',attrs = {'data-reactid' : '35'})[0];
    thead = thead.find_all('th');
    for i in thead:
        head.append(i.get_text().encode('utf-8'));


    data = []
    tdata = soup.find_all('tbody',attrs={'data-reactid' : '51'})[0].find_all('tr');
    for N,i in enumerate(tdata):
        dailyData = [];
        for M in range(len(i)):
            if M == 0:
                tmp = i.find_all('td')[M].get_text().encode('utf-8');
                month = int(month2code(tmp.split(' ')[0]));
                day = int(tmp.split(' ')[1].split(',')[0]);
                year = int(tmp.split(' ')[2]);
                dailyData.append(date2epoch(("%04d-%02d-%02d" % (year,month,day))));
            elif M == 6:
                    tmp = i.find_all('td')[M].get_text().encode('utf-8');
                    v = '';
                    for k in tmp.split(','):
                        v = v+k;
                    dailyData.append(v);
            else:
                dailyData.append(i.find_all('td')[M].get_text().encode('utf-8'));
        data.append(dailyData);

    databaseTmp = np.zeros((N,7));
    for N,i in enumerate(data):
        for M,j in enumerate(i):
            try:
                databaseTmp[N,M] = float(j);
            except:
                pass;

    databaseTmp = np.transpose(databaseTmp);
    databaseUnit = {};
    for N,i in enumerate(head):
        databaseUnit[i] = databaseTmp[N,:];

    database[stockCode] = databaseUnit;

    return database

if __name__ == "__main__":

    database = np.load("170708_database.npy");
    database = database.item()
#    database = {};
    start = str(date2epoch('2014-07-07'));
    stop = str(date2epoch('2017-07-07'));
    stockCode = ['5508'];

    driver = webdriver.Chrome();
    for i in stockCode:
        fetchingData(driver,i,start,stop,database);

    driver.quit();
