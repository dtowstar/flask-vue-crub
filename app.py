from flask import Flask, request, jsonify, render_template, json, Response
from flask_cors import CORS
from selenium import webdriver
import time
from openhome import open
from get import getActivatyName_URL
from get import getSessionTime


# @app.route('/', methods=['GET'])
# def ping_pong():
#   return jsonify("FHASDKF")  # （jsonify返回一个json格式的数据）

app = Flask(__name__,
            static_folder="./dist/static",
            template_folder="./dist")
CORS(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/confirmPage', methods=('GET', 'POST'))
def login():
    openhome = request.json.get('homepage')
    print(openhome)
    if request.method == 'POST':
        open(openhome)
        return jsonify(openhome)
    else:
        return jsonify(openhome)


@app.route('/getActivatyName_URL', methods=('GET', 'POST'))
def getActivatys():
    temp = {}
    activatyName = []
    temp = getActivatyName_URL()
    activatyName = list(temp.keys())
    return jsonify(activatyName)


@app.route('/useSessionTime', methods=('GET', 'POST'))
def useSessionTime():
    activatyN = request.json.get('activatyName')
    temp = {}
    temp = getActivatyName_URL()
    getURL = temp[activatyN]
    sessionTime = []
    sessionTime = getSessionTime(getURL)
    return jsonify(sessionTime)


if __name__ == '__main__':
    app.run()
