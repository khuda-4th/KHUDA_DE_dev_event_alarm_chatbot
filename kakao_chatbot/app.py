from flask import Flask, render_template, jsonify, request
from utils import *

app=Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World!'

@app.route("/dev_event", methods= ["POST"])
def dev_event():
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
