from flask import Flask, request, jsonify, render_template, json, Response
from flask_cors import CORS
from selenium import webdriver
import time
from get_img import save_img
from newTicket import runTicketP
from tixcraft.core import TixCraft
from tixcraft.driver import login
from tixcraft import parser

app = Flask(__name__,
            static_folder="./dist/static",
            template_folder="./dist")
CORS(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/getActivatyName_URL', methods=('GET', 'POST'))
def getActivatys():
    temp = {}
    activatyName = []
    urlL = []
    temp = parser.all_activaties_url()
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
    sessionTime, statuses = parser.events(gURL)
    pURL = save_img(gURL)
    sp = {
        'rSessionTime': sessionTime,
        'rPURL': pURL,
        'rstatus': [not status for status in statuses]

    }
    return jsonify(sp)


@app.route('/getForm', methods=('GET', 'POST'))
def runProgram():
    gobject = request.json.get('sform')
    ret_dict = json.loads(gobject)
    gAURL = ret_dict['activate_URL']
    gTPrice = ret_dict['ticket_areaPrice']
    gTN = int(ret_dict['ticket_number'])
    gSI = ret_dict['session_index']
    gTAName = ret_dict['ticket_areaName']
    gTR = ret_dict['ticket_rule']
    gSorR = ret_dict['SorR']

    sTR = ""
    if(gTR == True):
        sTR = "HIGHEST_PRICE"
    else:
        sTR = "LOWEST_PRICE"
    if(gSorR == False):
        runTicketP(gAURL, gSI, gTPrice, gTN)
    else:
        driver = webdriver.Chrome()
        cookies = login(driver)
        tixcraft = TixCraft(gAURL, cookies, ticket_number=gTN, area_price=gTPrice,
                            activity_index=gSI, area_name=gTAName, rule=sTR)
        tixcraft.run()
    return 'True'


if __name__ == '__main__':
    app.run()
