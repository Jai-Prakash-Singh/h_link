#!/usr/bin/env python 


import proxy_module 
from bs4 import BeautifulSoup
import re
import firebug_proxy
import sys
import MySQLdb


def archivesyou(db,cursor,links,archives_name, archives_link,movie_name,movie_link,watch,watch_link):
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
    #print archives_name, archives_link,movie_name,movie_link,watch,watch_link
    #print archives_name,movie_name,watch,em_link
    sql = """insert ignore into archives(archives,archives_link,movie,movie_link,watch,watch_link) values("%s","%s","%s","%s","%s","%s")"""%(archives_name,archives_link,movie_name,movie_link,watch,em_link)
    print sql
    print sql
    cursor.execute(sql)
    db.commit()


def archivesdaily(db,cursor,links,archives_name, archives_link,movie_name,movie_link,watch,watch_link):
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
    #print archives_name, archives_link,movie_name,movie_link,watch,watch_link
    #print archives_name,archives_link,movie_name,watch,em_link
    sql = """insert ignore into archives(archives,archives_link,movie,movie_link,watch,watch_link) values("%s","%s","%s","%s","%s","%s")"""%(archives_name,archives_link,movie_name,movie_link,watch,em_link)
    print sql
    cursor.execute(sql)
    db.commit()


    

def archives4(db,cursor,links,archives_name, archives_link,movie_name,movie_link):
    page = proxy_module.main(movie_link)
    soup = BeautifulSoup(page)
    page.close()
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
                archivesdaily(db,cursor,links,archives_name, archives_link,movie_name,movie_link,watch,watch_link)
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
                archivesyou(db,cursor,links,archives_name, archives_link,movie_name,movie_link,watch,watch_link)
            #sys.exit() 
        else:
            pass

def archives3(db,cursor,links,archives_name, archives_link):
    page = proxy_module.main(archives_link)
    soup = BeautifulSoup(page)
    page.close()
    data = soup.find_all("div",attrs={"class":"results_content"})
    for l in data:
        movie_link = l.a.get("href").encode("ascii","ignore")
        movie_name = l.a.get_text().encode("ascii","ignore")
        archives4(db,cursor,links,archives_name, archives_link,movie_name,movie_link)
    

def archives2(db,cursor,links):
    soup = BeautifulSoup(links)
    data = soup.find_all("a")
    for l in data:
        archives_name = l.get_text().encode("ascii","ignore")
        archives_link = l.get("href").encode("ascii","ignore")
        #print archives_name,archives_link
        archives3(db,cursor,links,archives_name, archives_link)
        
        
        


def archives(db,cursor):
    link = "http://www.hindilinks4u.net/"
    page = proxy_module.main(link)
    soup = BeautifulSoup(page)
    page.close()
    data = soup.find_all("h2",attrs={"class":"widgettitle"})
    for l in data:
        if str(l.get_text()).strip() =="Archives":
            links = l.find_next("ul")
            
    archives2(db,cursor,str(links))  
    

    

   



if __name__=="__main__":
    db = MySQLdb.connect("localhost","root","india123","hindi_link")
    cursor = db.cursor()
    archives(db, cursor)
    db.close()
