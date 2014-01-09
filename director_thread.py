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
    with open('h_director.csv', 'ab+') as csvfile:
        spamwriter = csv.writer(csvfile)
        spamwriter.writerow(data)
    csvfile.close()




def image_finder(soup,movie_name,movie_link):
    data = soup.select('a[href="%s"]'%movie_link)
    image_link = data[0].img["src"].encode("ascii","ignore")
    start  = image_link.find("img")
    image_link = "http://"+image_link[start:]
    filename = "director_image/"+movie_name  
    try:
        obj = br_hand.machanize_handler()
        br = obj.set_proxy()
        br.retrieve(image_link,filename)
        br.close()
    except:
        pass       
    return image_link



def directoryou(links,director_name, director_link,movie_name,movie_link,watch,watch_link,image_link):
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
    collection = [director_name,director_link,movie_name,movie_link,"youtube",watch,em_link,image_link]
    logging.debug(tuple(collection))
    in_file(collection)


def directordaily(links,director_name, director_link,movie_name,movie_link,watch,watch_link,image_link):
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
    collection = [director_name,director_link,movie_name,movie_link,"Dailymotion",watch,em_link,image_link]
    logging.debug(tuple(collection))
    in_file(collection)   


    

def director4(links,director_name, director_link,movie_name,movie_link):
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
                #directordaily(links,director_name, director_link,movie_name,movie_link,watch,watch_link,image_link)
                arg =(links,director_name, director_link,movie_name,movie_link,watch,watch_link,image_link)
                t = threading.Thread(target=directordaily,args=arg)
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
                #directoryou(links,director_name, director_link,movie_name,movie_link,watch,watch_link,image_link)
                arg =(links,director_name, director_link,movie_name,movie_link,watch,watch_link,image_link)
                t = threading.Thread(target=directoryou,args=arg)
                threads.append(t)
                t.start()
                logging.debug("Youtube")
                if len(threads)>5:
                    t.join()
                    del threads[:]

        else:
            pass

def director3(links,director_name, director_link):
    page = proxy_module.main(director_link)
    soup = BeautifulSoup(page)
    page.close()
    data = soup.find_all("div",attrs={"class":"results_content"})
    threads = []
    for l in data:
        movie_link = l.a.get("href").encode("ascii","ignore")
        movie_name = l.a.get_text().encode("ascii","ignore")
        #director4(links,director_name, director_link,movie_name,movie_link)
        arg =(links,director_name, director_link,movie_name,movie_link)
        t = threading.Thread(target=director4,args=arg)
        threads.append(t)
        t.start()
        logging.debug("director3")
        if len(threads)>5:
                t.join()
                del threads[:]
          

def director2(links):
    soup = BeautifulSoup(links)
    data = soup.find_all("a")
    threads = []
    for l in data:
        director_name = l.get_text().encode("ascii","ignore")
        director_link = l.get("href").encode("ascii","ignore")
        arg =(links,director_name, director_link)
        t = threading.Thread(target=director3,args=arg)
        threads.append(t)
        t.start()
        logging.debug("director2")
        if len(threads)>5:
                t.join()
                del threads[:]
        
        


def director():
    link = "http://www.hindilinks4u.net/"
    page = proxy_module.main(link)
    soup = BeautifulSoup(page)
    page.close()
    data = soup.find_all("h2",attrs={"class":"widgettitle"})
    for l in data:
        if str(l.get_text()).strip() =="Movies By Directors":
            links = l.find_next("ul")
            
    director2(str(links))  
    

    

   



if __name__=="__main__":
    try:
        os.mkdir("director_image")
    except:
        pass
    collection = ["director_name","director_link","movie_name","movie_link","Dailymotion","watch","em_link","image_link"]
    in_file(collection)
    director()

