from bs4 import BeautifulSoup
import requests
import shutil


def save_img(url):
    # url: https://tixcraft.com/activity/detail/19_ERIC'
    img_src = get_img_src(url)
    if(img_src == ""):
        return img_src
    else:
        res = requests.get(img_src, stream=True)
        if res.status_code == 200:
            print(img_src)
            return img_src


def get_img_src(url):
    # url: https://tixcraft.com/activity/detail/19_ERIC'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    try:
        img_src = soup.find('img', alt='示意圖僅供參考示意1')['src']
    except:
        img_src = ""

    return img_src


# save_img('https://tixcraft.com/activity/detail/19_TPENEPAL')
