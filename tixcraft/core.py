from lxml import etree
from PIL import Image
from time import sleep
import requests
import shutil
import json
from tixcraft import parser
from tixcraft.picker import AreaPicker


session = requests.Session()


class SessionFileNotFoundError(RuntimeError):
    pass


class NoLoggingError(RuntimeError):
    pass


class ActivityIndexError(RuntimeError):
    pass


class PaymentError(RuntimeError):
    pass


class UndefinedUrlError(RuntimeError):
    pass


class TixCraft:
    def __init__(self, activity_url, **setting):
        self.ACTIVITY_URL = activity_url
        self.ACTIVITY_INDEX = setting.get("activity_index", 0)
        self.TICKET_NUMBER = setting.get("ticket_number", 1)
        self.AREA_NAME = setting.get("area_name", "")
        self.AREA_PRICE = setting.get("area_price", 0)
        self.RULE = setting.get("rule", "")
        self.session = requests.Session()

    def _load_cookies(self):
        try:
            with open("session.json") as f:
                cookies = json.load(f)
            for cookie in cookies:
                session.cookies.set(cookie["name"], cookie["value"])
        except FileNotFoundError:
            raise SessionFileNotFoundError("檔案session.json不存在")

    def _set_lang_zh_tw(self):
        r = requests.get("https://tixcraft.com/user/changeLanguage/lang/zh_tw")
        cookies = r.cookies.get_dict()
        session.cookies.update({'lang': cookies['lang']})

    def get_username(self):
        r = session.get("https://tixcraft.com")
        html = etree.HTML(r.text)
        username = html.xpath('//a[@class="user-name"]/text()')
        if not username:
            raise NoLoggingError("尚未登入tixCraft")
        return username[0]

    def activity_detail(self, url):
        url = url.replace("detail", "game")
        return url

    def activity_game(self, source_code):
        html = etree.HTML(source_code)
        urls = html.xpath('//td[@class="gridc"]/input/@data-href')
        try:
            url = urls[self.ACTIVITY_INDEX]
        except IndexError:
            raise ActivityIndexError("活動場次索引不存在")

        return "https://tixcraft.com" + url

    def ticket_verify(self, source_code):
        html = etree.HTML(source_code)
        CSRFTOKEN = parser.CSRFTOKEN(html)
        checkCode = parser.checkcode(html)

        data = {"CSRFTOKEN": CSRFTOKEN, "checkCode": checkCode, "confirmed": "true"}
        url = parser.checkcode_url(source_code)
        r = session.post(url, data=data)
        url = parser.json_url(r.text)

        return "https://tixcraft.com" + url

    def ticket_area(self, source_code, rule="highest"):

        areas, price_status = parser.areas(source_code)
        areaUrlList = parser.areaUrlList(source_code)

        area_setting = {
            "AREA_NAME": self.AREA_NAME,
            "AREA_PRICE": self.AREA_PRICE,
            "RULE": self.RULE,
        }
        picker = AreaPicker(areas, areaUrlList, **area_setting)
        url = picker.pick_area()
        return "https://tixcraft.com" + url

    def show_captcha(self):
        r = session.get("https://tixcraft.com/ticket/captcha", stream=True)
        if r.status_code == 200:
            with open("captcha.png", "wb") as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)

            image = Image.open("captcha.png")
            image.show()

    def ticket_ticket(self, url, source_code):
        self.show_captcha()
        html = etree.HTML(source_code)
        CSRFTOKEN = parser.CSRFTOKEN(html)
        ticketPrice = parser.ticketPrice(html)
        verifyCode = input("請輸入驗證碼: ")
        agree = parser.agree(source_code)

        ticket_number = self.TICKET_NUMBER
        optional_number = parser.optional_number(html)

        if ticket_number > optional_number:
            ticket_number = optional_number
            print(f"剩餘可選{optional_number}張")

        ticket_number = str(ticket_number)

        data = {
            "CSRFTOKEN": CSRFTOKEN,
            ticketPrice: ticket_number,
            "TicketForm[verifyCode]": verifyCode,
            agree: "1",
            "ticketPriceSubmit": "",
        }
        return url, data

    def ticket_order(self):
        return "https://tixcraft.com/ticket/check"

    def ticket_check(self, url, source_code):
        json_data = json.loads(source_code)
        message = json_data["message"]
        time = int(json_data["time"])

        if time == 0:
            url = parser.location_replace(message)
            url = "https://tixcraft.com" + url
        else:
            print(f"請等待: {time}秒")
            sleep(time)
        return url

    def ticket_payment(self, source_code):
        if "訂購確認" in source_code:
            url = ""
            return url
        raise PaymentError("PaymentError")

    def request(self, url, data=None):
        if data is None:
            r = session.get(url)
        else:
            r = session.post(url, data=data)
        return r.url, r.text

    def next_step(self, url, source_code):
        data = None
        if "activity/detail" in url:
            url = self.activity_detail(url)
        elif "activity/game" in url:
            url = self.activity_game(source_code)
        elif "ticket/verify" in url:
            url = self.ticket_verify(source_code)
        elif "ticket/area" in url:
            url = self.ticket_area(source_code)
        elif "ticket/ticket" in url:
            url, data = self.ticket_ticket(url, source_code)
        elif "ticket/order" in url:
            url = self.ticket_order()
        elif "ticket/check" in url:
            url = self.ticket_check(url, source_code)
        elif "ticket/payment" in url:
            url = self.ticket_payment(source_code)
        else:
            raise UndefinedUrlError("未定義Url: " + url)

        if url != "":
            url, source_code = self.request(url, data)
        # print(url)
        return url, source_code

    def run(self):

        url = self.ACTIVITY_URL
        source_code = ""

        try:
            self._load_cookies()
            self._set_lang_zh_tw()
            username = self.get_username()
            print("會員:" + username)

            while True:
                url, source_code = self.next_step(url, source_code)
                if url == "":
                    break
            print("Good")
        except RuntimeError as e:
            print(e)
            print("QQ")