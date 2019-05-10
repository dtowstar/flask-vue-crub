from flask import Flask, request, jsonify, render_template, json, Response
from flask_cors import CORS
from selenium import webdriver
import time
from openhome import open
from get import getActivatyName_URL
from get import getSessionTime
from get_img import save_img


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
    urlL = []
    temp = getActivatyName_URL()
    activatyName = list(temp.keys())
    urlL = list(temp.values())
    nURL = {
        'name': activatyName,
        'url': urlL,
    }
    return jsonify(nURL)


@app.route('/useSessionTime', methods=('GET', 'POST'))
def useSessionTime():
    gURL = request.json.get('sURL')
    sessionTime = getSessionTime(gURL)
    pURL = save_img(gURL)
    sp = {
        'rSessionTime': sessionTime,
        'rPURL': pURL,
    }
    return jsonify(sp)


if __name__ == '__main__':
    app.run()
