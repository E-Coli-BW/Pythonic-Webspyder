# -*- coding: utf-8 -*-
"""
Created on Sun Apr  8 10:32:45 2018

@author: Haosong
"""
import requests
from bs4 import BeautifulSoup
import re
import  urllib.request
import os  
import urllib
# set headers
headers = {'User-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0'}
#url=r"https://www.osapublishing.org/ol/issue.cfm"
url=r"https://arxiv.org/list/cond-mat.mtrl-sci/new"
soup = BeautifulSoup(requests.get(url,headers=headers).content, 'html.parser')
#Paper Extractions
def getFile(url):
    file_name = url.split('/')[-1]
    u = urllib.request.urlopen(url)
    f = open(file_name, 'wb')

    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        f.write(buffer)
    f.close()
    print ("Sucessful to download" + " " + file_name)
def prepareData():
    letter_list= soup.find_all('div', attrs={'class': 'meta'})
    link_list=soup.findAll('span',attrs={'class':'list-identifier'})
    #link_list=link_list.find_all('a')
    link=link_list[0]
    link2=link_list[1]
    letter_dict={}
    TITLES=[]
    AUTHORS=[]
    ABSTRACT=[]
    DOWNLOAD=[]
    for link in link_list:
        
        link=str(link)
        objective='/pdf/'
        start=link.find(objective)
        end = link.find("title=\"Download PDF\"")
        link=link[start:end-2]
        DOWNLOAD.append("https://arxiv.org"+link+".pdf")        
    print(DOWNLOAD)  
    for letter in letter_list:
        #save papers into dictionary, key is title, value is author 
        title=letter.find('div', attrs={'class': 'list-title mathjax'}).get_text()
        #title=letter.find('span', attrs={'class': 'descriptor'})
        #title=list_title.find('span',attrs={'class': 'descriptor'})
        authors= [letter.find('div', attrs={'class': 'list-authors'}).get_text()]
        #abstract=letter.find('p',attrs={'class': 'mathjax'})
        abstract=[letter.findAll('p', attrs={'class': 'mathjax'})]
        '''
        print("should print abstract")
        '''
        abstract_buffer=str(abstract[0])
        abstract_buffer=abstract_buffer.replace("[<p class=\"mathjax\">","")
        abstract_buffer=abstract_buffer.replace("</p>]","")
        #print(abstract_buffer)
        '''
        print("End of test")
        '''
        letter_dict[title]= []
        letter_dict[title].append(authors[0])
        TITLES.append(title)
        '''
        print("Should print title")
        print(TITLES[-1])
        '''    
        authors=letter_dict[title][0]
        AUTHORS.append(authors)
        '''
        print("Should print author")
        print(AUTHORS[-1])
        '''  
        abstract=abstract_buffer
        #ABSTRACT
        ABSTRACT.append(abstract)
    
    for download in DOWNLOAD:
        for title in TITLES:
            getFile(download)    
    '''
    for title in TITLES:
        print(title)
    for author in AUTHORS:
        print(author)
    for abstract in ABSTRACT:
        if(abstract=="[]"):
            abstract=abstract.replace("[]","This paper has been replaced!")
        print(abstract)
    '''
    
    #print(len(ABSTRACT))   