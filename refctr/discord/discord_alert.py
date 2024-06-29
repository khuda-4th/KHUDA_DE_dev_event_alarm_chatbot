import sys, os, time
from datetime import datetime, timedelta
import pandas as pd
import concurrent.futures
sys.path.append(os.getcwd())


# from crawling.requirements import *
from discord_bot import EventNotifier, ContestNotifier, TrendNotifier

TODAY = datetime.today().strftime('%y%m%d')
YSTRDAY = (datetime.today() - timedelta(1)).strftime("%y%m%d") 

def send_event(eNotifier, event):
    # print(f"event['title']: {event['title']}, event['url']: {event['url']}, event['img_url']: {event['img_url']}, event['host']: {event['host']}, event['period']: {event['period']}, event['tags']: {event['tags']}")
    eNotifier.send_event_alarm(event['title'], event['url'], event['img_url'], \
        event['host'], event['period'], event['tags'])
    return "event alarm sent"
    
def send_contest(cNotifier, contest):
    # print(f"contest['title']: {contest['title']}, contest['url']: {contest['url']}, contest['img_url']: {contest['img_url']}, contest['status']: {contest['status']}, contest['category']: {contest['category']}, contest['target']: {contest['target']} \
    #           contest['host']: {contest['host']}, contest['sponsor']: {contest['sponsor']}, contest['period']: {contest['period']}, contest['d-day']: {contest['d-day']}, contest['total_prize']: {contest['total_prize']}, contest['first_prize']: {contest['first_prize']}")
    cNotifier.send_contest_alarm(contest['title'], contest['url'], contest['img_url'], \
        contest['status'], contest['category'], contest['target'], contest['host'], \
        contest['sponsor'], contest['period'], contest['d-day'], contest['total_prize'], \
        contest['first_prize'])
    return "contest alarm sent"

def send_trend(tNotifier, trend):
    # title,user,img,url,user_url,user_img
    tNotifier.send_trend_alarm(trend['title'], trend['user'], trend['img'], \
                               trend['url'], trend['user_url'], trend['user_img'])

def extract_valid_data():
    """ REAL PATH """
    # event_file = f"/opt/airflow/data/event_{TODAY}.csv"
    # contest_file = f"/opt/airflow/data/contest_{TODAY}.csv"
    # velog_file = f"/opt/airflow/data/velog_{TODAY}.csv"

    # event_file_y = f"/opt/airflow/data/event_{YSTRDAY}.csv"
    # contest_file_y = f"/opt/airflow/data/contest_{YSTRDAY}.csv"
    # velog_file_y = f"/opt/airflow/data/velog_{YSTRDAY}.csv"

    """ TEST PATH """
    event_file = f"./data/event_{TODAY}.csv"
    contest_file = f"./data/contest_{TODAY}.csv"
    trend_file = f"./data/trend_{TODAY}.csv"

    event_file_y = f"./data/event_{YSTRDAY}.csv"
    contest_file_y = f"./data/contest_{YSTRDAY}.csv"
    trend_file_y = f"./data/trend_{YSTRDAY}.csv"

    event_today = pd.read_csv(event_file, encoding='UTF-8')
    contest_today = pd.read_csv(contest_file, encoding='UTF-8')
    trend_today = pd.read_csv(trend_file, encoding='UTF-8')

    # event 어제 날짜 파일이 존재할 경우
    if os.path.exists(event_file_y):
        event_ystrday = pd.read_csv(event_file_y, encoding='UTF-8')
        event_diff = pd.concat([event_today, event_ystrday]).drop_duplicates(keep=False, ignore_index=True)
    else:
        event_diff = event_today
    
    # contest 어제 날짜 파일이 존재할 경우
    if os.path.exists(contest_file_y):
        contest_ystrday = pd.read_csv(contest_file_y, encoding='UTF-8')
        contest_diff = pd.concat([contest_today, contest_ystrday]).drop_duplicates(keep=False, ignore_index=True)
    else:
        contest_diff = contest_today
    
    # velog 어제 날짜 파일이 존재할 경우
    if os.path.exists(trend_file_y):
        trend_ystrday = pd.read_csv(trend_file_y)
        trend_diff = pd.concat([trend_today, trend_ystrday]).drop_duplicates(keep=False, ignore_index=True)
    else:
        trend_diff = trend_today

    return event_diff, contest_diff, trend_diff

### main ###
def discord_alert():
    eNotifier = EventNotifier('{event_discord_channel_webhook}')
    cNotifier = ContestNotifier('{contest_discord_channel_webhook}')
    tNotifier = TrendNotifier('{trend_discord_channel_webhook}')
  
    event, contest, trend = extract_valid_data()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        futures.append(executor.submit(send_event, eNotifier, event))
        futures.append(executor.submit(send_contest, cNotifier, contest))
        futures.append(executor.submit(send_trend, tNotifier, trend))
        
        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                print(result)
            except Exception as e:
                print(f"An error occured: {e}")

discord_alert()
