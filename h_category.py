#!/usr/bin/env python 


import proxy_module 
from bs4 import BeautifulSoup
import re
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

def catodaily(db, cursor,cat_name,cat_link,movie_name,movie_link,watch,watch_link,image_link):
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
    print 
    #print cat_link,movie_link,watch_link
    #print cat_name,movie_name
    #print watch,em_link
    sql = """insert ignore into category2(categories,cat_link,movie,movie_link,watch,watch_link,image_link) values("%s","%s","%s","%s","%s","%s","%s")"""%(cat_name,cat_link,movie_name,movie_link,watch,em_link,image_link)
    print sql
    cursor.execute(sql)
    db.commit()



def catoyou(db, cursor,cat_name,cat_link,movie_name,movie_link,watch,watch_link,image_link):
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
    #print cat_link,movie_link,watch_link
    #print cat_name,movie_name
    #print watch,em_link
    sql = """insert ignore into category2(categories,cat_link,movie,movie_link,watch,watch_link,image_link) values("%s","%s","%s","%s","%s","%s","%s")"""%(cat_name,cat_link,movie_name,movie_link,watch,em_link,image_link)
    print sql
    cursor.execute(sql)
    db.commit()


def cato3(db, cursor,cat_name,cat_link,movie_name,movie_link):
    page = proxy_module.main(movie_link)
    soup = BeautifulSoup(page)
    image_link=image_finder(soup,movie_name,movie_link)
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
                catodaily(db, cursor,cat_name,cat_link,movie_name,movie_link,watch,watch_link,image_link)
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
                catoyou(db, cursor,cat_name,cat_link,movie_name,movie_link,watch,watch_link,image_link)
            #sys.exit() 
        else:
            pass

    

def cato2(db, cursor,cat_name,cat_link):
    page = proxy_module.main(cat_link)
    soup = BeautifulSoup(page)
    page.close()
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
    page.close()
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
    try:
        os.mkdir("h_category_dir")
    except:
        pass
    db = MySQLdb.connect("localhost","root","india123","hindi_link")
    cursor = db.cursor()
    cato(db, cursor)
    db.close()
