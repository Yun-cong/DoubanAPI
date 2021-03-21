# -*- coding: utf-8 -*-
# @Author  : Yuncong
# @Email   : yuncongzt@163.com

import os
from flask import Flask, request, jsonify


class Application(Flask):
    def __init__(self, import_name, template_folder=None, root_path=None, static_folder=None):
        super(Application, self).__init__(import_name, template_folder=template_folder, root_path=root_path,
                                          static_folder=static_folder)


def register_blueprints(app):
    from api.douban import douban
    app.register_blueprint(douban, url_prefix="/api/douban")


app = Application(__name__, template_folder=os.getcwd() + "/web/templates/", root_path=os.getcwd(),
                  static_folder=os.getcwd() + "/web/static/")
app.config.from_pyfile('config/base_setting.py')
register_blueprints(app)

""" 全局路径拦截 """


@app.before_request
def before_request():
    path = request.path
    if '/api/douban/' not in path:
        resp = {'code': 404, 'msg': '豆瓣api测试，路径不存在', 'data': {}}
        return jsonify(resp), 404
