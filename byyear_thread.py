#!/usr/bin/env python 


# -*- coding: latin-1 -*-
# -*- coding: iso-8859-15 -*-
# -*- coding: ascii -*-
# -*- coding: utf-8 -*-

import proxy_module 
from bs4 import BeautifulSoup
import re
import firebug_proxy
import sys
import os
import csv
import threading
import time
import logging
from pyvirtualdisplay import Display
import br_hand


logging.basicConfig(level=logging.DEBUG,format='%(asctime)s (%(threadName)-2s) %(message)s',)



def in_file(data):
    with open('h_byyear.csv', 'ab+') as csvfile:
        spamwriter = csv.writer(csvfile)
        spamwriter.writerow(data)
    csvfile.close()


def image_finder(soup,movie_name,movie_link):
    data = soup.select('a[href="%s"]'%movie_link)
    image_link = data[0].img["src"].encode("ascii","ignore")
    start  = image_link.find("img")
    image_link = "http://"+image_link[start:]
    filename = "byyear_image/"+movie_name  
    try:
        obj = br_hand.machanize_handler()
        br = obj.set_proxy()
        br.retrieve(image_link,filename)
        br.close()
    except:
        pass       
    return image_link



def yearyou(links,year_name, year_link,movie_name,movie_link,watch,watch_link,image_link):
    page = proxy_module.main(watch_link)
    soup = BeautifulSoup(page)
    page.close() 
    if soup.find_all("iframe",attrs={"src":re.compile("youtube")}):
        em = soup.find_all("iframe",attrs={"src":re.compile("youtube")})
	em_link = em[0]["src"].encode("ascii","ignore")
    elif soup.find_all("embed",attrs={"src":re.compile(r"youtube")}):
	em = soup.find_all("embed",attrs={"src":re.compile(r"youtube")})
	em_link = em[0]["src"].encode("ascii","ignore")	
    else:
	em_link = " on this link: " +watch_link.encode("ascii","ignore")
    collection = [year_name,year_link,movie_name,movie_link,"Youtube",watch,em_link,image_link]
    logging.debug(tuple(collection))
    in_file(collection)


def yeardaily(links,year_name, year_link,movie_name,movie_link,watch,watch_link,image_link):
    page = proxy_module.main(watch_link)
    soup = BeautifulSoup(page)
    page.close()
    if soup.find_all("iframe",attrs={"src":re.compile("dailymotion")}):
        em = soup.find_all("iframe",attrs={"src":re.compile("dailymotion")})
	em_link = em[0]["src"].encode("ascii","ignore")	
    elif soup.find_all("embed",attrs={"src":re.compile(r"dailymotion")}):
	em = soup.find_all("embed",attrs={"src":re.compile(r"dailymotion")})
	em_link = em[0]["src"].encode("ascii","ignore")
    else:
	em_link = " on this link: "+watch_link.encode("ascii","ignore")
    collection = [year_name,year_link,movie_name,movie_link,"Dailymotion",watch,em_link,image_link]
    logging.debug(tuple(collection))
    in_file(collection)


    

def year4(links,year_name, year_link,movie_name,movie_link):
    page = proxy_module.main(movie_link)
    soup = BeautifulSoup(page)
    page.close()
    image_link = image_finder(soup,movie_name,movie_link)
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
                #yeardaily(links,year_name, year_link,movie_name,movie_link,watch,watch_link,image_link)
                arg =(links,year_name, year_link,movie_name,movie_link,watch,watch_link,image_link)
                t = threading.Thread(target=yeardaily,args=arg)
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
                #yearyou(links,year_name, year_link,movie_name,movie_link,watch,watch_link,image_link)
                arg =(links,year_name, year_link,movie_name,movie_link,watch,watch_link,image_link)
                t = threading.Thread(target=yearyou,args=arg)
                threads.append(t)
                t.start()
                logging.debug("Youtube")
                if len(threads)>10:
                    t.join()
                    del threads[:]
        else:
            pass

def year3(links,year_name, year_link):
    page = proxy_module.main(year_link)
    soup = BeautifulSoup(page)
    page.close()
    data = soup.find_all("div",attrs={"class":"results_content"})
    threads = []
    for l in data:
        movie_link = l.a.get("href").encode("ascii","ignore")
        movie_name = l.a.get_text().encode("ascii","ignore")
        #year4(links,year_name, year_link,movie_name,movie_link)
        t = threading.Thread(target=year4,args=(links,year_name, year_link,movie_name,movie_link))
        threads.append(t)   
        t.start()
        logging.debug("actor3")
        if len(threads)>10:
            t.join()
            del threads[:]

def year2(links):
    soup = BeautifulSoup(links)
    data = soup.find_all("a")
    threads = []
    for l in data:
        year_name = l.get_text().encode("ascii","ignore")
        year_link = l.get("href").encode("ascii","ignore")
        #year3(links,year_name, year_link)
        t = threading.Thread(target=year3,args=(links,year_name, year_link))
        threads.append(t)   
        t.start()
        logging.debug("actor2")
        if len(threads)>10:
            t.join()
            del threads[:]
        
        


def year():
    link = "http://www.hindilinks4u.net/"
    page = proxy_module.main(link)
    soup = BeautifulSoup(page)
    page.close()
    data = soup.find_all("div",attrs={"class":"tagcloud"})
    year2(str(data))  
    
    

    

   



if __name__=="__main__":
    try:
        os.mkdir("byyear_image")
    except:
        pass
    collection =["year_name","year_link","movie_name","movie_link","Type","watch","em_link","image_link"]
    in_file(collection)
    
    year()

