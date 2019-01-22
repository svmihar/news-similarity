from bs4 import BeautifulSoup
import requests
import time
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pprint import pprint
import csv
import logging
import pandas as pd 
logger = logging.Logger('catch_all')
headers = {'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}

def save_csv(result,name='hasil'):
    df = pd.DataFrame(result)
    df.to_csv(f'{name}.csv')

def crawl_kompas(url="https://indeks.kompas.com/ekonomi/",date='2019-01-21'):
    url = url+date+'/'
    result = []
    req = requests.get(url, headers = headers)
    soup = BeautifulSoup(req.content, "lxml")

    #looping through paging
    for i in range(1,4):
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
                news_dict['sumber']='kompas'
                news_dict['date']=date
                news_dict['title'] = title_news
                news_dict['content'] = news_content
                news_dict['images'] = image_content
                news_dict['url'] = url_news
                result.append(news_dict)
        except BaseException as e :
            logger.error(e, exc_info=True)
            print('\n\n\n\n\ngagal ambil')
    return result
""" 
#testing
def test_kompas(): 
    pprint(crawl_kompas(date='2019-01-21'))
test_kompas()
 """


def crawl_bisnis(url='https://www.bisnis.com/index', date='21+January+2019'):
    finansial='?c=5&d='
    market = '?c=194&d'
    ekonomi_bisnis = '?c=43&d='
    semua_link = [finansial,market,ekonomi_bisnis]
    kumpulan_link = []
    result = []
    for jenis in semua_link:
        kumpulan_link.append(url+jenis+date)
    for link in kumpulan_link:
        url = link
        print('scraping: '+url)
        req = requests.get(url, headers=headers)
        soup = BeautifulSoup(req.text, "lxml")

        #find article link
        news_links = soup.find_all("li",{'class':'row mb-30'})
        print('found ', len(news_links), 'links')
        for idx, news in enumerate(news_links):
            try:
                time.sleep(random.randint(1,5))
                news_dict={}
                title_news = news.find('div',{'class':'title'}).text
                url_news = news.find('a',{'class':'c-222'}).get('href')
                print(idx+1,'/',len(news_links))
                print("getting: ", url_news)
                #news content
                req_news = requests.get(url_news)
                soup_news = BeautifulSoup(req_news.text,'lxml')
                news_content = soup_news.find('div',{'class':'description'}).find_all('p')
                paragraf=''.join(item .text.strip() for item in news_content)
                image_content = soup_news.find('div',{'class':'main-image'})
                
                #save to dict
                news_dict['id']=idx
                news_dict['sumber']='bisnis'
                news_dict['date']=date
                news_dict['title'] = title_news
                news_dict['content'] = paragraf
                news_dict['images'] = image_content
                news_dict['url'] = url_news
                result.append(news_dict)

            except BaseException as e :
                logger.error(e, exc_info=True)
                print("gagal mengambil link\n\n\n\n\n\n\n")
    
    return result

def crawl_kontan(): 
    url_investasi = 'https://search.kontan.co.id/indeks?kanal=investasi&tanggal=21&bulan=01&tahun=2019&pos=indeks'
    url_keuangan = 'https://search.kontan.co.id/indeks?kanal=keuangan&tanggal=21&bulan=01&tahun=2019&pos=indeks'


    def check_insight(url):
        if "insight" not in url:
            return True
        else:
            print('found insight')
            return False
    url = [url_investasi,url_keuangan]
    hasil=[]
    for i,web in enumerate(url): 
        req = requests.get(web)
        soup = BeautifulSoup(req.text,"html.parser")
        links = soup.find_all('h1')
        for idx,link in enumerate(links): 
            news_dict={}
            link = 'https:'+link.a['href']
            if check_insight(link):
                print('scraping: ',link)
                req_news = requests.get(link)
            else:
                print("\n")
                print("\n","---PREMIUM PAGE DETECTED---","\n")
                print("\n","\n","\n","\n","\n","\n","\n","\n","\n","\n","\n")
            soup_news = BeautifulSoup(req_news.content,'lxml')
            news_content = soup_news.find("div",{'itemprop':'articleBody'})
            p = news_content.find_all('p')
            content = " ".join(item .text.strip() for item in p)
            print('paragraf: \t',content)
            image_content = soup_news.find('div',{'class':'img-detail-desk'})
            title_news = soup_news.find('h1',{"class":"detail-desk"})
            date = soup_news.find('div',{'class':" fs14 ff-opensans font-gray"})
            image_content='https:'+image_content.img['src']
            print('image: ',image_content,'\n')


        #wrap in dictionary 
            news_dict['id']=[i,idx]
            news_dict['sumber']='kontan'
            news_dict['date']=date.text
            news_dict['title'] = title_news.text
            news_dict['content'] = content
            news_dict['images'] = image_content
            news_dict['url'] = link
            hasil.append(news_dict)

    return hasil
def main():
    df = pd.DataFrame(crawl_kompas())
    df.to_csv('kompas.csv')
    # crawl_kontan()
    # df2 = pd.DataFrame(crawl_kontan())
    # df2.to_csv('kontan.csv')
    # df3=pd.DataFrame(crawl_bisnis())
    # df3.to_csv('bisnis.csv')
main()