# -*- coding: utf-8 -*-

def new():
    phone_num = input('Please enter the phone number:')
    password = input('Please enter the password:')
    return User(phone_num=phone_num, password=password)

class User:

    def __init__(self, phone_num, password, cookie=None):
        self.phone_num = phone_num
        self.password = password