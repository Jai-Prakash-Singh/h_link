#!/usr/bin/env python 


# -*- coding: latin-1 -*-
# -*- coding: iso-8859-15 -*-
# -*- coding: ascii -*-
# -*- coding: utf-8 -*-

import proxy_module 
from bs4 import BeautifulSoup
import re
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
    with open('h_tvs.csv', 'ab+') as csvfile:
        spamwriter = csv.writer(csvfile)
        spamwriter.writerow(data)
    csvfile.close()




def image_finder(soup,movie_name,movie_link):
    data = soup.select('a[href="%s"]'%movie_link)
    image_link = data[0].img["src"].encode("ascii","ignore")
    start  = image_link.find("img")
    image_link = "http://"+image_link[start:]
    filename = "h_tvs_image/"+movie_name  
    try:
        obj = br_hand.machanize_handler()
        br = obj.set_proxy()
        br.retrieve(image_link,filename)
        br.close()
    except:
        pass       
    return image_link

def tvsyou(links,show_name, show_link,watch,watch_link,image_link):
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
    collection = [show_name,show_link,"youtube",watch,em_link,image_link]
    logging.debug(tuple(collection))
    in_file(collection)


def tvsdaily(inks,show_name, show_link,watch,watch_link,image_link):
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
	em_link = " on this link: " +watch_link.encode("ascii","ignore")
    collection = [show_name,show_link,"Dailymotion",watch,em_link,image_link]
    logging.debug(tuple(collection))
    in_file(collection)


    

def tvs3(links,show_name, show_link):
    page = proxy_module.main(show_link)
    soup = BeautifulSoup(page)
    image_link = image_finder(soup,show_name,show_link)
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
                #tvsdaily(links,show_name, show_link,watch,watch_link,image_link)
                arg =(links,show_name, show_link,watch,watch_link,image_link)
                t = threading.Thread(target=tvsdaily,args=arg)
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
                #tvsyou(db,cursor,links,show_name, show_link,watch,watch_link,image_link)
                arg =(links,show_name, show_link,watch,watch_link,image_link)
                t = threading.Thread(target=tvsyou,args=arg)
                threads.append(t)
                t.start()
                logging.debug("Youtube")
                if len(threads)>5:
                    t.join()
                    del threads[:]
 
        else:
            pass


def tvs2(links):
    soup = BeautifulSoup(links)
    data = soup.find_all("a")
    threads = []
    for l in data:
        show_name = l.get_text().encode("ascii","ignore")
        show_link = l.get("href").encode("ascii","ignore")
        #tvs3(links,show_name, show_link)
        arg =(links,show_name, show_link)
        t = threading.Thread(target=tvs3,args=arg)
        threads.append(t)
        t.start()
        logging.debug("tvs2")
        if len(threads)>5:
                t.join()
                del threads[:]
        
        
        
        


def tvs():
    link = "http://www.hindilinks4u.net/"
    page = proxy_module.main(link)
    soup = BeautifulSoup(page)
    page.close()
    data = soup.find_all("h2",attrs={"class":"widgettitle"})
    for l in data:
        if str(l.get_text()).strip() =="TV Shows and Awards":
            links = l.find_next("ul")
            
    tvs2(str(links))  
    

    

   



if __name__=="__main__":
    try:
        os.mkdir("h_tvs_image")
    except:
        pass
    collection = ["show_name","show_link","type","watch","em_link","image_link"]
    in_file(collection)
    tvs()
