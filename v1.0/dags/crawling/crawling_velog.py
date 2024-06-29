import sys,os
sys.path.append(os.getcwd())

from crawling.requirements import *
# from discord_bot.discord_bot import Discord

# discord = Discord()

# selenium으로 velog 메인 페이지에서 트렌딩 글들 링크만 가져오기 (beautilfulSoup으로 하니까 못 찾아서)
def velog_get_url(**kwargs) : 
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    browser = webdriver.Chrome(options = chrome_options)
    browser.get("https://velog.io/trending/day")
    time.sleep(5)
    url_list = browser.find_elements(By.CLASS_NAME, 'VLink_block__Uwj4P.PostCard_styleLink__nc1Hy')
    result = []
    for url in url_list :
        link = url.get_attribute('href')
        result.append(link)
        print(link)
    result = list(set(result))
    kwargs['task_instance'].xcom_push(key='url_list', value = result)
    return "end get url list"

# beautifulSoup으로 각 블로그 글 접속
def open_page(url) :
    req=requests.get(url)
    if req.status_code == requests.codes.ok:
        req = req.text
        page=bs(req,"html.parser")
        return page
    else: return -1

# beautifulSoup으로 접속한 블로그 정보 가져오기
def velog_get_title(page) :
    title = page.find('div', {'class':'head-wrapper'})
    title = title.find('h1').get_text()
    return title

def velog_get_writer(page) :
    writer = page.find('a',{'class' : 'user-logo'}).get_text()
    return writer

def velog_get_thumnail(page) :
    img_all = page.find_all('img')
    img_src = img_all[0].get('src')
    return img_src

def velog_get_text(page) :
    text_all = page.find_all(['p','h1','h2','h3','li'])
    text=""
    for t in text_all :
        text += t.text
    return text
    
def velog_get_user_link(page):
    links_all = page.find("a", {"class": "sc-egiyK cyyZlI"})
    user_link = links_all.get("href")
    return user_link
    
def velog_get_user_thumbnail(page):
    user_info = page.find("img", {"alt": "profile"})
    user_thumbnail = user_info.get("src")
    return user_thumbnail
    
def velog_get_info(**kwargs) :
    url_list = kwargs['task_instance'].xcom_pull(key = 'url_list')
    title, writer, img, text, link, user_link, user_thumbnail = [], [], [], [], [], [], []
    for l in url_list :
        page = open_page(l)
        time.sleep(1)
        if page != -1:
            try:
                title_ = velog_get_title(page)
                writer_ = velog_get_writer(page)
                img_ = velog_get_thumbnail(page)
                text_ = velog_get_text(page)
                user_link_ = velog_get_user_link(page)
                user_thumbnail_ = velog_get_user_thumbnail(page)
            except:
                continue

            link.append(l)
            title.append( title_ )
            writer.append( writer_ )
            img.append( img_ )
            text.append( text_ )
            user_link.append( user_link_ )
            user_thumbnail.append( user_thumbnail_ )

    data = pd.DataFrame({'title' : title, 'writer' : writer, 'img' : img, 'text' : text, 'link' : link, "user_link": user_link, "user_thumbnail": user_thumbnail})
    date = datetime.now().strftime("%Y%m%d")
    data.to_csv(f"/opt/airflow/data/velog_{date}.csv", index=False)
    kwargs['task_instance'].xcom_push(key = f'velog_csv', value= f"/opt/airflow/data/velog_{date}.csv")
    # discord.velog_alarm(title, writer, link, user_thumbnail, user_link, img)
    


