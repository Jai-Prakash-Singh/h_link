#!/usr/bin/env python 


import proxy_module 
from bs4 import BeautifulSoup
import re
import firebug_proxy
import image_proxy
import sys
import MySQLdb
import os


def image_finder2(soup,movie_name,movie_link):
    length = len(movie_link)
    movie_name2 = movie_name[:(length/2)]
    if soup.find_all("img",attrs={"title":movie_name}):
        data = soup.find_all("img",attrs={"title":movie_name})
        image_link = data[0]["src"].encode("ascii","ignore")
        image_proxy.image("actor_folder",image_link,movie_name)
        print image_link 
        return image_link
    elif soup.find_all("img",attrs={"title":re.compile(movie_name2)}):
        data = soup.find_all("img",attrs={"title":re.compile(movie_name2)})
        image_link = data[0]["src"].encode("ascii","ignore")
        image_proxy.image("actor_folder",image_link,movie_name2)
        print image_link 
        return image_link
    else:
        print  "no link for: "+movie_link



def image_finder(soup,movie_name,movie_link):
    data = soup.select('a[href^="%s"]'%movie_link)
    try:
        image_link = (data[0].img["src"]).encode("ascii","ignore")
        image_proxy.image("actor_folder",image_link,movie_name)
        print image_link
    except:
        print " image not get for: "+movie_link
        
        
    


def actoryou(db,cursor,links,actor_name, actor_link,movie_name,movie_link,watch,watch_link):
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
    #print actor_name, actor_link,movie_name,movie_link,watch,watch_link
    #print actor_name,movie_name,watch,em_link
    '''sql = """insert ignore into actor(actor_actoress,actor_actoress_link,movie,movie_link,watch,watch_link) values("%s","%s","%s","%s","%s","%s")"""%(actor_name,actor_link,movie_name,movie_link,watch,em_link)
    print sql
    print sql
    cursor.execute(sql)
    db.commit()'''


def actordaily(db,cursor,links,actor_name, actor_link,movie_name,movie_link,watch,watch_link):
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
    #print actor_name, actor_link,movie_name,movie_link,watch,watch_link
    #print actor_name,actor_link,movie_name,watch,em_link
    '''sql = """insert ignore into actor(actor_actoress,actor_actoress_link,movie,movie_link,watch,watch_link) values("%s","%s","%s","%s","%s","%s")"""%(actor_name,actor_link,movie_name,movie_link,watch,em_link)
    print sql
    cursor.execute(sql)
    db.commit()'''


    

def actor4(db,cursor,links,actor_name, actor_link,movie_name,movie_link):
    page = proxy_module.main(movie_link)
    soup = BeautifulSoup(page)
    page.close()
    image_finder(soup,movie_name,movie_link)
    data = soup.find_all("strong")
    for l in data:
        s = l.get_text().encode("ascii","ignore")
        if re.search(r"Dailymotion",s):
            #print 
            #print "Dailymotion"
            para = l.find_next("p")
            soup2 = BeautifulSoup(str(para))
            data2 = soup2.find_all("a")
            for m in data2:
                #print m.get_text(),m.get("href") ok here
                watch = m.get_text().encode("ascii","ignore")
                watch_link = m.get("href").encode("ascii","ignore")
                #actordaily(db,cursor,links,actor_name, actor_link,movie_name,movie_link,watch,watch_link)
            #sys.exit()
        elif re.search(r"Youtube",s):
            #print 
            #print "You tube"
            para = l.find_next("p")
            soup2 = BeautifulSoup(str(para))
            data2 = soup2.find_all("a")
            for m in data2:
                #print m.get_text(),m.get("href") ok here
                watch = m.get_text().encode("ascii","ignore")
                watch_link = m.get("href").encode("ascii","ignore")
                #actoryou(db,cursor,links,actor_name, actor_link,movie_name,movie_link,watch,watch_link)
            #sys.exit() 
        else:
            pass

def actor3(db,cursor,links,actor_name, actor_link):
    page = proxy_module.main(actor_link)
    soup = BeautifulSoup(page)
    page.close()
    data = soup.find_all("div",attrs={"class":"results_content"})
    for l in data:
        movie_link = l.a.get("href").encode("ascii","ignore")
        #print movie_link
        movie_name = l.a.get_text().encode("ascii","ignore")
        actor4(db,cursor,links,actor_name, actor_link,movie_name,movie_link)
    

def actor2(db,cursor,links):
    soup = BeautifulSoup(links)
    data = soup.find_all("a")
    for l in data:
        actor_name = l.get_text().encode("ascii","ignore")
        actor_link = l.get("href").encode("ascii","ignore")
        #print actor_name,actor_link
        actor3(db,cursor,links,actor_name, actor_link)
        
        
        


def actor(db,cursor):
    link = "http://www.hindilinks4u.net/"
    page = proxy_module.main(link)
    soup = BeautifulSoup(page)
    page.close()
    data = soup.find_all("h2",attrs={"class":"widgettitle"})
    for l in data:
        if str(l.get_text()).strip() =="Movies By Actors & Actresses":
            links = l.find_next("ul")
            
    actor2(db,cursor,str(links))  
    

    

   



if __name__=="__main__":
    try:
        os.mkdir("actor_folder")
    except:
        pass

    db = MySQLdb.connect("localhost","root","india123","hindi_link")
    cursor = db.cursor()
    actor(db, cursor)
    db.close()
