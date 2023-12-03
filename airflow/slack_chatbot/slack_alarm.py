from slack_sdk import WebClient
from datetime import datetime

class SlackAlarm:
    def __init__(self, channel, token):
        self.channel = channel
        self.client = WebClient(token=token)

    def event_alarm(self, titles, hosts, hashtags, startd, endd, links):
        for t, h, hasht, sd, ed, l in zip(titles, hosts, hashtags, startd, endd, links):
            text = '\n\n     🔔 *개발 행사 속보입니다!!!*'
            text += "\n✔️ 제목: " + t
            text += "\n✔️ 해시태그: " + ", ".join(hasht)
            text += '\n✔️ 주최: ' + h
            text += '\n✔️ 기간: ' + sd + " ~ " + ed
            text += "\n\n✔️ 더 자세한 정보를 알고 싶다면 하단 링크에 방문하세요!"
            text += '\n' + l
            self.client.chat_postMessage(channel=self.channel, text=text)            

    def contest_alarm(self, title, host, category, target, startd, endd, estartd, eendd, ad, dday, status, link):
        text = "\n\n     📣 *개발 대회 속보입니다!!!*"
        text += "\n✔️ 제목: " + title
        text += '\n✔️ 카테고리: ' + ", ".join(category)
        text += '\n✔️ 주최: ' + host
        text += '\n✔️ 대상: ' + ", ".join(target)
        text += '\n✔️ 접수 기간: ' + startd + " ~ " + endd
        text += '\n✔️ 심사 기간: ' + estartd + " ~ " + eendd
        text += '\n✔️ 발표일: ' + ad
        text += '\n✔️ D-Day: ' + dday
        text += "\n✔️ 상태: "+ status
        text += "\n\n✔️ 더 자세한 정보를 알고 싶다면 하단 링크에 방문하세요!"
        text += '\n' + link
        self.client.chat_postMessage(channel=self.channel, text=text)

    def velog_alarm(self, titles, writers, texts, links):
        for t, w, texts, l in zip(titles, writers, texts, links):
            text = '\n\n     📢 *개발 트렌드 속보입니다!!!*'
            text += "\n✔️ 제목: " + t
            text += '\n✔️ 작성자: ' + w
            text += "\n\n✔️ 더 자세한 정보를 알고 싶다면 하단 링크에 방문하세요!"
            text += '\n' + l
            self.client.chat_postMessage(channel=self.channel, text=text)
