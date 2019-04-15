#! /usr/bim/env python
# _*_ coding: utf-8 _*_
# __author__ * "science +"
# Email: 110@163.com

user_status = False

def login(auto_type):
    def outer(func):
        def inner(*args,**kwargs):
            _username = "htl"
            _password = "123"
            global user_status

            if user_status == False:
                # username = raw_input("user:")
                # password = raw_input("password:")

                username = input("user:")
                password = input("password:")

                # print (username)
                # print (password)
                # print (username == _username)
                # print (password == _password)

                if username == _username and password == _password:
                    print ("welcome login....")
                    user_status = True
                else:
                    print("wrong username or password!")
            else:
                print("用户已登录...")
            if user_status == True:
                func(*args,**kwargs)

        return inner
    return outer


def home():
    print("----首页----")

def america():
    print("----欧美专区----")

@login("qq")
def japan(style):
    print("----日韩专区----",style)

@login("weibo")
def henan(style):
    print("----河南专区----",style)

home()
# henan = login(henan)
# henan()
# japan = login(japan)
# japan = login("qq",japan)
japan("4p")
henan("双飞")

# america()