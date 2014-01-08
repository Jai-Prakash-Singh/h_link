#!/usr/bin/env python 


import proxy_module 
from bs4 import BeautifulSoup
import re
import firebug_proxy
import sys
import image_proxy
import MySQLdb
import os 


def image_finder(soup,movie_name,movie_link):
    #print movie_link
    try:
        data = soup.select('a[href="%s"]'%movie_link)
        image_link = data[0].img["src"].encode("ascii","ignore")
        image_proxy.image("achieves_dir",image_link,movie_name)
        return image_link
    except:
        return " image not get for: "+movie_link


def directoryou(db,cursor,links,director_name, director_link,movie_name,movie_link,watch,watch_link,image_link):
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
    print 
    print 
    #print director_name, director_link,movie_name,movie_link,watch,watch_link
    #print director_name,movie_name,watch,em_link
    sql = """insert ignore into director(diector,director_link,movie,movie_link,watch,watch_link,image_link) values("%s","%s","%s","%s","%s","%s","%s")"""%(director_name,director_link,movie_name,movie_link,watch,em_link,image_link)
    print sql
    cursor.execute(sql)
    db.commit()


def directordaily(db,cursor,links,director_name, director_link,movie_name,movie_link,watch,watch_link,image_link):
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
    print 
    #print director_name, director_link,movie_name,movie_link,watch,watch_link
    #print director_name,director_link,movie_name,watch,em_link
    sql = """insert ignore into director(diector,director_link,movie,movie_link,watch,watch_link,image_link) values("%s","%s","%s","%s","%s","%s","%s")"""%(director_name,director_link,movie_name,movie_link,watch,em_link,image_link)
    print sql
    cursor.execute(sql)
    db.commit()


    

def director4(db,cursor,links,director_name, director_link,movie_name,movie_link):
    page = proxy_module.main(movie_link)
    soup = BeautifulSoup(page)
    page.close()
    image_link=image_finder(soup,movie_name,movie_link)
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
                directordaily(db,cursor,links,director_name, director_link,movie_name,movie_link,watch,watch_link,image_link)
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
                directoryou(db,cursor,links,director_name, director_link,movie_name,movie_link,watch,watch_link,image_link)
            #sys.exit() 
        else:
            pass

def director3(db,cursor,links,director_name, director_link):
    page = proxy_module.main(director_link)
    soup = BeautifulSoup(page)
    page.close()
    data = soup.find_all("div",attrs={"class":"results_content"})
    for l in data:
        movie_link = l.a.get("href").encode("ascii","ignore")
        movie_name = l.a.get_text().encode("ascii","ignore")
        director4(db,cursor,links,director_name, director_link,movie_name,movie_link)
    

def director2(db,cursor,links):
    soup = BeautifulSoup(links)
    data = soup.find_all("a")
    for l in data:
        director_name = l.get_text().encode("ascii","ignore")
        director_link = l.get("href").encode("ascii","ignore")
        #print director_name,director_link
        director3(db,cursor,links,director_name, director_link)
        
        
        


def director(db,cursor):
    link = "http://www.hindilinks4u.net/"
    page = proxy_module.main(link)
    soup = BeautifulSoup(page)
    page.close()
    data = soup.find_all("h2",attrs={"class":"widgettitle"})
    for l in data:
        if str(l.get_text()).strip() =="Movies By Directors":
            links = l.find_next("ul")
            
    director2(db,cursor,str(links))  
    

    

   



if __name__=="__main__":
    try:
        os.mkdir("director_dir")
    except:
        pass
  
    db = MySQLdb.connect("localhost","root","india123","hindi_link")
    cursor = db.cursor()
    director(db, cursor)
    db.close()
