# -*- coding: utf-8 -*-
# @Author  : Yuncong
# @Email   : yuncongzt@163.com

import json
import random
import requests
from pyquery import PyQuery as pq

from application import app
from common.Helper import *

headers = app.config['HEADERS']
domain = app.config['DOUBAN']

ips = app.config['PROXIES']
proxies = {}
if len(ips) > 0:
    ip = random.choice(ips)
    proxies = {
        "http": "http://{}".format(ip),
        "https": "http://{}".format(ip)
    }

"""
    豆瓣数据爬取
"""


class Spider(object):

    @staticmethod
    def get_hot(type):
        """
        获取豆瓣热门影视
        :param type: 类型 movie为电影 tv为剧集
        :return: 电影列表
        """
        url = '{}/j/search_subjects?type={}&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=40&page_start=0'.format(
            domain, type)
        req = requests.get(url, headers=headers, proxies=proxies, timeout=10)
        m = []
        if req.status_code == 200:
            data = json.loads(req.text)
            no = 0
            for item in data['subjects']:
                no = no + 1
                res = {
                    'no': no,
                    'id': item['id'],
                    'title': item['title'],
                    'poster': replace_img(item['cover']),
                    'average': float(item['rate']) if len(item['rate']) > 0 else 0.0,
                    'stars': get_stars(item['rate'])
                }
                m.append(res)
            return m
        else:
            return False

    @staticmethod
    def get_nowplaying():
        """
        获取正在上映的电影（默认地区北京）
        :return: 电影列表
        """
        url = '{}/cinema/nowplaying/beijing/'.format(domain)
        req = requests.get(url, headers=headers, proxies=proxies, timeout=10)
        m = []
        if req.status_code == 200:
            doc = pq(req.text)
            items = doc('#nowplaying .lists li.list-item').items()
            no = 0
            for item in items:
                no = no + 1
                mo = pq(item)
                id = mo('li.list-item').attr('id')
                title = mo('li.list-item').attr('data-title')
                average = mo('li.list-item').attr('data-score')
                stars = mo('li.list-item').attr('data-star')
                poster = mo('.poster a img').attr('src')
                res = {
                    'no': no,
                    'id': id,
                    'title': title,
                    'poster': replace_img(poster),
                    'average': float(average) if len(average) > 0 else 0.0,
                    'stars': stars
                }
                m.append(res)
            return m
        else:
            return False

    @staticmethod
    def get_later():
        """
        获取即将上映的电影
        :return: 电影列表
        """
        url = '{}/cinema/later/beijing/'.format(domain)
        req = requests.get(url, headers=headers, proxies=proxies, timeout=10)
        m = []
        if req.status_code == 200:
            doc = pq(req.text)
            items = doc('#showing-soon div.item').items()
            no = 0
            for item in items:
                no = no + 1
                mo = pq(item)
                href = mo('.intro h3 a').attr('href')
                title = mo('.intro h3 a').text()
                poster = mo('.thumb img').attr('src')
                res = {
                    'no': no,
                    'id': get_id(href),
                    'title': title,
                    'poster': replace_img(poster),
                    'average': 0.0,
                    'stars': 00
                }
                m.append(res)
            return m
        else:
            return False

    @staticmethod
    def get_top250(start):
        """
        获取豆瓣电影TOP250
        :param start: 开始节点 *25
        :return: 电影列表
        """
        url = '{}/top250?start={}'.format(domain, start)
        req = requests.get(url, headers=headers, proxies=proxies, timeout=10)
        m = []
        if req.status_code == 200:
            doc = pq(req.text)
            items = doc('.article > ol > li').items()
            for item in items:
                no = pq(item)('.pic em').text()
                href = pq(item)('.pic a').attr('href')
                title = pq(item)('.pic a img').attr('alt')
                poster = pq(item)('.pic a img').attr('src')
                average = pq(item)('.info .star .rating_num').text()
                res = {
                    'no': int(no),
                    'id': get_id(href),
                    'title': title,
                    'poster': replace_img(poster),
                    'average': float(average) if len(average) > 0 else 0.0,
                    'stars': get_stars(average) if len(average) > 0 else '00'
                }
                m.append(res)
            return m
        else:
            return False

    def get_movieinfo(self, id):
        url = '{}/subject/{}/'.format(domain, id)
        req = requests.get(url, headers=headers, proxies=proxies)
        if req.status_code == 200:
            doc = pq(req.text)
            try:
                photos, photo_num = self.get_movie_photo(id, 'S', 0, 'like')
            except Exception as ex:
                # 保存错误日志去除
                photos, photo_num = [], 0
            try:
                awards = self.get_movie_awards(id)
            except Exception as ex:
                awards = []

            # 通过script
            sc = doc('head [type="application/ld+json"]').text()
            json_data = json.loads(sc)
            type = json_data['@type']
            director = json_data['director']
            author = json_data['author']
            actor = json_data['actor']
            di = []
            au = []
            ac = []
            mac = []
            for i in director:
                di.append(i['name'])
            for i in author:
                au.append(i['name'])
            for i in actor:
                ac.append(i['name'])
                mac.append(str(i['name']).split(' ')[0])
            main_cast = '/'.join(mac[0:4]) if len(mac) >= 4 else '/'.join(mac)
            alt = '{}/subject/{}/'.format(domain, id)
            main_title = doc('[property="v:itemreviewed"]').text()
            alt_title = doc('#mainpic > a > img').attr('alt')
            year = doc('#content > h1 > .year').text()
            poster = doc('#mainpic > a > img').attr('src')
            head_title = replace_null(doc('head title').text(), [' (豆瓣)'])
            infos = doc('#info').text().split('\n')
            genres = []
            durations = []
            countries = []
            languages = []
            pubdates = []
            aka_title = []
            imdb_id = episodes = ''
            for i in infos:
                kv = str(i).split(': ')
                if kv[0] == '类型':
                    genres = split_a(kv[1])
                elif kv[0] == '制片国家/地区':
                    countries = split_a(kv[1])
                elif kv[0] == '语言':
                    languages = split_a(kv[1])
                elif kv[0] == '上映日期' or kv[0] == '首播':
                    pubdates = split_a(kv[1])
                elif kv[0] == '片长' or kv[0] == '单集片长':
                    durations = split_a(kv[1])
                elif kv[0] == '又名':
                    aka_title = split_a(kv[1])
                elif kv[0] == 'IMDb链接':
                    imdb_id = kv[1]
                elif kv[0] == '集数':
                    episodes = kv[1]

            summary = doc('[property="v:summary"]').text()
            summary_all = doc('#link-report > span.all').text()
            summary = summary_all if len(summary_all) > 0 else summary
            celebrities_all = str(doc('#celebrities h2 a').text()).split(' ')
            celebrities_num = int(celebrities_all[1]) if len(celebrities_all) > 1 else 0
            celebrities = doc('#celebrities .celebrities-list li').items()
            celebrities_f = []
            for ce in celebrities:
                if str(ce).find('fake') > 0:
                    break
                c_href = pq(ce)('.info .name a').attr('href')
                c_name = pq(ce)('.info .name a').text()
                c_avatar = replace_null(pq(ce)('.avatar').attr('style'), ['background-image: url(', ')', 'url(']).split(
                    ',')
                c_role = pq(ce)('.info .role').text()
                res = {
                    'id': get_id(c_href),
                    'name': c_name,
                    'avatar': replace_img(c_avatar[-1]),
                    'role': c_role,
                }
                celebrities_f.append(res)
            recommendations = doc('#recommendations .recommendations-bd dl').items()
            recommend = []
            for r in recommendations:
                r_href = pq(r)('dt a').attr('href')
                r_title = pq(r)('dt a img').attr('alt')
                r_poster = pq(r)('dt a img').attr('src')
                res = {
                    'id': get_id(r_href),
                    'title': r_title,
                    'poster': r_poster,
                    'average': '',
                    'stars': '',
                }
                recommend.append(res)

            tag = doc('#content .tags .tags-body').text()
            tags = str(tag).split(' ') if len(tag) > 0 else []
            average = doc('[property="v:average"]').text()
            votes = doc('[property="v:votes"]').text()
            star_detail = [0, 0, 0, 0, 0]
            ratings = doc('.ratings-on-weight .item .rating_per').text()
            ratings_a = str(ratings).split(' ') if len(ratings) > 0 else star_detail
            for i in range(5):
                star_detail[i] = float(replace_null(ratings_a[i], ['%']))
            rating_count = int(votes) if len(votes) > 0 else 0
            watching_count = collect_count = wish_count = 0
            counts = str(doc('#subject-others-interests .subject-others-interests-ft').text()).split('  /  ')
            for c in counts:
                if '人' not in c:
                    break
                kv = str(c).split('人')
                if kv[1] == '在看':
                    watching_count = int(kv[0])
                if kv[1] == '看过':
                    collect_count = int(kv[0])
                if kv[1] == '想看':
                    wish_count = int(kv[0])
            # titles = str(main_title).split(' ', 1)
            yearn = replace_null(year, ['(', ')'])
            year = int(yearn) if len(yearn) > 0 else 0
            awards_str = '\n'
            for a in awards:
                awards_str = awards_str + '\n　　' + a['name'] + '\n　　' + '\n　　'.join(a['list']) + '\n'
            awards_f = '◎获奖情况  ' + awards_str if len(awards) > 0 else ''

            pt_info = '[img]' + poster + '[/img]\n\n' + \
                      '◎译　　名　' + head_title + '/' + '/'.join(aka_title) + '\n' + \
                      '◎片　　名　' + alt_title + '\n' + \
                      '◎年　　代　' + str(year) + '\n' + \
                      '◎类　　型　' + '/'.join(genres) + '\n' + \
                      '◎产　　地　' + '/'.join(countries) + '\n' + \
                      '◎语　　言　' + '/'.join(languages) + '\n' + \
                      '◎片　　长　' + '/'.join(durations) + '\n' + \
                      '◎上映日期　' + '/'.join(pubdates) + '\n' + \
                      '◎IMDb链接　' + 'https://www.imdb.com/title/{}/'.format(imdb_id) + '\n' + \
                      '◎豆瓣评分　' + '{}/10 from {} users\n'.format(average, rating_count) + \
                      '◎豆瓣链接　' + alt + '\n' + \
                      '◎导　　演　' + ' / '.join(di) + '\n' + \
                      '◎编　　剧　' + ' / '.join(au) + '\n' + \
                      '◎主　　演　' + '\n　　　　　　'.join(ac) + '\n\n' + \
                      '◎标　　签　' + ' | '.join(tags) + '\n\n' + \
                      '◎简　　介  \n\n　　' + summary + '\n\n' + awards_f

            en_title = aka_title[-1] if len(aka_title) > 0 else ''
            sec_t = replace_null(main_title, [head_title]).strip()
            base_data = {
                'id': id,
                'type': type,
                'title': head_title,
                'org_title': sec_t if len(sec_t) >= 2 else en_title,
                'aka_title': aka_title,
                'alt': alt,
                'year': year,
                'poster': replace_img(poster),
                'summary': summary,
                'genres': genres,
                'durations': durations,
                'countries': countries,
                'languages': languages,
                'pubdates': pubdates,
                'imdb_id': imdb_id,
                'imdb_score': '',
                'episodes': episodes,
                'average': float(average) if len(average) > 0 else 0.0,
                'stars': get_stars(average) if len(average) > 0 else '00',
                'star_detail': star_detail,
                'rating_count': rating_count,
                'wish_count': wish_count,
                'watching_count': watching_count,
                'collect_count': collect_count,
                'photo_num': photo_num,
                'photos': photos,
                'celebrities_num': celebrities_num,
                'celebrities': celebrities_f,
                'casts': main_cast,
                'tags': tags,
                'director': di,
                'author': au,
                'actor': ac,
                'recommend': recommend
            }
            extra_data = {
                'id': id,
                'pt_info': pt_info,
            }

            return base_data, extra_data
        else:
            return {}, {}

    @staticmethod
    def get_movie_photo(id, type, start, sort):
        """
        获取电影剧照图片
        :param id: 豆瓣电影id
        :param type: 图片类型 剧照S，海报R
        :param start: 开始节点 一般*30
        :param sort: 排序方式 喜欢like，尺寸size，时间time
        :return: 图片链接列表和图片总数
        """
        url = '{}/subject/{}/photos?type={}&start={}&sortby={}'.format(domain, id, type, start, sort)
        req = requests.get(url, headers=headers, proxies=proxies, timeout=10)
        p = []
        if req.status_code == 200:
            doc = pq(req.text)
            count = doc('.article > .paginator > .count').text()
            total = replace_null(count, ['(共', '张)'])
            items = doc('.article > ul > li').items()
            for item in items:
                src = pq(item)('.cover a img').attr('src')
                p.append(replace_img(src))
            total = int(total) if len(total) > 0 else 0
            return p, total
        else:
            return [], 0

    @staticmethod
    def get_movie_cast(id):
        """
        获取影片演职员表
        :param id: 豆瓣电影id
        :return: 演职员信息
        """
        url = '{}/subject/{}/celebrities'.format(domain, id)
        req = requests.get(url, headers=headers, proxies=proxies, timeout=10)
        ca = []
        if req.status_code == 200:
            doc = pq(req.text)
            items = doc('.article .list-wrapper').items()
            for item in items:
                rolename = pq(item)('h2').text()
                celebrities = pq(item)('.celebrities-list .celebrity').items()
                c = []
                for ce in celebrities:
                    avatar = replace_null(pq(ce)('.avatar').attr('style'), ['background-image: url(', ')'])
                    name = pq(ce)('.info .name a').text()
                    href = pq(ce)('.info .name a').attr('href')
                    role = pq(ce)('.info .role').text()
                    res = {
                        'id': get_id(href),
                        'name': name,
                        'avatar': replace_img(avatar),
                        'role': role,
                    }
                    c.append(res)
                f = {
                    'role': rolename,
                    'celebrities': c
                }
                ca.append(f)
            return ca
        else:
            return []

    @staticmethod
    def get_movie_awards(id):
        """
        获取影片获奖情况
        :param id: 豆瓣电影id
        :return: 获取列表
        """
        url = '{}/subject/{}/awards/'.format(domain, id)
        req = requests.get(url, headers=headers, proxies=proxies, timeout=10)
        a = []
        if req.status_code == 200:
            doc = pq(req.text)
            items = doc('.article > .awards').items()
            for item in items:
                awardname = pq(item)('.hd h2').text()
                award = pq(item)('.award').items()
                aw = []
                for i in award:
                    name = str(pq(i).text()).replace('\n', ' ')
                    aw.append(name)
                res = {
                    'name': replace_null(awardname, ['  ']),
                    'list': aw
                }
                a.append(res)
            return a
        else:
            return []

    def get_personinfo(self, id):
        """
        获取影人基本信息
        :param id: 豆瓣影人id
        :return: 影人信息
        """
        url = '{}/celebrity/{}/'.format(domain, id)
        req = requests.get(url, headers=headers, proxies=proxies, timeout=10)
        if req.status_code == 200:
            doc = pq(req.text)
            avatar = doc('#headline > div.pic > a > img').attr('src')
            name = doc('#content > h1').text()
            infos = str(doc('#headline .info ul').text()).split('\n')
            gender = constellation = birthday = born_place = imdb_id = ''
            profession = []
            for i in infos:
                kv = str(i).split(': ')
                if kv[0] == '性别':
                    gender = kv[1]
                elif kv[0] == '星座':
                    constellation = kv[1]
                elif kv[0] == '出生日期':
                    birthday = kv[1]
                elif kv[0] == '生卒日期':
                    birthday = str(kv[1]).split(' ')[0]
                elif kv[0] == '出生地':
                    born_place = kv[1]
                elif kv[0] == '职业':
                    profession = split_a(kv[1])
                elif kv[0] == 'imdb编号':
                    imdb_id = kv[1]
            summary = doc('#intro > div.bd').text()
            summary_all = doc('#intro > div.bd > .all').text()
            summary = summary_all if len(summary_all) > 0 else summary
            partners = doc('#partners > .bd > ul > li').items()
            pa = []
            for item in partners:
                p_href = pq(item)('.pic a').attr('href')
                p_name = pq(item)('.pic a img').attr('alt')
                p_avatar = pq(item)('.pic a img').attr('src')
                p = {
                    'id': get_id(p_href),
                    'name': p_name,
                    'avatar': replace_img(p_avatar)
                }
                pa.append(p)
            try:
                works, work_num = self.get_person_work(id, 0, 'time')
            except Exception as ex:
                works, work_num = [], 0
            try:
                photos, photo_num = self.get_person_photo(id, 0, 'like')
            except Exception as ex:
                photos, photo_num = [], 0
            if check_cn(name):
                name = str(name).split(' ', 1)
            data = {
                'id': id,
                'name': name[0],
                'name_en': name[1] if len(name) > 1 else 'None',
                'avatar': replace_img(avatar),
                'gender': gender,
                'birthday': birthday,
                'born_place': born_place,
                'constellation': constellation,
                'profession': profession,
                'imdb_id': imdb_id,
                'summary': summary,
                'photos': photos,
                'photo_num': photo_num,
                'works': works,
                'work_num': work_num,
                'partners': pa
            }
            return data
        else:
            return False

    @staticmethod
    def get_person_photo(id, start, sort):
        """
        获取电影剧照图片
        :param id: 豆瓣影人id
        :param start: 开始节点 一般*30
        :param sort: 排序方式 喜欢like，尺寸size，时间time
        :return: 图片链接列表和图片总数
        """
        url = '{}/celebrity/{}/photos/?type=C&start={}&sortby={}'.format(domain, id, start, sort)
        req = requests.get(url, headers=headers, proxies=proxies, timeout=10)
        p = []
        if req.status_code == 200:
            doc = pq(req.text)
            count = doc('.article > .paginator > .count').text()
            total = replace_null(count, ['(共', '张)'])
            items = doc('.article > ul > li').items()
            for item in items:
                src = pq(item)('.cover a img').attr('src')
                p.append(replace_img(src))
            total = int(total) if len(total) > 0 else 0
            return p, total
        else:
            return [], 0

    @staticmethod
    def get_person_work(id, start, sort):
        """
        获取影人作品
        :param id: 豆瓣影人id
        :param start: 开始节点 *10
        :param sort: 排序方式 按时间time,按评价vote
        :return: 作品列表和作品总数
        """
        url = '{}/celebrity/{}/movies?start={}&sortby={}&format=pic'.format(domain, id, start, sort)
        req = requests.get(url, headers=headers, proxies=proxies, timeout=10)
        m = []
        if req.status_code == 200:
            doc = pq(req.text)
            count = doc('.article > .paginator > .count').text()
            total = replace_null(count, ['(共', '条)'])
            items = doc('.article > .grid_view > ul > li').items()
            for item in items:
                href = pq(item)('dd h6 a').attr('href')
                title = pq(item)('dd h6 a').text()
                poster = pq(item)('.nbg img').attr('src')
                average = pq(item)('dd .star span:nth-child(2)').text()
                res = {
                    'id': get_id(href),
                    'title': title,
                    'poster': replace_img(poster),
                    'average': float(average) if len(average) > 0 else 0.0,
                    'stars': get_stars(average) if len(average) > 0 else '00',
                }
                m.append(res)
            total = int(total) if len(total) > 0 else 0
            return m, total
        else:
            return [], 0
