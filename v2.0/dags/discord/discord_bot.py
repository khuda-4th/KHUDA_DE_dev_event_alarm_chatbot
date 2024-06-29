import requests
import json
from datetime import datetime

class DiscordNotifier:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url
        self.headers = {"Content-Type": "application/json"}

    def send_message(self, data):
        response = requests.post(self.webhook_url, data=json.dumps(data), headers=self.headers)
        print(f"Discord response: {response.status_code} - {response.text}")

    def format_common_fields(self, username, content):
        return {
            "username": username,
            "avatar_url": "",
            "content": content
        }

class EventNotifier(DiscordNotifier):
    def __init__(self, webhook_url):
        super().__init__(webhook_url)

    def send_event_alarm(self, titles, urls, img_urls, hosts, periods, tags):
        for title, url, img_url, host, period, tag in zip(titles, urls, img_urls, hosts, periods, tags):
            data = self.format_common_fields(
                username="AirDnB",
                content="🤖 " + datetime.today().strftime('%Y%m%d') + "일자 **개발 행사 안내드립니다!** 🤖"
            )
            data["embeds"] = [
                {
                    "author": {"name": host}if host else {},
                    "title": title,
                    "url": url,
                    "color": 15258703,
                    "fields": [
                        {"name": "기간", "value": period, "inline": True},
                        {"name": "관련 해시태그", "value": tag, "inline": True},
                    ],
                    "image": {"url": img_url} if img_url else {},
                }
            ]
            # print(f"event data: {data}")
            self.send_message(data)

class ContestNotifier(DiscordNotifier):
    def __init__(self, webhook_url):
        super().__init__(webhook_url)

    def send_contest_alarm(self, titles, urls, img_urls, statuss, categorys, targets, hosts, sponsors, periods, ddays, total_prizes, first_prizes):
        for title, url, img_url, status, category, target, host, sponsor, period, dday, total_prize, first_prize \
                    in zip(titles, urls, img_urls, statuss, categorys, targets, hosts, sponsors, periods, ddays, total_prizes, first_prizes):
            total_prize = str(total_prize)
            first_prize = str(first_prize).strip("\"")
            category = category.strip("\"")

            data = self.format_common_fields(
                username="AirDnB",
                content="🏆 " + datetime.today().strftime('%Y%m%d') + "일자 **개발 대회 안내드립니다!** 🏆"
            )
            data["embeds"] = [
                {
                    "author": {"name": host} if host else {},
                    "title": title,
                    "url": url,
                    "color": 10038562,
                    "fields": [
                        {"name": "카테고리", "value": category, "inline": True},
                        {"name": "대상", "value": target, "inline": True},
                        {"name": "접수 기간", "value": period},
                        {"name": "후원", "value": sponsor,},
                        {"name": "총 상금", "value": total_prize, "inline": True},
                        {"name": "1등 상금", "value": first_prize, "inline": True},
                        {"name": "D-Day", "value": dday},
                    ],
                    "image": {"url": img_url},
                }
            ]
            print(f"contest data: {data}")
            self.send_message(data)

class TrendNotifier(DiscordNotifier):
    def __init__(self, webhook_url):
        super().__init__(webhook_url)

    # title,user,img,url,user_url,user_img
    def send_trend_alarm(self, titles, users, imgs, urls, user_urls, user_imgs):
        for title, user, img, url, user_url, user_img in zip(titles, users, imgs, urls, user_urls, user_imgs):
            req = requests.get(url)
            if req.status_code == requests.codes.ok:
                data = self.format_common_fields(
                    username="AirDnB",
                    content="💡 " + datetime.today().strftime('%Y%m%d') + "일자 **개발 트렌드 안내드립니다!** 💡"
                )
                data["embeds"] = [
                    {
                        "author": {
                            "name": user,
                            "url": user_url,
                            "icon_url": user_img
                        },
                        "title": title,
                        "url": url,
                        "color": 2899536,
                        "image": {"url": img},
                    }
                ]
                self.send_message(data)


