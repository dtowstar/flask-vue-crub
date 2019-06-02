#!/usr/bin/env python
# coding: utf-8

# In[56]:


from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from urllib import request
import requests
import re
import random


def repeatclick(ses, driver):
    try:
        WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable(
            (By.XPATH, "//*[contains(text(), '立即購票')] | //*[contains(text(), '立即索票')]"))).click()
        driver.implicitly_wait(1)
        element = driver.find_element_by_xpath(
            "//*[@id='gameList']/table[1]/tbody[1]/tr["+str(ses)+"]/td[4]/input[1]").click()
    except:
        print("except")


def ticketTicket(tv, driver):

    WebDriverWait(driver, 60).until(EC.element_to_be_clickable(
        (By.XPATH, "//*[@id='TicketForm_agree']"))).click()
    res1 = driver.page_source
    data1 = BeautifulSoup(res1)
    for match in data1.find_all('select', id=re.compile("TicketForm_ticketPrice")):
        Tt = match.get('id')

    # 選擇購買票數
    tvarr = []
    s1 = Select(driver.find_element_by_xpath(
        "//*[@id='"+str(Tt)+"']"))

    for select in s1.options:
        tvarr.append(int(select.text))
    while True:
        if tv in tvarr:
            s1.select_by_index(tv)
            break
        else:
            tv = tv-1
            continue


def runTicketP(iurl, isessionIndex, iprice, iTN):
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(20)
    url = 'https://tixcraft.com/login'
    driver.get(url)
    element = WebDriverWait(driver, 600).until(
        EC.visibility_of_element_located((By.XPATH, "//*[@class='user-name']")))

    securl = iurl
    driver.get(securl)

    ses = int(isessionIndex)+1
    curl = driver.current_url
    while(curl[21:36] == 'activity/detail'):
        repeatclick(ses, driver)
        curl = driver.current_url

    print("pass")
    inAreaN = 0
    inTicketN = 0
    while(curl[21:35] != 'ticket/payment'):

        if curl[21:34] == 'ticket/verify':
            try:
                restv = driver.page_source
                sptv = BeautifulSoup(restv)
                sptv1 = sptv.find('font').text
            except:
                sptv1 = None
                print("no front")
            if(sptv1 != None):
                driver.find_element_by_id("checkCode").clear()
                driver.find_element_by_id("checkCode").send_keys(""+sptv1+"")
                driver.find_element_by_id("submitButton").click()
                WebDriverWait(driver, 5).until(EC.alert_is_present())
                alert = driver.switch_to_alert()
                alert.accept()
            else:
                print("wait user")
                try:
                    WebDriverWait(driver, 2).until(EC.alert_is_present())
                    alert = driver.switch_to_alert()
                    alert.accept()
                    ticketTicket(iTN, driver)
                except:
                    print("no alert")
                continue

        curl = driver.current_url
        if curl[21:32] == 'ticket/area':
            inAreaN += 1
            res = driver.page_source
            pl = str(iprice)
            sp = BeautifulSoup(res)
            sp1 = sp.find_all('div', {"class": "zone area-list"})
            sp2 = [s.find_all('a') for s in sp1]
            sp3 = [s.text[1:].split()[0] for s in sp2[0]]
            print("inarea")
            sp4 = []
            for s in sp3:
                if pl in s:
                    sp4.append(s)

            if len(sp4) != 0:
                rc = random.choice(sp4)

                element = WebDriverWait(driver, 600).until(EC.visibility_of_element_located(
                    (By.XPATH, "//*[contains(text(), '"+str(rc)+"')]")))
                etext = element.find_element_by_xpath("..").text
                if ('剩餘' in etext) or ('熱賣中' in etext):
                    element.click()
                curl = driver.current_url

            else:
                curl = driver.current_url
                cid = curl[-4:]
                list = []
                for match in sp.find_all('a', id=re.compile(""+cid+"")):
                    list.append(match.get('id'))
                rs = random.choice(list)
                # 選區域(價格)(隨機)
                WebDriverWait(driver, 600).until(
                    EC.element_to_be_clickable((By.ID, ""+rs+""))).click()
                curl = driver.current_url

        elif(curl[21:34] == 'ticket/ticket'):
            if(inAreaN > inTicketN):
                inTicketN += 1
                ticketTicket(iTN, driver)

            else:
                print("wait user")
                try:
                    WebDriverWait(driver, 3).until(EC.alert_is_present())
                    alert = driver.switch_to_alert()
                    alert.accept()
                    ticketTicket(iTN, driver)
                except:
                    print("no alert")

                continue

    # In[ ]:

    # In[54]:

    '''from selenium import webdriver
    from selenium.webdriver.support.ui import Select
    import time
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.wait import WebDriverWait
    from selenium.webdriver.common.keys import Keys
    from bs4 import BeautifulSoup
    import requests
    import re
    import random

    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(20)
    url = 'https://tixcraft.com/login'
    driver.get(url)
    element = WebDriverWait(driver, 600).until(
        EC.visibility_of_element_located((By.XPATH, "//*[@class='user-name']")))
    securl = 'https://tixcraft.com/activity/detail/19_BSB'
    driver.get(securl)
    '''


runTicketP('https://tixcraft.com/activity/detail/19_ELLA', '0', '1200', 1)

# In[ ]:
