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
    with open('h_actors.csv', 'ab+') as csvfile:
        spamwriter = csv.writer(csvfile)
        spamwriter.writerow(data)
    csvfile.close()


        


def image_finder(soup,movie_name,movie_link):
    data = soup.select('a[href="%s"]'%movie_link)
    image_link = data[0].img["src"].encode("ascii","ignore")
    start  = image_link.find("img")
    image_link = "http://"+image_link[start:]
    filename = "actor_image/"+movie_name  
    try:
        obj = br_hand.machanize_handler()
        br = obj.set_proxy()
        br.retrieve(image_link,filename)
        br.close()
    except:
        pass       
    return image_link
        
    


def actoryou(links,actor_name, actor_link,movie_name,movie_link,watch,watch_link,image_link):
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
    collection = [actor_name,actor_link,movie_name,movie_link,"Youtube",watch,em_link,image_link]
    logging.debug(tuple(collection))
    in_file(collection)


def actordaily(links,actor_name, actor_link,movie_name,movie_link,watch,watch_link,image_link):
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
    
    collection = [actor_name,actor_link,movie_name,movie_link,"Dailymotion",watch,em_link,image_link]
    logging.debug(tuple(collection))
    in_file(collection)

    

def actor4(links,actor_name, actor_link,movie_name,movie_link):
    page = proxy_module.main(movie_link)
    soup = BeautifulSoup(page)
    page.close()
    image_link=image_finder(soup,movie_name,movie_link)
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
                #actordaily(links,actor_name, actor_link,movie_name,movie_link,watch,watch_link)
                arg =(links,actor_name, actor_link,movie_name,movie_link,watch,watch_link,image_link)
                t = threading.Thread(target=actordaily,args=arg)
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
                #actoryou(links,actor_name, actor_link,movie_name,movie_link,watch,watch_link)
                arg =(links,actor_name, actor_link,movie_name,movie_link,watch,watch_link,image_link)
                t = threading.Thread(target=actoryou,args=arg)
                threads.append(t)
                t.start()
                logging.debug("Youtube")
                if len(threads)>10:
                    t.join()
                    del threads[:]
        else:
            pass

def actor3(links,actor_name, actor_link):
    page = proxy_module.main(actor_link)
    soup = BeautifulSoup(page)
    page.close()
    data = soup.find_all("div",attrs={"class":"results_content"})
    threads = []
    for l in data:
        movie_link = l.a.get("href").encode("ascii","ignore")
        movie_name = l.a.get_text().encode("ascii","ignore")
        #actor4(links,actor_name, actor_link,movie_name,movie_link)
        t = threading.Thread(target=actor4,args=(links,actor_name, actor_link,movie_name,movie_link))
        threads.append(t)   
        t.start()
        logging.debug("actor3")
        if len(threads)>10:
            t.join()
            del threads[:]
        

def actor2(links):
    soup = BeautifulSoup(links)
    data = soup.find_all("a")
    threads = []
    for l in data:
        actor_name = l.get_text().encode("ascii","ignore")
        actor_link = l.get("href").encode("ascii","ignore")
        #actor3(links,actor_name, actor_link)
        t = threading.Thread(target=actor3,args=(links,actor_name, actor_link))
        threads.append(t)   
        t.start()
        logging.debug("actor2")
        if len(threads)>10:
            t.join()
            del threads[:]
        
        


def actor():
    link = "http://www.hindilinks4u.net/"
    page = proxy_module.main(link)
    soup = BeautifulSoup(page)
    page.close()
    data = soup.find_all("h2",attrs={"class":"widgettitle"})
    for l in data:
        if str(l.get_text()).strip() =="Movies By Actors & Actresses":
            links = l.find_next("ul")
            
    actor2(str(links))  
    

    

   



if __name__=="__main__":
    try:
        os.mkdir("actor_image")
    except:
        pass
    collection =["actor_name","actor_link","movie_name","movie_link","Type","watch","em_link"]
    in_file(collection)
    actor()
