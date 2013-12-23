#!/usr/bin/env python 


import proxy_module 
from bs4 import BeautifulSoup
import re
import sys
import MySQLdb

def catodaily(db, cursor,cat_name,cat_link,movie_name,movie_link,watch,watch_link):
    page = proxy_module.main(watch_link)
    soup = BeautifulSoup(page)
    if soup.find_all("iframe",attrs={"src",re.compile("dailymotion")}):
        em = soup.find_all("iframe",attrs={"src",re.compile("dailymotion")})
	em_link = em[0]["src"].encode("ascii","ignore")	
    elif soup.find_all("embed",attrs={"src":re.compile(r"")}):
	em = soup.find_all("embed",attrs={"src":re.compile(r"dailymotion")})
	em_link = em[0]["src"].encode("ascii","ignore")
    else:
	em_link = " on this link: " +watch_link.encode("ascii","ignore")
    print 
    #print cat_link,movie_link,watch_link
    print cat_name,movie_name
    print watch,em_link



def catoyou(db, cursor,cat_name,cat_link,movie_name,movie_link,watch,watch_link):
    page = proxy_module.main(watch_link)
    soup = BeautifulSoup(page)
    if soup.find_all("iframe",attrs={"src",re.compile("youtube")}):
        em = soup.find_all("iframe",attrs={"src",re.compile("youtube")})
	em_link = em[0]["src"].encode("ascii","ignore")
    elif soup.find_all("embed",attrs={"src":re.compile(r"")}):
	em = soup.find_all("embed",attrs={"src":re.compile(r"youtube")})
	em_link = em[0]["src"].encode("ascii","ignore")	
    else:
	em_link = " on this link: " +watch_link.encode("ascii","ignore")
    print 
    #print cat_link,movie_link,watch_link
    print cat_name,movie_name
    print watch,em_link


def cato3(db, cursor,cat_name,cat_link,movie_name,movie_link):
    page = proxy_module.main(movie_link)
    soup = BeautifulSoup(page)
    data = soup.find_all("strong")
    for l in data:
        s = l.get_text().encode("ascii","ignore")
        if re.search(r"Dailymotion",s):
            print 
            print "Dailymotion"
            para = l.find_next("p")
            soup2 = BeautifulSoup(str(para))
            data2 = soup2.find_all("a")
            for m in data2:
                #print m.get_text(),m.get("href") ok here
                watch = m.get_text().encode("ascii","ignore")
                watch_link = m.get("href").encode("ascii","ignore")
                catodaily(db, cursor,cat_name,cat_link,movie_name,movie_link,watch,watch_link)
            #sys.exit()
        elif re.search(r"Youtube",s):
            print 
            print "You tube"
            para = l.find_next("p")
            soup2 = BeautifulSoup(str(para))
            data2 = soup2.find_all("a")
            for m in data2:
                #print m.get_text(),m.get("href") ok here
                watch = m.get_text().encode("ascii","ignore")
                watch_link = m.get("href").encode("ascii","ignore")
                catoyou(db, cursor,cat_name,cat_link,movie_name,movie_link,watch,watch_link)
            #sys.exit() 
        else:
            pass

    

def cato2(db, cursor,cat_name,cat_link):
    page = proxy_module.main(cat_link)
    soup = BeautifulSoup(page)
    data = soup.find_all("div",attrs={"class":"results_content"})
    for l in data:
        movie_name = l.a.get_text().encode("ascii","ignore")
        movie_link = l.a.get("href").encode("ascii","ignore")
        #print film_name, film_link  #ok till here
        cato3(db, cursor,cat_name,cat_link,movie_name,movie_link)
    

def cato(db, cursor):
    link = "http://www.hindilinks4u.net/"
    page = proxy_module.main(link)
    soup = BeautifulSoup(page)
    data = soup.find_all("h2",attrs={"class":"widgettitle"})
    for l in data:
        if str(l.get_text()).strip() =="Categories":
            cat_list = l.find_next("ul")

    soup = BeautifulSoup(str(cat_list))
    data = soup.find_all("a")
    for l in data:
        cat_name= l.get_text().encode("ascii","ignore")
        cat_link= l.get("href").encode("ascii","ignore")
        cato2(db, cursor,cat_name,cat_link)
            
    

    
    
if __name__=="__main__":
    db = MySQLdb.connect("localhost","root","india123","hindi_link")
    cursor = db.cursor()
    cato(db, cursor)
    db.close()
