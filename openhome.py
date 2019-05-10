from selenium import webdriver
import time


def open(openPage):
    chrome_path = "C:\chromedriver_win32\chromedriver.exe"
    web = webdriver.Chrome(chrome_path)
    web.get(openPage)
    web.set_window_position(0, 0)  # 瀏覽器位置
    web.set_window_size(700, 700)  # 瀏覽器大小
    time.sleep(5)

    web.close()
