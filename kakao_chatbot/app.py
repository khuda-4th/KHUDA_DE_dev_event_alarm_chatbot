from flask import Flask, render_template, jsonify, request
from utils import *

app=Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World!'

@app.route("/dev_event", methods= ["POST"])
def main_page():
        # 검색 타입(예매 순위 or 개봉 예정작)과 검색 시작 번호를 movie_search 함수로 전달하여 아이템과 버튼 설정을 반환받음  
    listItems = make_devcard()
    # 카드 리스트형 응답용 메시지
    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "carousel": {
                        "type": "basicCard",
                        "items" : listItems
                    }
                }
            ]
        }
    }
    # 전송
    return jsonify(res)

@app.route("/velog_event", methods= ["POST"])
def velog_event():
    listItems = make_velogcard()
    # 카드 리스트형 응답용 메시지
    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "carousel": {
                        "type": "basicCard",
                        "items" : listItems
                    }
                }
            ]
        }
    }

    # 전송
    return jsonify(res)

@app.route("/contest_event", methods= ["POST"])
def contest_event():
        # 검색 타입(예매 순위 or 개봉 예정작)과 검색 시작 번호를 movie_search 함수로 전달하여 아이템과 버튼 설정을 반환받음  
    listItems = make_eventcard()
    # 카드 리스트형 응답용 메시지
    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "carousel": {
                        "type": "basicCard",
                        "items" : listItems
                    }
                }
            ]
        }
    }

    # 전송
    return jsonify(res)



if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
