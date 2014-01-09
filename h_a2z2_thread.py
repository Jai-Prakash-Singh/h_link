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
    with open('h_a2z2.csv', 'ab+') as csvfile:
        spamwriter = csv.writer(csvfile)
        spamwriter.writerow(data)
    csvfile.close()




def image_finder(soup,movie_name,movie_link):
    data = soup.select('a[href="%s"]'%movie_link)
    image_link = data[0].img["src"].encode("ascii","ignore")
    start  = image_link.find("img")
    image_link = "http://"+image_link[start:]
    filename = "h2_a2Z_image/"+movie_name  
    try:
        obj = br_hand.machanize_handler()
        br = obj.set_proxy()
        br.retrieve(image_link,filename)
        br.close()
    except:
        pass       
    return image_link


def a2zdaily(link,movie_name,movie_link,watch,watch_link,image_link):
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
    collection = [link,movie_name,movie_link,"Dailymotion",watch,em_link,image_link]
    logging.debug(tuple(collection))
    in_file(collection)




def a2zyou(link,movie_name,movie_link,watch,watch_link,image_link):
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
    collection = [link,movie_name,movie_link,"Youtube",watch,em_link,image_link]
    logging.debug(tuple(collection))
    in_file(collection)
    
    

def a2zthird(link,movie_name,movie_link): 
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
                #a2zdaily)(link,movie_name,movie_link,watch,watch_link,image_link)
                arg =(link,movie_name,movie_link,watch,watch_link,image_link)
                t = threading.Thread(target=a2zdaily,args=arg)
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
                #a2zyou(link,movie_name,movie_link,watch,watch_link,image_link)
                arg =(link,movie_name,movie_link,watch,watch_link,image_link)
                t = threading.Thread(target=a2zyou,args=arg)
                threads.append(t)
                t.start()
                logging.debug("Youtube")
                if len(threads)>10:
                    t.join()
                    del threads[:]
        else:
            pass
                  


def a2zsecond(link):
    page = proxy_module.main(link)
    soup = BeautifulSoup(page)
    page.close()
    data = soup.find_all("div",attrs={"class":"results_content"})
    threads = []
    for l in data:
        movie_name = l.get_text().encode("ascii","ignore")
        movie_link = l.a.get("href").encode("ascii","ignore")
        #a2zthird(link,movie_name,str(movie_link))
        t = threading.Thread(target=a2zthird,args=(link,movie_name,str(movie_link)))
        threads.append(t)   
        t.start()
        logging.debug("a2zsecond")
        if len(threads)>10:
            t.join()
            del threads[:]
         
    



def a2z():
    
    link = "http://www.hindilinks4u.net/hindi-movies-a-to-z"
    page = proxy_module.main(link)
    soup = BeautifulSoup(page)
    page.close()
    data = soup.find_all("div",attrs={"id":"wp_page_numbers"})
    soup = BeautifulSoup(str(data))
    data = soup.find_all("a")
    page_list = []
    threads = []
    for l in data:
        if l.get("href") not in page_list:
            page_list.append(l.get("href"))

    for link in page_list:
        link = link.encode("ascii","ignore")
        #a2zsecond(link)
        t = threading.Thread(target=a2zsecond,args=(link,))
        threads.append(t)   
        t.start()
        logging.debug("a2z")
        if len(threads)>10:
            t.join()
            del threads[:]
        

 
    

if __name__=="__main__":
    try:
        os.mkdir("h2_a2Z_image")
    except:
        pass
    collection = ["link","movie_name","movie_link","Dailymotion","watch","em_link","image_link"]
    in_file(collection)
    a2z()

