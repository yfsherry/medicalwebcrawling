#!/usr/bin/env python
# coding: utf-8

# In[13]:


import urllib.request        #导入urllib.request库
import urllib.parse
import requests
from bs4 import BeautifulSoup
import json
import time
import pandas as pd
import numpy as np
import re
import os
import sys

def delete_tags(htmlString):
    s2 = re.sub(r'<.*?>','',htmlString)
    s2 = s2.replace('\n','')
    return s2

catalog=[]
path2=input('请输入目录文件路径：')
with open(path2,'r',encoding='GB2312') as f:
    for line in f:
        catalog.append(list(line.strip('\n').split(',')))
for _item in catalog:
    print("开始爬取词条："+ _item[0])
    c1=urllib.parse.quote(_item[0])
    b = "https://baike.baidu.com/item/"+c1
    a = urllib.request.urlopen(b)#打开指定网址
    html = a.read()              #读取网页源码
    html = html.decode("utf-8") #解码为unicode码

    soup = BeautifulSoup(html, 'html.parser')
    div = soup.find('div',class_='main-content')
    pattern1="(?<=\/span>).*(?=<\/h2>)"  #匹配小标题
    pattern2="(?<=label-module=\"para\">).*(?=<\/div>)"   #匹配内容

    #观察发现，小标题("适应症"等)单独写在一个class='para_title level-2'的div里
    #它的内容写在若干个和小标题平级的class="para"的div里，这些div是紧密排列的
    #它们的上级div可以通过class="main-content"索引到
    #对于一个项（"适应症"等下面所有内容）直到下一个项，排列格式是：
        #一个<div class="anchor-list">…</div>(意义不明)
        #一个<div class="para-title level-2">…</div>
        #若干个<div class="para">…<div>
    all_contents = div.contents
    #print(all_contents[1])
    my_set=[]
    for i in all_contents:
        my_set.append(str(i))

    temp_content=''
    temp_title=''
    content_set=[]
    title_set=[]

    num=[]

    for j in my_set:
        try: #先判断是不是小标题
            print("------"+delete_tags(re.search(pattern1,j).group())+"------")
            if(temp_content!=''):
                content_set.append(temp_content)
                temp_content=''
                title_set.append(temp_title)
            temp_title=delete_tags(re.search(pattern1,j).group())

            num.append("1")
            continue
        except Exception as e:
            try:
                print(">>>"+delete_tags(re.search(pattern2,j).group()))
                temp_content=temp_content+delete_tags(re.search(pattern2,j).group())

                num.append("2")

            except Exception as ee:
                num.append("0")

    content_set.append(temp_content)
    title_set.append(temp_title)
    df1=pd.DataFrame(columns=['内容'])
    for i in range(0,len(title_set)):
        df1.loc[title_set[i]]=content_set[i]
    path1=_item[0]+".csv"

    try:
        df1.to_csv(path1,encoding='utf_8_sig')
        print("\n爬取成功！文件存于 "+_item[0]+".csv\n")
    except Exception as e:
        print("\n爬取失败\n")
    

