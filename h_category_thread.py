#!/usr/bin/env python 

# -*- coding: latin-1 -*-
# -*- coding: iso-8859-15 -*-
# -*- coding: ascii -*-
# -*- coding: utf-8 -*-

import proxy_module 
from bs4 import BeautifulSoup
import re
import sys
import image_proxy
import MySQLdb
import os 
import csv
import threading
import time
import logging
import firebug_proxy
from pyvirtualdisplay import Display
import br_hand
import br_image


logging.basicConfig(level=logging.DEBUG,format='%(asctime)s (%(threadName)-2s) %(message)s',)

def in_file(data):
    with open('h_category2.csv', 'ab+') as csvfile:
        spamwriter = csv.writer(csvfile)
        spamwriter.writerow(data)
    csvfile.close()

def image_finder(soup,movie_name,movie_link):
    data = soup.select('a[href="%s"]'%movie_link)
    image_link = data[0].img["src"].encode("ascii","ignore")
    start  = image_link.find("img")
    image_link = "http://"+image_link[start:]
    #image_proxy.image("achieves_dir",image_link,movie_name)   
    filename = "achieves_dir2/"+movie_name  
    #br = br_image.main(image_link,filename)
    try:
        obj = br_hand.machanize_handler()
        br = obj.set_proxy()
        br.retrieve(image_link,filename)
        br.close()
    except:
        pass       
    return image_link
 

def catodaily(cat_name,cat_link,movie_name,movie_link,watch,watch_link,image_link):
    #page,driver= firebug_proxy.main(watch_link)
    page= proxy_module.main(watch_link)
    soup = BeautifulSoup(page)
    page.close()
    #driver.close()
    if soup.find_all("iframe",attrs={"src":re.compile("dailymotion")}):
        em = soup.find_all("iframe",attrs={"src":re.compile("dailymotion")})
	em_link = em[0]["src"].encode("ascii","ignore")	
    elif soup.find_all("embed",attrs={"src":re.compile(r"dailymotion")}):
	em = soup.find_all("embed",attrs={"src":re.compile(r"dailymotion")})
	em_link = em[0]["src"].encode("ascii","ignore")
    else:
	em_link = " on this link: " +watch_link.encode("ascii","ignore")
    
    collection = [cat_name,cat_link,movie_name,movie_link,"Daliymotion",watch,em_link,image_link]
    logging.debug(tuple(collection))
    in_file(collection)



def catoyou(cat_name,cat_link,movie_name,movie_link,watch,watch_link,image_link):
    #page,driver= firebug_proxy.main(watch_link)
    page= proxy_module.main(watch_link)
    soup = BeautifulSoup(page)
    page.close()
    #driver.close()
    if soup.find_all("iframe",attrs={"src":re.compile("youtube")}):
        em = soup.find_all("iframe",attrs={"src":re.compile("youtube")})
	em_link = em[0]["src"].encode("ascii","ignore")
    elif soup.find_all("embed",attrs={"src":re.compile(r"youtube")}):
	em = soup.find_all("embed",attrs={"src":re.compile(r"youtube")})
	em_link = em[0]["src"].encode("ascii","ignore")	
    else:
	em_link = " on this link: " +watch_link.encode("ascii","ignore")

    collection = [cat_name,cat_link,movie_name,movie_link,"youtube",watch,em_link,image_link]
    logging.debug(tuple(collection))
    in_file(collection)


def cato3(cat_name,cat_link,movie_name,movie_link):

    page = proxy_module.main(movie_link)
    soup = BeautifulSoup(page)
    image_link=image_finder(soup,movie_name,movie_link)
    page.close()
    data = soup.find_all("strong")
    threads = []
     
    for l in data:
        s = l.get_text().encode("ascii","ignore")
        if re.search(r"Dailymotion",s):
            para = l.find_next("p")
            soup2 = BeautifulSoup(str(para))
            data2 = soup2.find_all("a")
            for m in data2:
                watch = m.get_text().encode("ascii","ignore")
                watch_link = m.get("href").encode("ascii","ignore")
                arg =(cat_name,cat_link,movie_name,movie_link,watch,watch_link,image_link)
                t = threading.Thread(target=catodaily,args=arg)
                threads.append(t)
                t.start()
                logging.debug("Dailymotion")
                if len(threads)>5:
                    t.join()
                    del threads[:]

        elif re.search(r"Youtube",s):
            para = l.find_next("p")
            soup2 = BeautifulSoup(str(para))
            data2 = soup2.find_all("a")
            for m in data2:
                watch = m.get_text().encode("ascii","ignore")
                watch_link = m.get("href").encode("ascii","ignore")
                arg =(cat_name,cat_link,movie_name,movie_link,watch,watch_link,image_link)
                t = threading.Thread(target=catoyou,args=arg)
                threads.append(t)
                t.start()
                logging.debug("Youtube")
                if len(threads)>10:
                    t.join()
                    del threads[:]

        else:
            pass

    

def cato2(cat_name,cat_link):
    page = proxy_module.main(cat_link)
    soup = BeautifulSoup(page)
    page.close()
    data = soup.find_all("div",attrs={"class":"results_content"})
    threads = []
    for l in data:
        movie_name = l.a.get_text().encode("ascii","ignore")
        movie_link = l.a.get("href").encode("ascii","ignore")
        #cato3(cat_name,cat_link,movie_name,movie_link)
        t = threading.Thread(target=cato3,args=(cat_name,cat_link,movie_name,movie_link))
        threads.append(t)
        t.start()
        logging.debug("cato2")
        if len(threads)>10:
            t.join()
            del threads[:]


def cato():
    link = "http://www.hindilinks4u.net/"
    page = proxy_module.main(link)
    soup = BeautifulSoup(page)
    page.close()
    data = soup.find_all("h2",attrs={"class":"widgettitle"})
    for l in data:
        if str(l.get_text()).strip() =="Categories":
            cat_list = l.find_next("ul")

    soup = BeautifulSoup(str(cat_list))
    data = soup.find_all("a")
    threads = []
    for l in data:
        cat_name= l.get_text().encode("ascii","ignore")
        cat_link= l.get("href").encode("ascii","ignore")
        #cato2(cat_name,cat_link)
        t = threading.Thread(target=cato2,args=(cat_name,cat_link))
        threads.append(t)   
        t.start()
        logging.debug("cato")
        if len(threads)>10:
            t.join()
            del threads[:]
      
    
    
if __name__=="__main__":
    try:
        os.mkdir("achieves_dir2")
    except:
        pass

    try:
        os.mkdir("h_category_dir")     
    except:
        pass

    collection =["cat_name","cat_link","movie_name","movie_link","type","watch","em_link","image_link"]
    in_file(collection)
    cato()

