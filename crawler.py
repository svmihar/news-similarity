from bs4 import BeautifulSoup
import requests
import time
import random
import json 
import io 
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pprint import pprint
import csv
import logging

logger = logging.Logger('catch_all')
headers = {'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}

def save_csv(result):
    # writing dict(key, value) inside a list
    for items in result: 
            print()
    csv_columns = items.keys()
    csv_file = 'dict.csv'
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in result:
                writer.writerow(data)
    except IOError:
        print("I/O error") 

def crawl_kompas(url="https://indeks.kompas.com/ekonomi/",date='2019-01-07'):
    url = url+date+'/'
    result = []
    req = requests.get(url, headers = headers)
    soup = BeautifulSoup(req.content, "lxml")

    #looping through paging
    for i in range(1,5):
        waktu = random.randint(1,5)
        time.sleep(waktu)
        print (url+str(i))
        #find article link
        req = requests.get(url+str(i),headers = headers)
        soup = BeautifulSoup(req.text, "lxml")
        news_links = soup.find_all("div",{'class':'article__list clearfix'})
        print('found: ', len(news_links))
        try:
            #looping through article link
            for idx,news in enumerate(news_links):
                time.sleep(waktu)
                print('\nscraping: ', idx+1,'/',len(news_links))
                news_dict = {}

                #find news title
                title_news= news.find('a',{'class':'article__link'}).text 
                print(title_news)

                #find urll news
                url_news = news.find('a',{'class':'article__link'}).get('href')
                print(url_news)
                
                #find news content in url
                req_news =  requests.get(url_news)
                soup_news = BeautifulSoup(req_news.content, "lxml")

                #find news content 
                news_content = soup_news.find("div",{'class':'read__content'})
                image_content = soup_news.find('div',{'class':"photo"})
                image_content=image_content.img['src']
                #find paragraph in news content 
                p = news_content.find_all('p')
                content = ' '.join(item .text for item in p)
                news_content = content

                #wrap in dictionary 
                news_dict['id']=[i,idx]
                news_dict['date']=date
                news_dict['title'] = title_news
                news_dict['content'] = news_content
                news_dict['images'] = image_content
                news_dict['url'] = url_news
                result.append(news_dict)
            
            return result
        except BaseException as e :
            logger.error(e, exc_info=True)
            print('\n\n\n\n\ngagal ambil')
       """ 
#testing
def test_kompas(): 
    pprint(crawl_kompas(date='2019-01-21'))
test_kompas()
 """

def crawl_bisnis(url='https://www.bisnis.com/', date='07+January+2019'):
     # prepare headers


    url = url+date
    result = []
    req = requests.get(url, headers=headers)
    soup = BeautifulSoup(req.text, "lxml")

    #find article link
    news_links = soup.find_all("li",{'class':'row mb-30'})
    print('found ', len(news_links), 'links')
    for idx, news in enumerate(news_links):
        time.sleep(random.randint(1,10))
        news_dict={}

        title = news.find('div',{'class':'title'}).text
        news_url = news.find('a',{'class':'c-222'}).get('href')
        print(idx+1,'/',len(news_links))


        #news content
        req_news = requests.get(news_url)
        soup_news = BeautifulSoup(req_news.text,'lxml')
        news_content = soup_news.find('div',{'class':'col-sm-10'})

        #find paragraph 
        p = news_content.find_all('p')
        content = ' '.join(item .text for item in p)
        news_content = content

        #wrap in dictionary
        news_dict['id']=idx
        news_dict['url'] = news_url
        news_dict['title'] = title
        news_dict['content'] = news_content
        result.append(news_dict)


    return result
crawl_bisnis()
# kontan 
def crawl_kontan(url, run_headless=True):
    def scrollDown(browser, numberOfScrollDowns):
        body = browser.find_element_by_tag_name("body")
        while numberOfScrollDowns >=0:
            time.sleep(1)
            body.send_keys(Keys.END)
            numberOfScrollDowns -= 1
        return browser

    def correct_url(url): 
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
        return url

    def check_insight(url):
        if "insight" not in url:
            return True
        else:
            print('found insight')
            return False
    
    result = []
    url = correct_url(url)
    browser = webdriver.Firefox()
    browser.set_window_size(1280,720)
    browser.get(url)
    browser = scrollDown(browser, 10)
    """ innerHTML = browser.execute_script("return document.body.outerHTML") #returns the inner HTML as a string
    print(innerHTML) """
    body = browser.find_element_by_tag_name("body")
    bodyText = body.get_attribute("outerHTML")
    soup=BeautifulSoup(bodyText,"lxml")
    news_links = soup.find_all("h1")
    print(len(news_links))
    for index, news in enumerate(news_links):
        news_dict={}
        title_news = news.find('a').content
        url_news = news.find('a').get('href')
        url_news = 'http:'+url_news
        if check_insight(url_news):
            print(url_news)
            req_news = requests.get(url_news)
        else:
            print("\n")
            print("\n","---PREMIUM PAGE DETECTED---","\n")
            print("\n","\n","\n","\n","\n","\n","\n","\n","\n","\n","\n")
        soup_news = BeautifulSoup(req_news.content,"html.parser")
        print(index,"/",len(news_links), "links scraped")
        news_content = soup_news.find("div",{'itemprop':'articleBody'})
        try:
            p = news_content.find_all('p')
            content = ' '.join(item .text for item in p)
            print(type(news_content))
            print(len(news_content))
            news_content = content


            news_dict['id']=index
            news_dict['title']=title_news
            news_dict['url'] = url_news
            news_dict['content'] = news_content
            result.append(news_dict)
        except AttributeError:
            print('error', AttributeError)
            print('skipped')
            pass        
    browser.quit()
    return result