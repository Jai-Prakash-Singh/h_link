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



def tvsyou(db,cursor,links,show_name, show_link,watch,watch_link,image_link):
    #page = firebug_proxy.main(watch_link)
    #page = page.encode("ascii","ignore")
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
    #print cat_link,show_link,watch_link
    #print show_name,show_link
    #print watch,em_link
    sql = """insert ignore into tvs2(show_name,link_link,watch,watch_link,image_link) values("%s","%s","%s","%s","%s")"""%(show_name,show_link,watch,em_link,image_link)
    print sql
    cursor.execute(sql)
    db.commit()


def tvsdaily(db,cursor,links,show_name, show_link,watch,watch_link,image_link):
    #page = firebug_proxy.main(watch_link)
    #page = page.encode("ascii","ignore")
    #soup = BeautifulSoup(page)
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
    #print cat_link,show_link,watch_link
    #print show_name,show_link
    #print watch,em_link
    sql = """insert ignore into tvs2(show_name,link_link,watch,watch_link,image_link) values("%s","%s","%s","%s","%s")"""%(show_name,show_link,watch,em_link,image_link)
    print sql
    cursor.execute(sql)
    db.commit()


    

def tvs3(db,cursor,links,show_name, show_link):
    page = proxy_module.main(show_link)
    soup = BeautifulSoup(page)
    image_link = image_finder(soup,show_name,show_link)
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
                tvsdaily(db,cursor,links,show_name, show_link,watch,watch_link,image_link)
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
                tvsyou(db,cursor,links,show_name, show_link,watch,watch_link,image_link)
            #sys.exit() 
        else:
            pass


def tvs2(db,cursor,links):
    soup = BeautifulSoup(links)
    data = soup.find_all("a")
    for l in data:
        show_name = l.get_text().encode("ascii","ignore")
        show_link = l.get("href").encode("ascii","ignore")
        #print show_name,show_link
        tvs3(db,cursor,links,show_name, show_link)
        
        
        


def tvs(db,cursor):
    link = "http://www.hindilinks4u.net/"
    page = proxy_module.main(link)
    soup = BeautifulSoup(page)
    page.close()
    data = soup.find_all("h2",attrs={"class":"widgettitle"})
    for l in data:
        if str(l.get_text()).strip() =="TV Shows and Awards":
            links = l.find_next("ul")
            
    tvs2(db,cursor,str(links))  
    

    

   



if __name__=="__main__":
    try:
        os.mkdir("h_tvs_dir")
    except:
        pass
    db = MySQLdb.connect("localhost","root","india123","hindi_link")
    cursor = db.cursor()
    tvs(db, cursor)
    db.close()
