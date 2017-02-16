# -*- coding: utf-8 -*-

import sys
import logging
from cookie import Cookie
from user import User
from captcha import Captcha
from datetime import datetime
from settings import HEADERS, LOGINDATA


class Login:

    def __init__(self):
        self.user = None
        self.captcha = None
        self.login()

    def login(self, retry=False):
        self.user = User.new()
        if not retry:
            self.captcha = Captcha.new()
        LOGINDATA['mobile'] = self.user.phone_num
        LOGINDATA[self.captcha.password_vk] = self.user.password
        LOGINDATA['code'] = self.captcha.code
        LOGINDATA['vk'] = self.captcha.vk
        LOGINDATA['capId'] = self.captcha.cap_id
        self.captcha.requests_session.post(self.captcha.login_url, headers=HEADERS, data=LOGINDATA)
        logined_page = self.captcha.requests_session.get('http://weibo.cn/?vt=4', headers=HEADERS)
        if '登录' in logined_page.text:
            logging.warning('Login failed.')
            retry_or_exit = input("Enter 'n' in order to retry, else enter any other words:")
            if retry_or_exit == 'n':
                self.login(retry=True)
            else:
                sys.exit()
        else:
            logging.warning('Login success.')
            new_cookie = Cookie(self.user.phone_num, datetime.now(), self.captcha.requests_session.cookies.get_dict())
            new_cookie.save()
