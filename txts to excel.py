# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 22:07:51 2020

@author: WYQ
"""

import os
import pandas
import codecs
import glob
import pandas as pd
os.getcwd()
os.chdir('C:/Users/WYQ/Desktop/UGC/dxy 爬虫/result2/保济丸')
def txtcombine():
    files = glob.glob('*.txt')
    all = codecs.open('all.txt','a')
    for filename in files: 
        print(filename) 
        fopen=codecs.open(filename,'r',encoding='utf-8') 
        lines=[] 
        lines=fopen.readlines() 
        fopen.close() 
        for line in lines: 
            for x in line: 
                all.write(x)
    
 #读取为DataFrame格式
    all1 = pd.read_csv('all.txt',sep=' ',encoding='GB2312')
 #保存为csv格式
    print(all1)
    all1.to_csv('all.csv',encoding='unicode_escape')
  
txtcombine()