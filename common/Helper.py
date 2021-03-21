# -*- coding: utf-8 -*-
# @Author  : Yuncong
# @Email   : yuncongzt@163.com

import datetime

'''获取当前时间'''


def getCurrentDate():
    return datetime.datetime.now()


'''获取格式化的时间'''


def getFormatDate(date=None, format="%Y.%m.%d %H:%M"):
    if date is None:
        date = datetime.datetime.now()
    return date.strftime(format)


'''获取年月日'''


def getYMD(date=None, format="%Y.%m.%d"):
    if date is None:
        date = datetime.datetime.now()
    return date.strftime(format)


""" 豆瓣爬取数据处理 """


def get_id(href):
    """
    通过链接获取id
    :param href: 链接
    :return: id
    """
    return str(href).split('/')[-2]


def replace_img(src):
    """
    替换图片格式 webp->jpg
    :param src: 图片链接
    :return: 替换后的链接
    """
    return str(src).replace('.webp', '.jpg')


def replace_null(content, keywords):
    """
    将部分内容替换为空 即删除部分
    :param content: 要替换的内容
    :param keywords: 要替换的关键词 []
    :return: 替换后的字符串
    """
    for i in keywords:
        content = str(content).replace(i, '')
    return content


def get_stars(average):
    """
    通过评分获取星级
    :param average: 评分
    :return: 星级
    """
    average = float(average) if len(average) > 0 else 0.0
    if average >= 9.5:
        stars = '50'
    elif 8.5 <= average < 9.5:
        stars = '45'
    elif 7.5 <= average < 8.5:
        stars = '40'
    elif 6.5 <= average < 7.5:
        stars = '35'
    elif 5.5 <= average < 6.5:
        stars = '30'
    elif 4.5 <= average < 5.5:
        stars = '25'
    elif 3.5 <= average < 4.5:
        stars = '20'
    elif 2.5 <= average < 2.5:
        stars = '15'
    elif 1.5 <= average < 2.5:
        stars = '10'
    else:
        stars = '00'
    return stars


def split_a(content):
    """
    通过 / 拆封字符串
    :param content: 要拆分的内容
    :return: 拆分后的列表
    """
    return str(content).split(' / ')


def check_cn(content):
    """
    检测是否包含中文字符
    :param content: 要检测文本
    :return: {bool} 包含返回True， 不包含返回False
    """
    for ch in str(content):
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False
