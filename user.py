# -*- coding: utf-8 -*-

class User:

    def __init__(self, phone_num, password):
        self.phone_num = phone_num
        self.password = password

    @staticmethod
    def new():
        phone_num = input('Please enter the phone number:')
        password = input('Please enter the password:')
        return User(phone_num=phone_num, password=password)