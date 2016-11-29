# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 09:06:01 2016

@author: dingchaoqun
"""
#encoding:UTF-8
import urllib.request
import pandas as pd

from bs4 import BeautifulSoup
def getcontrolgraghbyOnestockcode(stockcode,bx):
    global url
    print(stockcode)
    url = "http://basic.10jqka.com.cn/16/%s/holder.html"%stockcode[-6:]
    data = urllib.request.urlopen(url).read()
    data = data.decode('gbk')
    soup =  BeautifulSoup(data, "lxml")
    holdlevel=soup.select('#holdlevel')
    leveldiv=holdlevel[0].select('div.pt5.bd')
    controltables = leveldiv[0].select('div.hierarchy-wrapper.J_hierarchy.clearfix')
    
    #controltable=controltables[0]
    for controltable in controltables:
        left=controltable.select('div.fl.hierarchy-left')
        left_hierarchy_num=left[0].select('th.hierarchy-num')[0].get_text()
        contrlfather=left[0].select('th.tl.hierarchy-name')
        
        for x in contrlfather:
            c=x.select('*')
            for y in c:
                y.extract()
        #contrlfather=left[0].find_all('th',class_='hierarchy-name')
        contrlfather[0].get_text().strip(' \r\n')
        
        mid=controltable.select('div.fl.hierarchy-mid')
        contrlpercent=mid[0].select('.hierarchy-disc.tip .upcolor')
        #contrlpercent=mid[0].find_all('span',class_='upcolor')
        contrlpercent[0].get_text().strip(' \r\n')
        
        
        right=controltable.select('div.fl.hierarchy-right.J_hierRight')
        right_hierarchy_num=right[0].select('th.hierarchy-num')[0].get_text()
        contrlsun=right[0].find_all('th',class_='hierarchy-name')
        
        for x in contrlsun:
            c=x.select('*')
            for y in c:
                y.extract()
        
        #c=contrlsun[0].select('*')
        #x.extract()
        #contrlsun[0].get_text().strip(' \r\n')
       
        #len(contrlfather)
        for x in range(len(contrlpercent)):
            a=left_hierarchy_num
            b=contrlfather[x if x<len(contrlfather) else len(contrlfather)-1].get_text().replace("\r"," ").strip()
            b1=contrlpercent[x].get_text().strip(' \r\n')
            d=right_hierarchy_num
            e=contrlsun[x if x<len(contrlsun) else len(contrlsun)-1].get_text().replace("\r"," ").strip()
            print("%s %s %s %s %s %s"%(stockcode,a,b,b1,d,e))
            row = []
            row.append(stockcode)
            row.append(a)
            row.append(b)
            row.append(b1)
            row.append(d)
            row.append(e)
            s= pd.Series(row)
            table.append(s)
            if bx is None or len(bx) == 0:
                bx=pd.DataFrame([row])
            else:
                bx=bx.append([row])
    return bx
        
def getcontrolgraph(stockcodes,bx=None):
    if  bx is None:
        bx = pd.DataFrame()
    for stockcode in stockcodes:
        olddata =None
        if len(bx) >0:
            olddata = bx[bx[0] == stockcode]
        if olddata is None or len(olddata) == 0:
            bx=getcontrolgraghbyOnestockcode(stockcode,bx)
    return bx

#import sys
df=pd.read_csv('stock.csv')
#f=open('log','w') 
#sys.stdout=f 

stockcodes=df.iloc[:,0]
table = []
store = pd.HDFStore('mydatacontrolgraph.h5')
if store.get_node('controlgraph') :
        bx=store['controlgraph']
        print ('ttt')
else:
    bx = None

bx = getcontrolgraph(stockcodes,bx=bx)

bx.loc[:,3][bx.loc[:,3]=='--']='100%'
store['controlgraph'] =bx
store.close()

wk =bx[bx.loc[:,0]=='SZ000002']     

bx.to_csv('pg.csv')  



    
    
    
