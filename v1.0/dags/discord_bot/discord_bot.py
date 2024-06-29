from crawling.requirements import *

class Discord():
    def __init__(self):
        self.webhook_url = 'https://discord.com/api/webhooks/1206985842304880660/LYOwypDX-GZx3OgNPcVk4z62RiyOoauYx27bDzPwElBqhHP5VsEyKGENuk4EVAE8KB_E'
        self.headers = { "Content-Type": "application/json" }

    def event_alarm(self, titles, hosts, hashtags, startd, endd, links, image):
        for t, h, hasht, sd, ed, l, img in zip(titles, hosts, hashtags, startd, endd, links, image):
            hasht = re.sub('[^A-Za-z0-9가-힣\s]', '', hasht)
            hasht = hasht.split(" ")
            data = {
                        "username": "AirDnB",
                        "avatar_url": "https://private-user-images.githubusercontent.com/64704608/287463972-30a4b397-cc10-4505-a46d-60fb7eb32219.jpeg?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MDQyMDUzNTAsIm5iZiI6MTcwNDIwNTA1MCwicGF0aCI6Ii82NDcwNDYwOC8yODc0NjM5NzItMzBhNGIzOTctY2MxMC00NTA1LWE0NmQtNjBmYjdlYjMyMjE5LmpwZWc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjQwMTAyJTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI0MDEwMlQxNDE3MzBaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT05Njc3MjRlNzkwNmIzNDM5ZWM5M2Y2M2VjNDM3MTUwNTExMzY0YjlkODlkY2M0YmUwY2RkNzk5NzE0NGY4MTdiJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCZhY3Rvcl9pZD0wJmtleV9pZD0wJnJlcG9faWQ9MCJ9.p6gWiW1iF4A67nvZIVKhNn3NyIbpUUNG_J9RSeOb8IA",
                        "content": "🔔 " + datetime.today().strftime('%Y%m%d') +  "일자 **개발 행사 속보입니다!!!**",
                        "embeds": [
                        {
                            "author": {
                                "name": h
                            },
                            "title": t,
                            "url": l,
                            "color": 15258703,
                            "fields": [
                            {
                                "name": "시작일",
                                "value": sd,
                                "inline": True
                            },
                            {
                                "name": "종료일",
                                "value": ed,
                                "inline": True
                            },
                            {
                                "name": "관련 해시태그",
                                "value": ", ".join(hasht)
                            },
                            ],
                            "image": {
                                "url": img
                            },
                        }
                        ]
                    }
            
            response = requests.post(self.webhook_url, data=json.dumps(data), headers=self.headers)
            print(f"discord response event : {response}")



    def contest_alarm(self, title, host, category, target, startd, endd, estartd, eendd, ad, dday, link, img):
        category = re.sub('[^A-Za-z0-9가-힣\s]', '', category)
        category = category.split(" ")
        target = re.sub('[^A-Za-z0-9가-힣\s]', '', target)
        target = target.split(" ")
        startd, endd, estartd, eendd, ad = str(startd), str(endd), str(estartd), str(eendd), str(ad)
        data = {
                
                    "username": "AirDnB",
                    "avatar_url": "https://private-user-images.githubusercontent.com/64704608/287463972-30a4b397-cc10-4505-a46d-60fb7eb32219.jpeg?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MDQyMDUzNTAsIm5iZiI6MTcwNDIwNTA1MCwicGF0aCI6Ii82NDcwNDYwOC8yODc0NjM5NzItMzBhNGIzOTctY2MxMC00NTA1LWE0NmQtNjBmYjdlYjMyMjE5LmpwZWc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjQwMTAyJTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI0MDEwMlQxNDE3MzBaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT05Njc3MjRlNzkwNmIzNDM5ZWM5M2Y2M2VjNDM3MTUwNTExMzY0YjlkODlkY2M0YmUwY2RkNzk5NzE0NGY4MTdiJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCZhY3Rvcl9pZD0wJmtleV9pZD0wJnJlcG9faWQ9MCJ9.p6gWiW1iF4A67nvZIVKhNn3NyIbpUUNG_J9RSeOb8IA",
                    "content": "📣 " + datetime.today().strftime('%Y%m%d') + "일자 **개발 대회 속보입니다!!!**",
                    "embeds": [
                    {
                        "author": {
                            "name": host,
                        },
                        "title": title,
                        "url": link,
                        "color": 10038562,
                        "fields": [
                        {
                            "name": "카테고리",
                            "value": ", ".join(category),
                            "inline": True
                        },
                        {
                            "name": "대상",
                            "value": ", ".join(target),
                            "inline": True
                        },
                        {
                            "name": chr(10),
                            "value": chr(10)
                        },

                         {
                             "name": "접수 시작일",
                             "value": startd,
                             "inline": True,
                         },
                         {
                             "name": "접수 종료일",
                             "value": endd,
                              "inline": True,
                         },
                         {
                             "name": chr(10),
                             "value": chr(10)
                         },
                         {
                             "name": "심사 시작일",
                             "value": estartd,
                             "inline": True,
                         },
                         {
                             "name": "심사 종료일",
                             "value": eendd,
                             "inline": True,
                         },
                         {
                             "name": chr(10),
                             "value": chr(10)
                         },
                         {
                             "name": "발표일",
                             "value": ad,
                             "inline": True
                           
                         },
                         {
                             "name": "D-Day",
                             "value": dday,
                             "inline": True
                         },
                        ],
                        "image": {
                            "url": img,
                        },
                    }
                    ]
                }
        
        response = requests.post(self.webhook_url, data=json.dumps(data), headers=self.headers)
        print(f"discord response contest : {response}")
    
    def velog_alarm(self, titles, writers, links, user_thumbnail, user_link, img):
        for t, w, l, uthm, userl, image in zip(titles, writers, links, user_thumbnail, user_link, img):
            req = requests.get(l)
            if req.status_code == requests.codes.ok:
                data = {
                            "username": "AirDnB",
                            "avatar_url": "https://private-user-images.githubusercontent.com/64704608/287463972-30a4b397-cc10-4505-a46d-60fb7eb32219.jpeg?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTEiLCJleHAiOjE3MDM2NzMyOTMsIm5iZiI6MTcwMzY3Mjk5MywicGF0aCI6Ii82NDcwNDYwOC8yODc0NjM5NzItMzBhNGIzOTctY2MxMC00NTA1LWE0NmQtNjBmYjdlYjMyMjE5LmpwZWc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBSVdOSllBWDRDU1ZFSDUzQSUyRjIwMjMxMjI3JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDIzMTIyN1QxMDI5NTNaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT05M2RjNmQ1OTI3ODNlNzY0OTExOTY1NTE0NWQwZjk5YThhN2U3MDc1ZDlhMmUzNmUyZTE0ZWYyNTg3OWViZTkwJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCZhY3Rvcl9pZD0wJmtleV9pZD0wJnJlcG9faWQ9MCJ9.R16PV8RaTELsWntHgnv988dKi6nh41d34-LAaVsGpGo",
                            "content": "📢 " + datetime.today().strftime('%Y%m%d') + "일자 **개발 트렌드 속보입니다!!!**",
                            "embeds": [
                                {
                                "author": {
                                    "name": w,
                                    "url": userl,
                                    "icon_url": uthm
                                },
                                "title": t,
                                "url": l,
                                "color": 2899536,
                                "image": {
                                    "url": image
                                },
                            }
                            ]
                        }
            
                response = requests.post(self.webhook_url, data=json.dumps(data), headers=self.headers)
                print(f"discord response velog : {response}")
        

