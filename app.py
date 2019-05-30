from flask import Flask, request, jsonify, render_template, json, Response
from flask_cors import CORS
from selenium import webdriver
import time
#from openhome import open
from get import getActivatyName_URL
from get import getSessionTime
from get_img import save_img
from newTicket import runTicketP
from tixcraft.core import TixCraft

app = Flask(__name__,
            static_folder="./dist/static",
            template_folder="./dist")
CORS(app)


@app.route('/')
def index():
    return render_template('index.html')


# @app.route('/confirmPage', methods=('GET', 'POST'))
# def login():
    #openhome = request.json.get('homepage')
    # print(openhome)
    # if request.method == 'POST':
    # open(openhome)
    # return jsonify(openhome)
    # else:
    # return jsonify(openhome)


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
    sessionTime, status = getSessionTime(gURL)
    pURL = save_img(gURL)
    sp = {
        'rSessionTime': sessionTime,
        'rPURL': pURL,
        'rstatus': status
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
    print(gAURL)
    print(gTPrice)
    print(gTN)
    print(gSI)
    print(gTAName)
    print(gTR)
    print(gSorR)
    sTR = ""
    if(gTR == True):
        sTR = "HIGHEST_PRICE"
    else:
        sTR = "LOWEST_PRICE"
    if(gSorR == False):
        runTicketP(gAURL, gSI, gTPrice, gTN)
    else:
        tixcraft = TixCraft(gAURL, ticket_number=gTN, area_price=gTPrice,
                            activity_index=gSI, area_name=gTAName, rule=sTR)
        tixcraft.run()
    return 'True'


if __name__ == '__main__':
    app.run()
