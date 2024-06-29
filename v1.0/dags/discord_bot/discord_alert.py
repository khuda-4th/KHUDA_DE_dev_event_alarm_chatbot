import sys,os
sys.path.append(os.getcwd())

from crawling.requirements import *
from discord_bot.discord_bot import Discord

def discord_alert():

    discord = Discord()

    date = datetime.today().strftime('%Y%m%d')
    date_y = (datetime.today() - timedelta(1)).strftime("%Y%m%d")

    event_file = f"/opt/airflow/data/event_{date}.csv"
    contest_file = f"/opt/airflow/data/contest_{date}.csv"
    #velog_file = f"/opt/airflow/data/velog_{date}.csv"

    event_file_y = f"/opt/airflow/data/event_{date_y}.csv"
    contest_file_y = f"/opt/airflow/data/contest_{date_y}.csv"
    #velog_file_y = f"/opt/airflow/data/velog_{date_y}.csv"

    event = pd.read_csv(event_file, encoding='UTF-8')
    contest = pd.read_csv(contest_file, encoding='UTF-8')
    #velog = pd.read_csv(velog_file, encoding='UTF-8')
    
    flag = False

    try:
        event_y = pd.read_csv(event_file_y, encoding='UTF-8')
        contest_y = pd.read_csv(contest_file_y, encoding='UTF-8')
        #velog_y = pd.read_csv(velog_file_y, encoding='UTF-8')
                

        event_total = pd.concat([event, event_y])
        contest_total = pd.concat([contest, contest_y])
        #velog_total = pd.concat([velog, velog_y])
        
        event_dropped = event_total.drop_duplicates(['title'], keep=False, ignore_index=True)
        contest_dropped = contest_total.drop_duplicates(['제목'], keep=False, ignore_index=True)
        #velog_dropped = velog_total.drop_duplicates(['title'], keep=False, ignore_index=True)
        

        flag = True

    except:
        flag = False

    print(f"flag: {flag}")
    if flag:
        # 중복 제거된 내역만 출력
        discord.event_alarm(event_dropped['title'], event_dropped['host'], event_dropped['hashtag'], event_dropped['start_date'],
                                event_dropped['end_date'], event_dropped['link'], event_dropped['image'])
        for _, row in contest_dropped.iterrows(): 
            discord.contest_alarm(row['제목'], row['주최'], row['카테고리'], row['대상'], row['접수 시작일'], row['접수 마감일'],
                                row['심사 시작일'], row['심사 종료일'], row['발표일'], row['D-Day'], row['링크'], row['이미지 링크'])
        #discord.velog_alarm(velog_dropped['title'], velog_dropped['writer'], velog_dropped['link'], velog_dropped['user_thumbnail'], velog_dropped['user_link'], velog_dropped['img'])

    else:
        discord.event_alarm(event['title'], event['host'], event['hashtag'], event['start_date'],
                                event['end_date'], event['link'], event['image'])
        for _, row in contest.iterrows():
            discord.contest_alarm(row['제목'], row['주최'], row['카테고리'], row['대상'], 
                    row['접수 시작일'], row['접수 마감일'],
                                row['심사 시작일'], row['심사 종료일'], row['발표일'], row['D-Day'], row['링크'], row['이미지 링크'])
        #discord.velog_alarm(velog['title'], velog['writer'], velog['link'], velog['user_thumbnail'], velog['user_link'], velog['img'])
