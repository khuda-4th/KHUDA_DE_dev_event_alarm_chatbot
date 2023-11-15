import pandas as pd
import time,os,requests
import warnings
from selenium import webdriver
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
warnings.filterwarnings(action="ignore")

# selenium으로 velog 메인 페이지에서 트렌딩 글들 링크만 가져오기 (beautilfulSoup으로 하니까 못 찾아서)
'''
def get_url_list() : 
    browser = webdriver.Chrome('crawling/chromedriver') # chrome version 119.0.6045.105 (이것보다 높으면 안 됨)
    browser.get("https://velog.io/")
    url_list = browser.find_elements(By.CLASS_NAME, 'VLink_block__Uwj4P.PostCard_styleLink__DYahQ')
    result = []
    for url in url_list :
        result.append(url.get_attribute('href'))
    return result
'''
def get_url_list() :
    page = open_page("https://velog.io/trending/week")
    url_list = page.find_all('div',{'class' : 'PostCard_block__t_0t8'})
    print(url_list)

# beautifulSoup으로 각 블로그 글들 정보 가져오기
def open_page(url) :
    req=requests.get(url).text
    page=bs(req,"html.parser")
    return page

def get_title(page) :
    title = page.find('div', {'class':'head-wrapper'})
    title = title.find('h1').text
    return title

def get_user(page) :
    user = page.find('a',{'class' : 'user-logo'}).text
    return user

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
    
def main() :
    url_list = get_url_list()
    for l in url_list :
        page = open_page(l)
        title = get_title(page)
        print(title)
        user = get_user(page)
        print(user)
        img = get_thumnail(page)
        text = get_text(page)

if __name__ == "__main__" :
    main()