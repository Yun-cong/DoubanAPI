# -*- coding: utf-8 -*-
# @Author  : Yuncong
# @Email   : yuncongzt@163.com

import os
import pymongo

CLIENT = pymongo.MongoClient('mongodb://user:passwd.@localhost:27017')
DB = CLIENT['dbname']

DOMAIN = 'http://localhost'
ROOT_PATH = os.getcwd()

MAX_COUNT = 20

DOUBAN = 'https://movie.douban.com'

UID='' #从个人主页获取uid


HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Referer': 'https://movie.douban.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    'Cookie': '',  # 浏览器登录后复制Cookie贴到此处
}

PROXIES = []  # 放代理ip，格式如xx.xx.xx.xx:xx
