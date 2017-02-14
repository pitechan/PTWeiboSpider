# -*- coding: utf-8 -*-

import re
import os
import requests
import logging
import time
import threading
from settings import HEADERS, WEIBODATA, COMMENTDATA, COMMENTWEIBOHEADERS, ADDFANSHEADERS, REPOSTWEIBOHEADERS, REPOSTDATA, THUMBWEIBOHEADERS, ABSOLUTEPATH

class Weibo:

    def __init__(self, cookies):
        self.cookies = cookies

    def post(self, content):
        for cookies in self.cookies:
            get_st = requests.get('http://weibo.cn', headers=HEADERS, cookies=cookies)
            try:
                st = re.findall(r'<form action="/mblog/sendmblog\?st=(.*?)"', get_st.text)[0]
            except:
                raise AttributeError('Can not get value for st.')
            WEIBODATA['content'] = content
            requests.post('http://weibo.cn/mblog/sendmblog?st=' + st, headers=HEADERS, cookies=cookies, data=WEIBODATA)

    def comment(self, weibo_url, content):
        try:
            weibo_id = re.findall(r'http://weibo\.cn/comment/(.*?)\?', weibo_url)[0]
        except:
            raise  ValueError('Url does not contain a weibo id')
        COMMENTDATA['id'] = weibo_id
        COMMENTDATA['content'] = content
        COMMENTWEIBOHEADERS['Referer'] = weibo_url
        for cookies in self.cookies:
            get_st = requests.get('http://weibo.cn', headers=HEADERS, cookies=cookies)
            st = re.findall(r'st=(.*?)"', get_st.text)[0]
            get_srcuid = requests.get(weibo_url, headers=HEADERS, cookies=cookies)
            srcuid = re.findall(r'<a href="/u/(.*?)\?', get_srcuid.text)[0]
            COMMENTDATA['srcuid'] = srcuid
            requests.post('http://weibo.cn/comments/addcomment?vt=4&st=' + st, cookies=cookies, headers=COMMENTWEIBOHEADERS, data=COMMENTDATA)

    def addfans(self, user_url):
        ADDFANSHEADERS['Referer'] = user_url
        for cookies in self.cookies:
            get_addfans = requests.get(user_url, cookies=cookies, headers=HEADERS)
            try:
                add_attention_url = re.findall(r'<a href="(/attention/add\?uid=\d+&amp;rl=0&amp;st=\w+)">', get_addfans.text)[0].replace('amp;', '')
            except:
                raise  ValueError('Cannot get add fans url')
            try:
                requests.get('http://weibo.cn' + add_attention_url, cookies=cookies, headers=ADDFANSHEADERS)
            except:
                logging.warning('Error when add fans %s' %cookies)

    def repost(self ,weibo_url, content):
        try:
            weibo_id = re.findall(r'http://weibo\.cn/repost/(.*?)\?', weibo_url)[0]
        except:
            raise  ValueError('Url does not contain a weibo id')
        REPOSTWEIBOHEADERS['Referer'] = weibo_url
        REPOSTDATA['content'] = content
        for cookies in self.cookies:
                get_st = requests.get('http://weibo.cn', headers=HEADERS, cookies=cookies)
                try:
                    st = re.findall(r'st=(.*?)"', get_st.text)[0]
                except:
                    raise AttributeError('Can not get value for st.')
                requests.post('http://weibo.cn/repost/dort/' + weibo_id + '?st=' + st, cookies=cookies, data=REPOSTDATA, headers=REPOSTWEIBOHEADERS)

    def thumb(self, weibo_url):
        try:
            weibo_id = re.findall(r'http://weibo\.cn/repost/(.*?)\?\w+', weibo_url)[0]
        except:
            raise  ValueError('Url does not contain a weibo id')
        THUMBWEIBOHEADERS['Referer'] = weibo_url
        for cookies in self.cookies:
            get_st = requests.get('http://weibo.cn', headers=HEADERS, cookies=cookies)
            try:
                st = re.findall(r'st=(.*?)"', get_st.text)[0]
            except:
                raise AttributeError('Can not get value for st.')
            try:
                suid = re.findall(r'<a href="/(.*?)/info', get_st.text)[0]
            except:
                raise AttributeError('Can not get value for suid.')
            requests.get('http://weibo.cn/attitude/' + weibo_id + '/add?uid=' + suid + '&rl=0&gid=10001&vt=4&st=' + st, cookies=cookies, headers=THUMBWEIBOHEADERS)

    def backup(self, user_url):
        content_list = []
        user_res = requests.get(user_url, headers=HEADERS, cookies=self.cookies[0])
        page_num = re.findall(r'<input name="mp" type="hidden" value="(.*?)"', user_res.text)
        if len(page_num):
            page = page_num[0]
            n = 1
            while n <= int(page):
                url = user_url + '?page=' + str(n)
                res = requests.get(url, headers=HEADERS, cookies=self.cookies[0])
                content = re.findall(r'<span class="ctt">(.*?)</span>', res.text)
                for con in content:
                    print(con)
                    content_list.append(con)
                time.sleep(3)
                n = n + 1
        else:
            content = re.findall(r'<span class="ctt">(.*?)</span>', user_res.text)
            for con in content:
                print(con)
                content_list.append(con)
        with open(os.path.join(ABSOLUTEPATH, 'backup.txt'), 'a') as f:
            for con in content_list:
                f.write(con)

    def specialCare(self, user_url, min=60):
        user_index_res = requests.get(user_url, headers=HEADERS, cookies=self.cookies[0])
        now_content = re.findall(r'<span class="ctt">(.*?)</span>', user_index_res.text)
        n = int(min/3)
        while n > 0:
            user_index_res = requests.get(user_url, headers=HEADERS, cookies=self.cookies[0])
            content = re.findall(r'<span class="ctt">(.*?)</span>', user_index_res.text)
            for con in content:
                if con not in now_content:
                    logging.warning('New weibo captured: %s' % con)
                    now_content.append(con)
            time.sleep(180)
            n-=1

    def specialCareInBackground(self, user_url, min=60):
        t = threading.Thread(target=self.specialCare, args=(user_url, min))
        t.start()

    def search(self, content, pages):
        content_list = []
        url = 'http://weibo.cn/search/mblog?hideSearchFrame=&keyword=' + content + '&page=1'
        url_res = requests.get(url, headers=HEADERS, cookies=self.cookies[0])
        actual_pages = re.findall(r'nbsp;1/(.*?)页</div>', url_res.text)
        if len(actual_pages):
            logging.warning('%s pages searched' % actual_pages)
            if pages > int(actual_pages):
                pages = int(actual_pages)
            n = 1
            while n <= int(pages):
                url = 'http://weibo.cn/search/mblog?hideSearchFrame=&keyword=' + content + '&page=' + str(n)
                res = requests.get(url, headers=HEADERS, cookies=self.cookies[0])
                content = re.findall(r'<span class="ctt">(.*?)</span>', res.text)
                for con in content:
                    print(con)
                    content_list.append(con)
                time.sleep(3)
                n = n + 1
        else:
            res = requests.get(url, headers=HEADERS, cookies=self.cookies[0])
            content = re.findall(r'<span class="ctt">(.*?)</span>', res.text)
            for con in content:
                print(con)
                content_list.append(con)
        with open(os.path.join(ABSOLUTEPATH, 'search.txt'), 'a') as f:
            for con in content_list:
                f.write(con)


