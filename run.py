# -*- coding: utf-8 -*-
# @Author  : Yuncong
# @Email   : yuncongzt@163.com

from waitress import serve
from application import app
from jobs.Spider import Spider
from flask import jsonify
import json

import click
@app.cli.command()
@click.argument("start")
def wish(start):
    resp = {'code': 200, 'msg': '获取成功', 'data': {}}
    works, work_num =Spider().get_book_wish(int(start)*15)
    if len(works) > 0:
        temp = {
            'works': works,
            'total': work_num,
        }
        resp['data'] = temp
    else:
        resp['code'] = -1
        resp['msg'] = "数据为空"
    click.echo(json.dumps(resp))

if __name__ == '__main__':
    serve(app, listen='*:5000', threads=10)
