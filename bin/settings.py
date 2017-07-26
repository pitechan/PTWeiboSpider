# -*- coding: utf-8 -*-

import os

ABSOLUTEPATH = os.path.split(os.path.realpath(__file__))[0]

HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
    }

COMMENTWEIBOHEADERS = ADDFANSHEADERS = REPOSTWEIBOHEADERS = THUMBWEIBOHEADERS = {
        'Referer': '',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
    }

LOGINDATA = {
        'remember': 'on',
        'backURL': 'http%3A%2F%2Fweibo.cn%2F',
        'backTitle': '微博',
        'tryCount': '',
        'submit': '登录',
    }

WEIBODATA = {
        'rl': '0',
        'content': ''
    }

COMMENTDATA = {
        'srcuid': '',
        'id': '',
        'rl': '1',
        'content': ''
    }

REPOSTDATA = {
        'act': 'dort',
        'rl': '2',
        'id': 'EuMI563xx',
        'content': ''
    }
