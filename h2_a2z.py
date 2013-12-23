#!/usr/bin/env python 


import proxy_module 
from bs4 import BeautifulSoup
import re
import sys
import MySQLdb


def a2zdaily(db,cursor,link,movie_name,movie_link,watch,watch_link):
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
    #print link,movie_name,movie_link
    print watch,watch_link,em_link



def a2zyou(db,cursor,link,movie_name,movie_link,watch,watch_link):
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
    #print link,movie_name,movie_link
    print watch,watch_link,em_link
    
    

def a2zthird(db,cursor,link,movie_name,movie_link): 
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
                a2zdaily(db,cursor,link,movie_name,movie_link,watch,watch_link)
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
                a2zyou(db,cursor,link,movie_name,movie_link,watch,watch_link)
            #sys.exit() 
        else:
            pass
                  


def a2zsecond(db,cursor,link):
    page = proxy_module.main(link)
    soup = BeautifulSoup(page)
    data = soup.find_all("div",attrs={"class":"results_content"})
    for l in data:
        movie_name = l.get_text().encode("ascii","ignore")
        movie_link = l.a.get("href").encode("ascii","ignore")
        print  movie_name, movie_link
        a2zthird(db,cursor,link,movie_name,str(movie_link))
         
    



def a2z(db, cursor):
    
    link = "http://www.hindilinks4u.net/hindi-movies-a-to-z"
    page = proxy_module.main(link)
    soup = BeautifulSoup(page)
    data = soup.find_all("div",attrs={"id":"wp_page_numbers"})
    soup = BeautifulSoup(str(data))
    data = soup.find_all("a")
    # print data ok 
    page_list = []
    for l in data:
        if l.get("href") not in page_list:
            page_list.append(l.get("href"))
    #print page_list ok 
    for link in page_list:
        link = link.encode("ascii","ignore")
        #print type(link),
        #print link
        a2zsecond(db,cursor,link)
        

 
    

if __name__=="__main__":
    db = MySQLdb.connect("localhost","root","india123","hindi_link")
    cursor = db.cursor()
    a2z(db, cursor)
    db.close()
