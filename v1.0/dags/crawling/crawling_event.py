import sys, os
sys.path.append(os.getcwd())
# from discord_bot.discord_bot import Discord
from crawling.requirements import *

# discord = Discord()

def event_get_urls(url):
    response = requests.get(url)
    html = response.text
    soup = bs(html, 'html.parser')
    return soup

def event_get_link(soup):
    link_list = []
    links = (soup.find_all('a', target='_blank'))
    for link in links:
        link_list.append(link.text)
        
    return link_list

def event_get_hashtag(soup):
    hashtags_all = soup.find_all('div', class_='Item_tags___ujeV')
    hashtags  = []
    for hash in hashtags_all:
        txt = hash.text.split("# ")
        hashtags.append(txt[1:])
    return hashtags

def event_get_title(soup):
    title_all = soup.find_all('span', class_='Item_item__content__title___fPQa')
    titles = []
    for title in title_all:
        titles.append(title.text)
    return titles

def event_get_host(soup):
    hosts_all = soup.find_all('div', class_='Item_host__zNXMy')
    hosts = []
    for host in hosts_all:
        hosts.append(host.text)
    return hosts

def event_get_date(soup):
    dates_all = soup.find_all('div', class_='Item_date__kVMJZ')
    dates = []
    for date in dates_all:
        txt = re.sub(r"\s", "", date.text)
        txt = re.sub(r"\(.\)", "", txt)
        dates.append(txt.split("~"))
    return dates

def event_get_image(soup):
    images_all = soup.find_all('img', alt="/default/event_img.png")
    images = []
    for i, image in enumerate(images_all):
        if i % 2 == 1:
            text = 'https://dev-event.vercel.app'
            text += image.get('src')
            images.append(text)
    return images

def event_get_link(soup):
    link_all = soup.find_all('div', class_='Item_item__86e_I')
    links = []
    for link in link_all:
        txt = link.a.attrs["href"]
        links.append(txt)
    return links


def event_get_data():
    url = 'https://dev-event.vercel.app/events'
    soup = event_get_urls(url)
    titles = event_get_title(soup) # 제목
    hashtags = event_get_hashtag(soup) # 해시태그
    hosts = event_get_host(soup) # 주최자
    dates = event_get_date(soup) # 일시[시작일, 종료일,]
    images = event_get_image(soup) # 이미지
    links = event_get_link(soup) # 주최 링크

    start_dates = [start_end[0] for start_end in dates] #시작 날짜
    end_dates = [start_end[1] for start_end in dates] # 끝나는 날짜

    # discord.event_alarm(titles, hosts, hashtags, start_dates, end_dates, links, images)

    
    # dataframe으로 변환
    dev_df = pd.DataFrame({'title' : titles, 'host' : hosts, 'hashtag': hashtags, 'start_date' : start_dates, 'end_date' : end_dates, 'image' : images, 'link' : links})
    date = datetime.now().strftime("%Y%m%d")
    # csv 파일로 저장
    dev_df.to_csv(f"/opt/airflow/data/event_{date}.csv", index=False)
    
