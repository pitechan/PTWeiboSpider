# -*- coding: utf-8 -*-

import re
import os
import logging
import requests
from settings import HEADERS, ABSOLUTEPATH

def new():
    requests_session = requests.session()
    login_page = requests_session.get(
        'http://login.weibo.cn/login/?ns=1&revalid=2&backURL=http%3A%2F%2Fweibo.cn%2F&backTitle=%CE%A2%B2%A9&vt=',
        headers=HEADERS)
    try:
        vk = re.findall(r'input type=\"hidden\" name=\"vk\" value=\"(.*?)\"', login_page.text)[0]
    except:
        raise AttributeError('Can not get value for vk.')
    try:
        cap_id = re.findall(r'input type=\"hidden\" name=\"capId\" value=\"(.*?)\"', login_page.text)[0]
    except:
        raise AttributeError('Can not get value for cap_id.')
    try:
        login_url = 'https://weibo.cn/login/' + re.findall(r'form action=\"(.*?)\"', login_page.text)[0]
    except:
        raise AttributeError('Can not get value for login_url.')
    cap_pic = requests_session.get('http://weibo.cn/interface/f/ttt/captcha/show.php?cpt=' + cap_id, headers=HEADERS)
    with open(os.path.join(ABSOLUTEPATH, 'captcha.jpg'), 'wb') as f:
        f.write(cap_pic.content)
    logging.warning('Captcha picture has been downloaded.')
    code = input(
        "Please enter the verification code shown in the picture. Enter 'n' if the picture is blur:")
    if code == 'n':
        new()
    else:
        new_captcha = Captcha(requests_session, cap_id, vk, code, login_url)
        new_captcha.password_vk = 'password_' + str(vk.split('_')[0])
        return new_captcha

class Captcha:

    def __init__(self, requests_session, cap_id, vk, code, login_url):
        self.requests_session = requests_session
        self.cap_id = cap_id
        self.vk = vk
        self.code = code
        self.login_url = login_url
        self.password_vk = 'password_' + str(vk.split('_')[0])

