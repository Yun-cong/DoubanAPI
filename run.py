# -*- coding: utf-8 -*-
# @Author  : Yuncong
# @Email   : yuncongzt@163.com

from waitress import serve
from application import app

if __name__ == '__main__':
    serve(app, listen='*:5000', threads=10)
