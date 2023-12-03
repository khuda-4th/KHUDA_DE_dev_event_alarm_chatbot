import requests
from bs4 import BeautifulSoup
import csv

def crawl_csv(pages):
    # csv 파일 쓰기 모드
    csv_file_path = '/home/ubuntu/airflow/contest_crawling.csv'
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        # csv writer 생성
        csv_writer = csv.writer(csvfile)
        
        # column 작성
        csv_writer.writerow(["제목", "카테고리", "주최", "대상", "접수 기간", "심사 기간", "발표일", "D-day", "상태", "이미지 링크"])

        for page in pages:
            url = f"https://www.contestkorea.com/sub/list.php?displayrow=12&int_gbn=1&Txt_sGn=1&Txt_key=all&Txt_word=&Txt_bcode=030510001&Txt_code1=&Txt_aarea=&Txt_area=&Txt_sortkey=a.int_sort&Txt_sortword=desc&Txt_host=&Txt_tipyn=&Txt_comment=&Txt_resultyn=&Txt_actcode=&page={page}"

            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            contests = soup.select('.list_style_2 li')

            for contest in contests:
                try:
                    title = contest.select_one('.title .txt').get_text(strip=True)
                    category = contest.select_one('.title .category').get_text(strip=True)
                    sponsor = contest.select_one('.host .icon_1').get_text(strip=True)
                    target = contest.select_one('.host .icon_2').get_text(strip=True)
                    reception_period = contest.select_one('.date .step-1').get_text(strip=True)
                    evaluation_period = contest.select_one('.date .step-2').get_text(strip=True)
                    announcement_date = contest.select_one('.date .step-3').get_text(strip=True)
                    d_day = contest.select_one('.d-day .day').get_text(strip=True)
                    condition = contest.select_one('.d-day .condition').get_text(strip=True)
                    link = contest.select_one('a')['href']
                    link = "https://www.contestkorea.com/sub/" + link

                    response_b = requests.get(link)
                    soup_b = BeautifulSoup(response_b.text, 'html.parser')

                    image_link = soup_b.select_one('div.clfx>div.img_area > div > img')['src']
                    image_link = 'https://www.contestkorea.com' + image_link

                    # 한 행씩 csv 파일에 추가
                    csv_writer.writerow([title, category, sponsor, target, reception_period, evaluation_period, announcement_date, d_day, condition, image_link])
                except:
                    pass