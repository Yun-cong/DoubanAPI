# -*- coding: utf-8 -*-
# @Author  : Yuncong
# @Email   : yuncongzt@163.com

from flask import Blueprint, request, jsonify
from jobs.Spider import Spider

douban = Blueprint('douban', __name__)

"""自建豆瓣电影信息API"""

'''获取电影列表'''


@douban.route('/list', methods=["GET"])
def get_list():
    # 此处本为从本地数据库获取，故start仅top250有效，且*25
    resp = {'code': 200, 'msg': '获取成功', 'data': {}}
    req = request.values
    listname = req['listname'] if 'listname' in req else ''
    start = int(req['start'] if 'start' in req and len(req['start']) > 0 else 0)
    if listname is None or len(listname) < 1:
        resp['code'] = -1
        resp['msg'] = "参数为空"
        return jsonify(resp)
    if listname not in ['nowplaying', 'later', 'hotmovie', 'hottv', 'top250']:
        resp['code'] = -1
        resp['msg'] = "参数错误"
        return jsonify(resp)

    if listname == 'nowplaying':
        data = Spider().get_nowplaying()
    elif listname == 'later':
        data = Spider().get_later()
    elif listname == 'hotmovie':
        data = Spider().get_hot('movie')
    elif listname == 'hottv':
        data = Spider().get_hot('tv')
    else:
        data = Spider().get_top250(start)

    if data:
        resp['data']['list'] = data
        resp['data']['listname'] = listname
        resp['data']['start'] = start
        resp['data']['count'] = len(data)
    else:
        resp['code'] = -1
        resp['msg'] = '内部错误或数据为空'

    return jsonify(resp)


'''获取电影信息'''


@douban.route('/movie', methods=["GET"])
def get_movie():
    resp = {'code': 200, 'msg': '获取成功', 'data': {}}
    req = request.values
    id = req['id'] if 'id' in req else ''
    if id is None or len(id) < 1:
        resp['code'] = -1
        resp['msg'] = "ID为空"
        return jsonify(resp)

    base_data, extra_data = Spider().get_movieinfo(id)
    if len(base_data) > 2:
        resp['data'] = base_data
    else:
        resp['code'] = -1
        resp['msg'] = '内部错误或数据为空'

    return jsonify(resp)


'''获取电影剧照'''


@douban.route('/movie/pic', methods=["GET"])
def get_movie_photo():
    resp = {'code': 200, 'msg': '获取成功', 'data': {}}
    req = request.values
    id = req['id'] if 'id' in req else ''
    type = req['type'] if 'type' in req and req['type'] in ['S', 'R'] else ''
    sort = req['sort'] if 'sort' in req and req['sort'] in ['like', 'size', 'time'] else 'like'
    start = int(req['start'] if 'start' in req and len(req['start']) > 0 else 0)
    if id is None or len(id) < 1:
        resp['code'] = -1
        resp['msg'] = "ID为空"
        return jsonify(resp)
    if type is None or len(type) < 1:
        resp['code'] = -1
        resp['msg'] = "参数为空"
        return jsonify(resp)
    photos, photo_num = Spider().get_movie_photo(id, type, start, sort)
    if len(photos) > 0:
        temp = {
            'id': id,
            'photos': photos,
            'start': start,
            'sort': sort,
            'total': photo_num,
        }
        resp['data'] = temp
    else:
        resp['code'] = -1
        resp['msg'] = "数据为空"
    return jsonify(resp)


'''获取电影演职员'''


@douban.route('/movie/cast', methods=["GET"])
def get_movie_cast():
    resp = {'code': 200, 'msg': '获取成功', 'data': {}}
    req = request.values
    id = req['id'] if 'id' in req else ''
    if id is None or len(id) < 1:
        resp['code'] = -1
        resp['msg'] = "ID为空"
        return jsonify(resp)
    casts = Spider().get_movie_cast(id)
    if len(casts) > 0:
        temp = {
            'id': id,
            'casts': casts
        }
        resp['data'] = temp
    else:
        resp['code'] = -1
        resp['msg'] = "数据为空"
    return jsonify(resp)


'''获取电影获奖信息'''


@douban.route('/movie/awards', methods=["GET"])
def get_movie_awards():
    resp = {'code': 200, 'msg': '获取成功', 'data': {}}
    req = request.values
    id = req['id'] if 'id' in req else ''
    if id is None or len(id) < 1:
        resp['code'] = -1
        resp['msg'] = "ID为空"
        return jsonify(resp)
    awards = Spider().get_movie_awards(id)
    if len(awards) > 0:
        temp = {
            'id': id,
            'awards': awards
        }
        resp['data'] = temp
    else:
        resp['code'] = -1
        resp['msg'] = "数据为空"
    return jsonify(resp)


'''获取电影额外信息'''


@douban.route('/movie/extra', methods=["GET"])
def get_movie_extra():
    # 此处删改只保留了pt_info
    resp = {'code': 200, 'msg': '获取成功', 'data': {}}
    req = request.values
    id = req['id'] if 'id' in req else ''
    field = req['field'] if 'field' in req else ''
    if id is None or len(id) < 1:
        resp['code'] = -1
        resp['msg'] = "ID为空"
        return jsonify(resp)
    if field is None or len(field) < 1:
        resp['code'] = -1
        resp['msg'] = "参数为空"
        return jsonify(resp)
    if field not in ['pt_info']:
        resp['code'] = -1
        resp['msg'] = "参数错误"
        return jsonify(resp)

    base_data, extra_data = Spider().get_movieinfo(id)
    if len(base_data) > 2:
        resp['data'] = extra_data
    else:
        resp['code'] = -1
        resp['msg'] = '内部错误或数据为空'

    return jsonify(resp)


'''获取影人信息'''


@douban.route('/person', methods=["GET"])
def get_person():
    resp = {'code': 200, 'msg': '获取成功', 'data': {}}
    req = request.values
    id = req['id'] if 'id' in req else ''
    if id is None or len(id) < 1:
        resp['code'] = -1
        resp['msg'] = "ID为空"
        return jsonify(resp)

    data = Spider().get_personinfo(id)
    if data:
        resp['data'] = data
    else:
        resp['code'] = -1
        resp['msg'] = "内部错误或数据为空"

    return jsonify(resp)


'''获取影人图片'''


@douban.route('/person/pic', methods=["GET"])
def get_person_photo():
    resp = {'code': 200, 'msg': '获取成功', 'data': {}}
    req = request.values
    id = req['id'] if 'id' in req else ''
    sort = req['sort'] if 'sort' in req and req['sort'] in ['like', 'size', 'time'] else 'like'
    start = int(req['start'] if 'start' in req and len(req['start']) > 0 else 0)
    if id is None or len(id) < 1:
        resp['code'] = -1
        resp['msg'] = "ID为空"
        return jsonify(resp)
    photos, photo_num = Spider().get_person_photo(id, start, sort)
    if len(photos) > 0:
        temp = {
            'id': id,
            'photos': photos,
            'start': start,
            'sort': sort,
            'total': photo_num,
        }
        resp['data'] = temp
    else:
        resp['code'] = -1
        resp['msg'] = "数据为空"
    return jsonify(resp)


'''获取影人作品'''


@douban.route('/person/work', methods=["GET"])
def get_person_work():
    resp = {'code': 200, 'msg': '获取成功', 'data': {}}
    req = request.values
    id = req['id'] if 'id' in req else ''
    sort = req['sort'] if 'sort' in req and req['sort'] in ['time', 'vote'] else 'time'
    start = int(req['start'] if 'start' in req and len(req['start']) > 0 else 0)
    if id is None or len(id) < 1:
        resp['code'] = -1
        resp['msg'] = "ID为空"
        return jsonify(resp)
    works, work_num = Spider().get_person_work(id, start, sort)
    if len(works) > 0:
        temp = {
            'id': id,
            'works': works,
            'start': start,
            'sort': sort,
            'total': work_num,
        }
        resp['data'] = temp
    else:
        resp['code'] = -1
        resp['msg'] = "数据为空"
    return jsonify(resp)

@douban.route('/book/wish', methods=["GET"])
def get_book_wish():
    resp = {'code': 200, 'msg': '获取成功', 'data': {}}
    req = request.values
    start = req['start'] if 'start' in req else 0
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
    return jsonify(resp)