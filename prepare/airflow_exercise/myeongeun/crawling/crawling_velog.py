import pandas as pd
import time,os,requests
import warnings
import datetime
from selenium import webdriver
from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.by import By
warnings.filterwarnings(action="ignore")

# selenium으로 velog 메인 페이지에서 트렌딩 글들 링크만 가져오기 (beautilfulSoup으로 하니까 못 찾아서)
def get_url_list(**kwargs) : 
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    browser = webdriver.Chrome(options = chrome_options)
    browser.get("https://velog.io/")
    time.sleep(5)
    url_list = browser.find_elements(By.CLASS_NAME, 'VLink_block__Uwj4P.PostCard_styleLink__DYahQ')
    result = []
    for url in url_list :
        link = url.get_attribute('href')
        print(f"######{link}######")
        result.append(link)
    result = list(set(result))
    kwargs['task_instance'].xcom_push(key='url_list', value = result)
    return "end get url list"

# beautifulSoup으로 각 블로그 글 접속
def open_page(url) :
    req=requests.get(url).text
    page=bs(req,"html.parser")
    return page

# beautifulSoup으로 접속한 블로그 정보 가져오기
def get_title(page) :
    title = page.find('div', {'class':'head-wrapper'})
    title = title.find('h1').text
    return title

def get_writer(page) :
    writer = page.find('a',{'class' : 'user-logo'}).text
    return writer

def get_thumnail(page) :
    img_all = page.find_all('img')
    img_src = img_all[0].get('src')
    return img_src

def get_text(page) :
    text_all = page.find_all(['p','h1','h2','h3','li'])
    text=""
    for t in text_all :
        text += t.text
    return text
    
def crawling(**kwargs) :
    url_list = kwargs['task_instance'].xcom_pull(key = 'url_list')
    title, writer, img, text, link = [], [], [], [], []
    for l in url_list :
        link.append(l)
        page = open_page(l)
        time.sleep(1)
        title.append( get_title(page) )
        writer.append( get_writer(page) )
        img.append( get_thumnail(page) )
        text.append( get_text(page) )
        print(title)
    data = pd.DataFrame({'title' : title, 'writer' : writer, 'img' : img, 'text' : text, 'link' : link})
    date = datetime.datetime.now().strftime("%Y%m%d")
    data.to_csv(f"/home/ubuntu/airflow/airflow/data/velog_{date}.csv", index=False)
    kwargs['task_instance'].xcom_push(key = f'velog_csv', value= f"/home/ubuntu/airflow/airflow/data/velog_{date}.csv")
    kwargs['task_instance'].xcom_push(key='result_msg', value= f"total number of blogs this week : {len(data)}")
