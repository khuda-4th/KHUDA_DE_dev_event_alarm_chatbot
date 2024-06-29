import pandas as pd
import json
from datetime import datetime

def makeCarouselCard(title, desc, image_url, web_url, ment):
    card = {
        "title": title,
        "description": desc,
        "thumbnail": {
            "imageUrl": image_url
        },
        "buttons": [
            {
                "action": "webLink",
                "label": f"{ment}로 이동",
                "webLinkUrl": web_url
            },
        ]
    }
    return card


def make_devcard():
    dev_list = []
    date = datetime.now().strftime("%Y%m%d")
    dev_df = pd.read_csv(f'../data/event_{date}.csv',encoding='utf-8')
    today = datetime.today().strftime("%Y.%m.%d")
    cur_df = dev_df[dev_df['end_date'] >= today]
    cur_df = cur_df.head(10) #일단 10개만 뽑아보자
    for _, row in cur_df.iterrows():
        title = row['title']
        host = row['host']
        start_date = row['start_date']
        end_date = row['end_date']
        image = row['image']
        link = row['link']
        desc = f"주최사 : {host} \n 일시 : {start_date} ~ {end_date}"
        basic_card = makeCarouselCard(title, desc, image_url = image, web_url = link, ment="주최사이트")
        dev_list.append(basic_card)

    return dev_list

def make_velogcard():
    velog_list = [] 
    date = datetime.now().strftime("%Y%m%d")
    velog_df = pd.read_csv(f'../data/velog_{date}.csv', encoding='utf-8')
    velog_df = velog_df.head(10)
    for _, row in velog_df.iterrows():
        title = row['title']
        host = row['writer']
        image = row['img']
        link = row['link']
        desc = f"작성자 : {host}"
        basic_card = makeCarouselCard(title, desc, image_url = image, web_url = link, ment="Velog")
        velog_list.append(basic_card)

    return velog_list

def make_eventcard():
    event_list =[]
    date = datetime.now().strftime("%Y%m%d")
    event_df = pd.read_csv(f'../data/contest_{date}.csv', encoding='utf-8')
    event_df = event_df.head(10)
    for _, row in event_df.iterrows():
        title = row['제목']
        host = row['주최']
        category = row['카테고리']
        start_date = row['접수 시작일']
        end_date = row['접수 마감일']
        image = row['이미지 링크']
        link = row['링크']
        desc = f"주최사 : {host} \n 접수기간 : {start_date} ~ {end_date} \n  카테고리 : {category}"
        basic_card = makeCarouselCard(title = title, desc = desc, image_url = image, web_url = link, ment="공모전 사이트")
        event_list.append(basic_card)

    return event_list


