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
    with open('h_latest_movie.csv', 'ab+') as csvfile:
        spamwriter = csv.writer(csvfile)
        spamwriter.writerow(data)
    csvfile.close()




def image_finder(soup,movie_name,movie_link):
    data = soup.select('a[href="%s"]'%movie_link)
    image_link = data[0].img["src"].encode("ascii","ignore")
    start  = image_link.find("img")
    image_link = "http://"+image_link[start:]
    filename = "h_latest_movie_image/"+movie_name  
    try:
        obj = br_hand.machanize_handler()
        br = obj.set_proxy()
        br.retrieve(image_link,filename)
        br.close()
    except:
        pass       
    return image_link

def latest_movieyou(links,movie_name, movie_link,watch,watch_link,image_link):
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
    collection = [movie_name,movie_link,"youtube",watch,em_link,image_link]
    logging.debug(tuple(collection))
    in_file(collection)


def latest_moviedaily(inks,movie_name, movie_link,watch,watch_link,image_link):
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
    collection = [movie_name,movie_link,"Dailymotion",watch,em_link,image_link]
    logging.debug(tuple(collection))
    in_file(collection)


    

def latest_movie3(links,movie_name, movie_link):
    page = proxy_module.main(movie_link)
    soup = BeautifulSoup(page)
    image_link = image_finder(soup,movie_name,movie_link)
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
                #latest_moviedaily(links,movie_name, movie_link,watch,watch_link,image_link)
                arg =(links,movie_name, movie_link,watch,watch_link,image_link)
                t = threading.Thread(target=latest_moviedaily,args=arg)
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
                #latest_movieyou(db,cursor,links,movie_name, movie_link,watch,watch_link,image_link)
                arg =(links,movie_name, movie_link,watch,watch_link,image_link)
                t = threading.Thread(target=latest_movieyou,args=arg)
                threads.append(t)
                t.start()
                logging.debug("Youtube")
                if len(threads)>5:
                    t.join()
                    del threads[:]
 
        else:
            pass


def latest_movie2(links):
    soup = BeautifulSoup(links)
    data = soup.find_all("a")
    threads = []
    for l in data:
        movie_name = l.get_text().encode("ascii","ignore")
        movie_link = l.get("href").encode("ascii","ignore")
        #latest_movie3(links,movie_name, movie_link)
        arg =(links,movie_name, movie_link)
        t = threading.Thread(target=latest_movie3,args=arg)
        threads.append(t)
        t.start()
        logging.debug("latest_movie2")
        if len(threads)>5:
                t.join()
                del threads[:]
        
        
        
        


def latest_movie():
    link = "http://www.hindilinks4u.net/"
    page = proxy_module.main(link)
    soup = BeautifulSoup(page)
    page.close()
    data = soup.find_all("h2",attrs={"class":"widgettitle"})
    for l in data:
        if str(l.get_text()).strip() =="Latest Movies":
            links = l.find_next("ul")
            
    latest_movie2(str(links))  
    

    

   



if __name__=="__main__":
    try:
        os.mkdir("h_latest_movie_image")
    except:
        pass
    collection = ["movie_name","movie_link","type","watch","em_link","image_link"]
    in_file(collection)
    latest_movie()
