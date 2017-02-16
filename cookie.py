# -*- coding: utf-8 -*-

import os
import re
import ast
import logging
import requests
from settings import ABSOLUTEPATH, HEADERS


class Cookie:

    def __init__(self, phone_num, date, params):
        self.phone_num = phone_num
        self.date = date
        self.params = params

    def save(self):
        with open(os.path.join(ABSOLUTEPATH, 'cookie.txt'), 'a') as f:
            f.write('PhoneNum:' + self.phone_num + ' | ' + str(self.date) + '\n' + str(self.params) + '\n')

    def check(self):
        test_page = requests.get('http://weibo.cn', headers=HEADERS, cookies=self.params)
        if '登录' not in test_page.text:
            logging.warning('Valid Cookie')
            return True
        else:
            logging.warning('Invaild Cookie.')
            return False

    @staticmethod
    def read():
        cookie_list = []
        user_list = []
        user_cookie_dict = {}
        with open(os.path.join(ABSOLUTEPATH, 'cookie.txt'), 'r') as f:
            for line in f.readlines():
                phone_number = re.findall(r'PhoneNum:(.*?) \|', line)
                user_list += phone_number
                cookie = re.findall(r'(\{.*\})', line)
                for item in cookie:
                    cookie_list.append(ast.literal_eval(item))
        if len(user_list) == 0:
            logging.warning('No cookie')
        else:
            logging.warning("Get %s cookies" % len(user_list))
        for index, phone_number in enumerate(user_list):
            user_cookie_dict[phone_number] = cookie_list[index]
        return user_cookie_dict
