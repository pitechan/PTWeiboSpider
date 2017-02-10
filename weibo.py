# -*- coding: utf-8 -*-

import os
import re
import sys
import ast
import time
import logging
import datetime
import threading
import requests

class Captcha:

    def __init__(self, cap_id=None, vk=None, password_vk=None, code=None, login_url=None):
        self.cap_id = cap_id
        self.vk = vk
        self.password_vk = password_vk
        self.code = code
        self.login_url = login_url

class User:

    def __init__(self, phone_num=None, password=None, cookie=None):
        self.phone_num = phone_num
        self.password = password
        self.cookie = cookie

class WeiboSpider:

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
    }

    login_data = {
        'remember': 'on',
        'backURL': 'http%3A%2F%2Fweibo.cn%2F',
        'backTitle': '微博',
        'tryCount': '',
        'submit': '登录',
    }

    base_url = 'https://weibo.cn/login/'
    absolute_path = os.path.split(os.path.realpath(__file__))[0]

    requests_session = requests.session()

    user = User()
    captcha = Captcha()

    user_list = []
    cookie_list = []

    def downloadCaptcha(self):
        login_page = self.requests_session.get('http://login.weibo.cn/login/?ns=1&revalid=2&backURL=http%3A%2F%2Fweibo.cn%2F&backTitle=%CE%A2%B2%A9&vt=', headers=self.headers)
        try:
            vk = re.findall(r'input type=\"hidden\" name=\"vk\" value=\"(.*?)\"', login_page.text)[0]
        except:
            raise  AttributeError('Can not get value for vk.')
        password_vk = 'password_' + str(vk.split('_')[0])
        try:
            cap_id = re.findall(r'input type=\"hidden\" name=\"capId\" value=\"(.*?)\"', login_page.text)[0]
        except:
            raise AttributeError('Can not get value for cap_id.')
        try:
            login_url = self.base_url + re.findall(r'form action=\"(.*?)\"', login_page.text)[0]
        except:
            raise  AttributeError('Can not get value for login_url.')
        cap_pic = self.requests_session.get('http://weibo.cn/interface/f/ttt/captcha/show.php?cpt=' + cap_id, headers=self.headers)
        with open(self.absolute_path + '/captcha.jpg', 'wb') as f:
            f.write(cap_pic.content)
        logging.warning('Captcha picture has been downloaded.')
        self.captcha.password_vk = password_vk
        self.captcha.cap_id = cap_id
        self.captcha.vk = vk
        self.captcha.login_url = login_url

    def getVerificationCode(self):
        verification_code = input("Please enter the verification code shown in the picture. Enter 'n' if the picture is blur:")
        if verification_code == 'n':
            self.downloadCaptcha()
            self.getVerificationCode()
        else:
            self.captcha.code = verification_code

    def enterLoginData(self):
        phone_num = input('Please enter the phone number:')
        password = input('Please enter the password:')
        self.user.phone_num = phone_num
        self.user.password = password

    def loginWeibo(self, retry=False):
        self.downloadCaptcha()
        self.getVerificationCode()
        if not retry:
            self.enterLoginData()
        self.login_data['mobile'] = self.user.phone_num
        self.login_data[self.captcha.password_vk] = self.user.password
        self.login_data['code'] = self.captcha.code
        self.login_data['vk'] = self.captcha.vk
        self.login_data['capId'] = self.captcha.cap_id
        login_page = self.requests_session.post(self.captcha.login_url, headers=self.headers, data=self.login_data)
        logined_page = self.requests_session.get('http://weibo.cn/?vt=4', headers=self.headers)
        if '登录' in logined_page.text:
            logging.warning('Login failed.')
            retry_or_exit = input("Enter 'n' in order to retry, else enter any other words:")
            if retry_or_exit == 'n':
                self.loginWeibo(retry=True)
            else:
                sys.exit()
        else:
            logging.warning('Login success.')

    def saveLoginedCookie(self):
        with open(self.absolute_path + '/cookie.txt', 'a+') as f:
            f.write('PhoneNum:' + self.user.phone_num + ' | ' + str(datetime.datetime.now()) + '\n' + str(self.requests_session.cookies.get_dict()) + '\n')

    def readCookieFile(self):
        with open(self.absolute_path + '/cookie.txt', 'r') as f:
            for line in f.readlines():
                info_dict = {}
                phone_number = re.findall(r'PhoneNum:(.*?) \|', line)
                self.user_list = self.user_list + phone_number
                cookie = re.findall(r'(\{.*\})', line)
                for item in cookie:
                    self.cookie_list.append(ast.literal_eval(item))
        if len(self.user_list) == 0:
            logging.warning('Cookie does not exist')
        else:
            logging.warning("Get %s cookies" % len(self.user_list))

    def checkCookie(self, cookie):
        test_page = requests.get('http://weibo.cn', headers=self.headers, cookies=cookie)
        if '登录' not in test_page.text:
            logging.warning('Valid Cookie')
            return True
        else:
            logging.warning('Invaild Cookie.')
            return False

    def run(self):
        self.loginWeibo()
        self.saveLoginedCookie()

if __name__ == '__main__':
    spider = WeiboSpider()
    spider.run()


