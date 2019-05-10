#!/usr/bin/env python
# coding: utf-8

# In[57]:


import requests
from bs4 import BeautifulSoup

# In[58]:

activities = {}
# 抓活動場次的時間


def getSessionTime(getHref):
    tahref = getHref.replace("detail", "game")
    r = requests.get(tahref)
    soup = BeautifulSoup(r.text, 'html.parser')
    tr_tags = soup.find_all(class_='gridc fcTxt')
    times = [tr.td.string for tr in tr_tags]

    return times


# In[59]:


# 抓活動詳細資訊的連結

def getActivatyURL():
    r = requests.get('https://tixcraft.com/activity/detail/19_JackyWu')
    soup = BeautifulSoup(r.text, 'html.parser')
    a_tag = soup.find(class_='btn btn-default btn-lg')
    href = a_tag['href']

    return href


# In[60]:


# 抓取所有活動名稱和網址

def getActivatyName_URL():
    r = requests.get('https://tixcraft.com/activity')
    soup = BeautifulSoup(r.text, 'html.parser')
    tbody_tag = soup.find('tbody')
    a_tags = tbody_tag.find_all(class_='fcDark')

    for a_tag in a_tags:
        href = a_tag['href']
        activities[a_tag.string] = f'http://tixcraft.com{href}'

    # for name, href in activities.items():
        #print(name, '\t', href)

    # activities = {'activities': activities}

    return activities
