#!/usr/bin/env python 


import proxy_module 
from bs4 import BeautifulSoup
import re
import sys



def latest_movie():
    link1 = "http://www.hindilinks4u.net/"
    page1 = proxy_module.main(link1)
    soup1 = BeautifulSoup(page1)
    page1.close()
    data1 = soup1.find_all("ul", attrs={"class":"xoxo blogroll"})
    soup2 = BeautifulSoup(str(data1))
    data2 = soup2.find_all("li")
    for l in data2:
        link3 = l.a.get("href") 
	title =l.get_text()
        #print link3
	print title
        print "main link: " +link3
        page3 = proxy_module.main(link3)
	soup3 = BeautifulSoup(page3)
	if soup3.find_all("div",attrs={"class":"results_content"}):
	    data3 = soup3.find_all("div", attrs={"class":"results_content"})
	    for m in data3:
	        film_link = m.a.get("href")
		film_name  = m.get_text()
                print film_name
		page4 = proxy_module.main(film_link)
		soup4 = BeautifulSoup(page4)
		data5 = soup4.find_all(text=re.compile(r"Dailymotion"))
		for n in data5:
		    dm_block = n.parent.find_next("p")
		    dm_links = dm_block.find_all("a")
                    for p in dm_links:
                        print p.get_text()
		        link4 = str(p.get("href"))
                        #print link4
                        page4 = proxy_module.main(link4)
			soup5 = BeautifulSoup(page4)
			if soup5.find_all("iframe",attrs={"src",re.compile("dailymotion")}):
			    em = soup5.find_all("iframe",attrs={"src",re.compile("dailymotion")})
			    em_link = em[0]["src"]
			    print em_link
			elif soup5.find_all("iframe",attrs={"src":re.compile(r"dailymotion")}):
			    em = soup5.find_all("iframe",attrs={"src":re.compile(r"dailymotion")})
			    em_link = em[0]["src"]
			    print em_link
		        else:
			    print " on this link: " +link4
        elif soup3.find_all(text=re.compile(r"Dailymotion")):
            data3 = soup3.find_all(text=re.compile(r"Dailymotion"))
	    for l in data3:
	        dm_block = l.parent.find_next("p")
	        dm_links = dm_block.find_all("a")
	        for m  in dm_links:
		    link4 =  str(m.a.get("href"))
		    page4 = proxy_module.main(link4)
		    soup5 = BeautifulSoup(page4)
		    if soup5.find_all("iframe",attrs={"src",re.compile("dailymotion")}):
		        em = soup5.find_all("iframe",attrs={"src",re.compile("dailymotion")})
		        em_link = em[0]["src"]
		        print em_link
		    elif soup5.find_all("iframe",attrs={"src":re.compile(r"dailymotion")}):
		        em = soup5.find_all("iframe",attrs={"src":re.compile(r"dailymotion")})
		        em_link = em[0]["src"]
		        print em_link
  		    else:
		        print " on this link: " +link4
        else:
	    print "sourse on other motion"
 





	    


 

                         
                        #print data6
                        #print 



 

 
			
		        
                    
                 
                    
		









if __name__=="__main__":
    latest_movie()

