from botocore.exceptions import NoCredentialsError
from dotenv import load_dotenv
import sys, os
sys.path.append(os.getcwd())
# from discord_bot.discord_bot import Discord

from crawling.requirements import *

load_dotenv()

AIRFLOW_CONN_ID = os.getenv("AIRFLOW_CONN_ID")
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")

date = datetime.now().strftime("%y%m%d")
# discord = Discord()


async def fetch(session, url, csv_writer):
    async with session.get(url) as response:
        html = await response.text()
        soup = bs(html, 'html.parser')
        contests = soup.select('.list_style_2 li')

        for contest in contests:
            try:
                title = contest.select_one('.title .txt').get_text(strip=True)
                category = contest.select_one(
                    '.title .category').get_text(strip=True).split("•")
                sponsor = contest.select_one('.host .icon_1').get_text(
                    strip=True).replace("주최. ", "")
                target = re.sub(r"\s", "", contest.select_one(
                    '.host .icon_2').get_text(strip=True)).replace("대상.", "").split(",")
                reception_period = re.sub(
                    r"[ㄱ-ㅣ가-힣]", "", contest.select_one('.date .step-1').get_text(strip=True)).split("~")
                evaluation_period = re.sub(
                    r"[ㄱ-ㅣ가-힣]", "", contest.select_one('.date .step-2').get_text(strip=True)).split('~')
                announcement_date = contest.select_one(
                    '.date .step-3').get_text(strip=True).replace("발표", "")
                d_day = contest.select_one('.d-day .day').get_text(strip=True)
                condition = contest.select_one(
                    '.d-day .condition').get_text(strip=True)
                link = contest.select_one('a')['href']
                link = "https://www.contestkorea.com/sub/" + link

                response_b = requests.get(link)
                soup_b = bs(response_b.text, 'html.parser')

                image_link = soup_b.select_one(
                    'div.clfx>div.img_area > div > img')['src']
                image_link = 'https://www.contestkorea.com' + image_link


                # CSV 파일에 데이터 추가
                if (condition == '접수중') | (condition == '마감임박'):
                    csv_writer.writerow([title, category, sponsor, target, reception_period[0], reception_period[1],
                                        evaluation_period[0], evaluation_period[1], announcement_date, d_day, condition, link, image_link])
                    # discord.contest_alarm(title, sponsor, category, target, reception_period[0], reception_period[1],
                    #             evaluation_period[0], evaluation_period[1], announcement_date, d_day, link, image_link)
                    
                    
            except:
                pass


def contest_crawling():

    async def main():
        # 기본 url을 바탕으로 페이지별 크롤링
        BASE_URL = 'https://www.contestkorea.com/sub/list.php?displayrow=12&int_gbn=1&Txt_sGn=1&Txt_key=all&Txt_word=&Txt_bcode=030510001&Txt_code1=&Txt_aarea=&Txt_area=&Txt_sortkey=a.int_sort&Txt_sortword=desc&Txt_host=&Txt_tipyn=&Txt_comment=&Txt_resultyn=&Txt_actcode='
        urls = [f"{BASE_URL}&page={i}" for i in range(1, 10)]

        # 파일 구분을 위한 날짜
        date = datetime.now().strftime("%Y%m%d")

        # 데이터를 저장할 폴더 생성
        try:
            os.mkdir("/opt/airflow/data")
        except FileExistsError:
            pass

        # CSV 파일 생성
        with open(f'/opt/airflow/data/contest_{date}.csv', 'w', newline='', encoding='utf-8') as file:
            csv_writer = csv.writer(file)
            # CSV 파일 헤더 작성
            csv_writer.writerow(['제목', '카테고리', '주최', '대상', '접수 시작일',
                                '접수 마감일', '심사 시작일', '심사 종료일', '발표일', 'D-Day', '상태', '링크', '이미지 링크'])

            # 비동기적으로 CSV 내용 작성
            async with aiohttp.ClientSession() as session:
                await asyncio.gather(*[fetch(session, url, csv_writer) for url in urls])

    asyncio.run(main())
