# 通过Python爬虫自建豆瓣电影API

## 项目简介
 ##### 在开发微信小程序「影库MDb」时，使用了豆瓣api来获取电影信息，后来由于豆瓣apikey失效了，小程序就无法正常访问，而个人主体貌似无法申请官方apikey，所以自己抽时间通过爬虫的方式写了个电影接口。这里把项目中的电影接口部分单独提取出来，分享给有需要的朋友。 
 ##### 本项目使用Python Flask框架搭建，采用爬取豆瓣官网的方式，获取并处理电影信息，返回的Json数据，便于小程序使用。
 ##### 主要实现的功能有获取电影列表，获取电影信息、图片、演员等，以及获取影人信息、图片、作品，具体可参考api文档。
 
## 开发技术
 * 编程语言：Python 3.7
 * WEB框架：Flask
 * WSGI服务器：Waitress
 
 ## 使用方法
 ##### 先部署环境，安装依赖。
    pip install -r requirements.txt
 ##### 直接运行run.py即可，我设置的5000端口，可改为其它，部署后可通过nginx来代理。
    python run.py
 ##### 成功运行之后可以通过 `http://localhost:5000+对应URL和参数` 来获取数据，URL和参数详见API文档。
 
 ##### 不建议直接部署使用，因为每次请求都要现爬取并处理数据，占用资源，响应比较慢，并且爬虫受限。可以在此基础上进行开发，将数据保存到本地数据库，然后定期更新数据。如果要部署使用，建议在config目录的配置文件里的HEADERS和PROXIES加上对应配置，来解决豆瓣爬虫限制。
 
## 使用建议
 - 豆瓣官网有反爬机制，单ip有访问限制，所以建议增加ip代理池。
 - 部分影视不登录豆瓣账号无法查看信息，所以建议增加cookie。
 - 建议将爬取处理好的数据保存到本地数据库（推荐mongodb），处理逻辑是：访问接口->查询本地数据库->有返回数据，没有现爬数据并存储。
 - 如果将数据存到本地，电影的一些数据会变化，建议添加个时间字段，用于定期更新数据。
 - 由于我是在Windows服务器运行，使用的是Waitress，Linux建议更换其它WSGI服务器。

------------

# API文档

### 文档说明

- 接口固定返回格式如下，以下‘返回参数说明’中只含data中的参数

```  
  {
    "code": 200, // 响应状态码
    "data": {}, // 数据
    "msg": "成功" // 状态提示
  }
```
- 返回示例中的数据仅截取部分，非完整数据

------------

### 1. 电影列表
    
##### 简要描述

- 获取电影列表，包括正在热映、即将上映、热门电影、热门电视、豆瓣TOP250
- 请求参数中的listname可选值为：nowplaying、later、hotmovie、hottv、top250，分别对应上面5个列表

##### 请求URL
- ` /api/douban/list `
  
##### 请求方式
- GET 

##### 参数

|参数名|必选|类型|说明|
|:----    |:---|:----- |-----|
|listname |是  |string |列表名   |
|start |否  |int | 起点，默认为0  |


##### 返回示例 

``` 
  {
    "code": 200,
    "data": {
        "count": 25,
        "list": [
            {
                "average": 9.7,
                "id": "1292052",
                "no": 1,
                "poster": "https://img2.doubanio.com/view/photo/s_ratio_poster/public/p480747492.jpg",
                "stars": "50",
                "title": "肖申克的救赎"
            },
            {
                "average": 9.6,
                "id": "1291546",
                "no": 2,
                "poster": "https://img3.doubanio.com/view/photo/s_ratio_poster/public/p2561716440.jpg",
                "stars": "50",
                "title": "霸王别姬"
            },
            ...
        ],
        "listname": "top250",
        "start": 0
    },
    "msg": "获取成功"
}
```

##### 返回参数说明 

|参数名|类型|说明|
|:-----  |:-----|-----|
|list  |array |电影列表  |
|listname  |string |当前列表名 |
|start |int   |当前起点  |
|total |int   |该列表总数  |


##### 备注 

- 本为从本地数据库获取，改直接爬取后，start参数只对top250有效，且*25

------------

### 2.1 电影基本信息
    
##### 简要描述

- 获取电影基本信息

##### 请求URL
- ` /api/douban/movie `
  
##### 请求方式
- GET 

##### 参数

|参数名|必选|类型|说明|
|:----    |:---|:----- |-----|
|id |是  |string |电影id   |


##### 返回示例 

``` 
  {
    "code": 200,
    "data": {
        "actor": [
            "蒂姆·罗宾斯 Tim Robbins",
            "摩根·弗里曼 Morgan Freeman",
            ...
        ],
        "aka_title": [
            "月黑高飞(港)",
            "刺激1995(台)",
            "地狱诺言",
            "铁窗岁月",
            "消香克的救赎"
        ],
        "alt": "https://movie.douban.com/subject/1292052/",
        "author": [
            "弗兰克·德拉邦特 Frank Darabont",
            "斯蒂芬·金 Stephen King"
        ],
        "average": 9.7,
        "casts": "蒂姆·罗宾斯/摩根·弗里曼/鲍勃·冈顿/威廉姆·赛德勒",
        "celebrities": [
            {
                "avatar": "https://img3.doubanio.com/view/celebrity/s_ratio_celebrity/public/p230.jpg",
                "id": "1047973",
                "name": "弗兰克·德拉邦特",
                "role": "导演"
            },
            {
                "avatar": "https://img9.doubanio.com/view/celebrity/s_ratio_celebrity/public/p17525.jpg",
                "id": "1054521",
                "name": "蒂姆·罗宾斯",
                "role": "饰 安迪·杜佛兰 Andy Dufresne"
            },
            ...
        ],
        "celebrities_num": 43,
        "collect_count": 3517566,
        "countries": [
            "美国"
        ],
        "director": [
            "弗兰克·德拉邦特 Frank Darabont"
        ],
        "durations": [
            "142分钟"
        ],
        "episodes": "",
        "genres": [
            "剧情",
            "犯罪"
        ],
        "id": "1292052",
        "imdb_id": "tt0111161",
        "imdb_score": "",
        "languages": [
            "英语"
        ],
        "org_title": "The Shawshank Redemption",
        "photo_num": 771,
        "photos": [
            "https://img2.doubanio.com/view/photo/m/public/p2561714803.jpg",
            "https://img9.doubanio.com/view/photo/m/public/p2309770674.jpg",
            "https://img3.doubanio.com/view/photo/m/public/p456482220.jpg",
            ...
        ],
        "poster": "https://img2.doubanio.com/view/photo/s_ratio_poster/public/p480747492.jpg",
        "pubdates": [
            "1994-09-10(多伦多电影节)",
            "1994-10-14(美国)"
        ],
        "rating_count": 2308132,
        "recommend": [
            {
                "average": "",
                "id": "1292720",
                "poster": "https://img2.doubanio.com/view/photo/s_ratio_poster/public/p2372307693.webp",
                "stars": "",
                "title": "阿甘正传"
            },
            {
                "average": "",
                "id": "1849031",
                "poster": "https://img9.doubanio.com/view/photo/s_ratio_poster/public/p2614359276.webp",
                "stars": "",
                "title": "当幸福来敲门"
            },
            ...
        ],
        "star_detail": [
            85.4,
            13.2,
            1.3,
            0.1,
            0.1
        ],
        "stars": "50",
        "summary": "一场谋杀案使银行家安迪（蒂姆•罗宾斯 Tim Robbins 饰）蒙冤入狱，谋杀妻子及其情人的指控将囚禁他终生。在肖申克监狱的首次现身就让监狱“大哥”瑞德（摩根•弗里曼 Morgan Freeman 饰）对他另眼相看...",
        "tags": [
            "经典",
            "励志",
             ...
        ],
        "title": "肖申克的救赎",
        "type": "Movie",
        "watching_count": 0,
        "wish_count": 361551,
        "year": 1994
    },
    "msg": "获取成功"
}
```

##### 返回参数说明 

|参数名|类型|说明|
|:-----  |:-----|-----|
|id |string   |电影id |
|type |string   |类型，电影/剧集 |
|title |string   |中文名 |
|org_title |string   |原名 |
|aka_title |array   |其它译名 |
|alt |string   |豆瓣链接 |
|year |int   |年份 |
|poster |string   |海报链接 |
|summary |string   |简介 |
|genres |array   |类型 |
|durations |array   |时长 |
|countries |array   |国家 |
|languages |array   |语言 |
|pubdates |array    |上映时间 |
|imdb_id |string   |IMDB id |
|episodes |string   |集数，仅type为剧集时有 |
|average |float   |评分 |
|stars |string    |星级 |
|star_detail |array   |各星级占百分比 |
|rating_count |int   |评分人数 |
|wish_count |int   |想看人数 |
|watching_count |int  |在看人数 |
|collect_count |int   |看过人数 |
|photo_num |int   |图片总数 |
|photos |string   |电影剧照，最多30张 |
|celebrities_num |int  |演职总数 |
|celebrities |string   |主要演职，最多6位 |
|recommend |array   |相关推荐，最多10部 |
|tags |array   |电影标签 |
|director |array   |导演 |
|author |array   |编剧 |
|actor |array   |演员 |

##### 备注 

- 无


------------


### 2.2 电影演职人员

    
##### 简要描述

- 获取该电影全部演职人员

##### 请求URL
- `  /api/douban/movie/cast `
  
##### 请求方式
- GET 

##### 参数

|参数名|必选|类型|说明|
|:----    |:---|:----- |-----|
|id |是  |string |电影id   |

##### 返回示例 

``` 
 {
    "code": 200,
    "data": {
        "casts": [
            {
                "celebrities": [
                    {
                        "avatar": "https://img3.doubanio.com/view/celebrity/s_ratio_celebrity/public/p230.jpg",
                        "id": "1047973",
                        "name": "弗兰克·德拉邦特 Frank Darabont",
                        "role": "导演 Director"
                    }
                ],
                "role": "导演 Director"
            },
            {
                "celebrities": [
                    {
                        "avatar": "https://img9.doubanio.com/view/celebrity/s_ratio_celebrity/public/p17525.jpg",
                        "id": "1054521",
                        "name": "蒂姆·罗宾斯 Tim Robbins",
                        "role": "演员 Actor (饰 安迪·杜佛兰 Andy Dufresne)"
                    },
                    {
                        "avatar": "https://img3.doubanio.com/view/celebrity/s_ratio_celebrity/public/p34642.jpg",
                        "id": "1054534",
                        "name": "摩根·弗里曼 Morgan Freeman",
                        "role": "演员 Actor (饰 艾利斯·波伊德·“瑞德”·瑞丁 Ellis Boyd 'Red' Redding)"
                    },
                    ...
                ],
                "role": "演员 Cast"
            },
            ...
        ],
        "id": "1292052"
    },
    "msg": "获取成功"
}
```

##### 返回参数说明 

|参数名|类型|说明|
|:-----  |:-----|-----|
|id |string   |电影id  |
|casts |array   |演职人员数组  |
| - role |string   |职位中英名  |
| - celebrities |array   |该职位的人员信息  |
| - - id |string   | 职员豆瓣id |
| - - avatar |string   | 职员头像链接 |
| - - name |string   | 职员中/英文名 |
| - - role |string   | 扮演角色 |

##### 备注 

- 无

------------

### 2.3 电影剧照海报

    
##### 简要描述

- 获取该电影剧照和海报

##### 请求URL
- `/api/douban/movie/pic `
  
##### 请求方式
- GET

##### 参数

|参数名|必选|类型|说明|
|:----    |:---|:----- |-----|
|id |是  |string |电影id   |
|type |是  |string |图片类型：S为剧照，R为海报 |
|start|否  |int |起点 *30  |

##### 返回示例 

``` 
 {
    "code": 200,
    "data": {
        "id": "1292052",
        "photos": [
            "https://img2.doubanio.com/view/photo/m/public/p2561714803.jpg",
            "https://img9.doubanio.com/view/photo/m/public/p2309770674.jpg",
            "https://img3.doubanio.com/view/photo/m/public/p456482220.jpg",
            ...
        ],
        "start": 0,
        "total": 575
    },
    "msg": "获取成功"
}
```

##### 返回参数说明 

|参数名|类型|说明|
|:-----  |:-----|-----|
|id |string   |电影id  |
|start |int   |当前起点  |
|total |int   |图片总数  |
|photos |array   |图片链接，一次最多30张 |

##### 备注 

- 图片大小默认为中等尺寸m，原图改链接中的m为r


------------


### 2.4 电影获奖信息

    
##### 简要描述

- 获取该电影获奖信息

##### 请求URL
- `/api/douban/movie/awards `
  
##### 请求方式
- GET

##### 参数

|参数名|必选|类型|说明|
|:----    |:---|:----- |----- |
|id |是  |string |电影id   |

##### 返回示例 

``` 
 {
    "code": 200,
    "data": {
        "awards": [
            {
                "list": [
                    "最佳影片(提名) 妮基·马文",
                    "最佳男主角(提名) 摩根·弗里曼",
                    "最佳改编剧本(提名) 弗兰克·德拉邦特",
                 	...
                ],
                "name": "第67届奥斯卡金像奖(1995)"
            },
            {
                "list": [
                    "最佳外语片"
                ],
                "name": "第19届日本电影学院奖(1996)"
            },
            ...
        ],
        "id": "1292052"
    },
    "msg": "获取成功"
}
```

##### 返回参数说明 

|参数名|类型|说明|
|:-----  |:-----|-----|
|id |string  |电影id  |
|awards |array   |获奖信息  |
| - name  |string   |电影节/奖名称  |
| - list |array   |获得的奖项列表 |

##### 备注 

- 无


------------


### 2.5 电影额外信息

    
##### 简要描述

- 获取电影额外信息，这里只保留了pt_info

##### 请求URL
- `/api/douban/movie/extra `
  
##### 请求方式
- GET

##### 参数

|参数名|必选|类型|说明|
|:----    |:---|:----- |-----|
|id |是  |string |电影id   |
|field |是  |string |此处只有pt_info   |

##### 返回示例 

``` 
 {
    "code": 200,
    "data": {
        "id": "1292052",
        "pt_info": "[img]https://img2.doubanio.com/view/photo/s_ratio_poster/public/p480747492.webp[/img]\n\n◎译　　名　肖申克的救赎/月黑高飞(港)/刺激1995(台)/地狱诺言/铁窗岁月/消香克的救赎\n◎片　　名　The Shawshank Redemption\n ...太长不展示了"
    },
    "msg": "获取成功"
}

```

##### 返回参数说明 

|参数名|类型|说明|
|:-----  |:-----|-----|
|id |string  |电影id  |
|pt_info |string   |生成的PT_info |


##### 备注 

- 一般用不上


------------


### 3.1 影人基本信息

##### 简要描述

- 获取影人基本信息

##### 请求URL
- `/api/douban/person `
  
##### 请求方式
- GET

##### 参数

|参数名|必选|类型|说明|
|:----    |:---|:----- |-----   |
|id |是  |string |影人id   |

##### 返回示例 

``` 
 {
    "code": 200,
    "data": {
        "avatar": "https://img1.doubanio.com/view/celebrity/s_ratio_celebrity/public/p56339.jpg",
        "birthday": "1965-04-04",
        "born_place": "美国,纽约",
        "constellation": "白羊座",
        "gender": "男",
        "id": "1016681",
        "imdb_id": "nm0000375",
        "name": "小罗伯特·唐尼",
        "name_en": "Robert Downey Jr.",
        "partners": [
            {
                "avatar": "https://img9.doubanio.com/view/celebrity/s_ratio_celebrity/public/p15885.jpg",
                "id": "1040505",
                "name": "马克·鲁弗洛"
            },
           ...
        ],
        "photo_num": 1092,
        "photos": [
            "https://img9.doubanio.com/view/photo/m/public/p960012104.jpg",
            "https://img2.doubanio.com/view/photo/m/public/p2562580933.jpg",
            "https://img9.doubanio.com/view/photo/m/public/p737203514.jpg",
            ...
        ],
        "profession": [
            "演员",
            "制片人",
            "编剧",
            "配音"
        ],
        "summary": "小罗伯特·唐尼，美国男演员。7岁时在父亲的电影《Greaser's Palace》中饰演角色，8岁时父亲递给了他人生第一支大麻烟，10岁时全家居住在伦敦，他参加了切尔西著名的Perry House School 学习古典芭蕾。...",
        "work_num": 130,
        "works": [
            {
                "average": 0.0,
                "id": "10546745",
                "poster": "https://img3.doubanio.com/view/photo/s_ratio_poster/public/p1966199971.jpg",
                "stars": "00",
                "title": "木偶奇遇记"
            },
            {
                "average": 0.0,
                "id": "20451138",
                "poster": "https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2570486869.jpg",
                "stars": "00",
                "title": "大侦探福尔摩斯3"
            },
           ...
        ]
    },
    "msg": "获取成功"
}

```

##### 返回参数说明 

|参数名|类型|说明|
|:-----  |:-----|-----|
|id |string  |影人id  |
|name |string  |中文名  |
|name_en |string  |英文名  |
|gender |string  |性别  |
|avatar |string  |头像链接  |
|birthday |string  |出生日期  |
|born_place |string  |出生地  |
|constellation |string  |星座  |
|profession |array  |职业  |
|summary |string  |简介  |
|imdb_id |string  |IMDB id  |
|photo_num |int  |图片总数  |
|photos |array  |图片链接，最多30张  |
|work_num |int  |作品总数  |
|works |array  |最新作品，最多10部 |
|partners |array  |合作2次以上的人，最多6位 |

##### 备注 

- 暂无


------------


### 3.2 影人图片

    
##### 简要描述

- 获取影人图片

##### 请求URL
- `/api/douban/person/pic `
  
##### 请求方式
- GET

##### 参数

|参数名|必选|类型|说明|
|:----    |:---|:----- |-----|
|id |是  |string |影人id   |
|start|否  |int |起点 *30   |

##### 返回示例 

``` 
 {
    "code": 200,
    "data": {
        "id": "1016681",
        "photos": [
            "https://img9.doubanio.com/view/photo/m/public/p960012104.jpg",
            "https://img2.doubanio.com/view/photo/m/public/p2562580933.jpg",
            "https://img9.doubanio.com/view/photo/m/public/p737203514.jpg",
            ...
        ],
        "start": 0,
        "total": 1092
    },
    "msg": "获取成功"
}
```

##### 返回参数说明 

|参数名|类型|说明|
|:-----  |:-----|-----|
|id |string   |影人id  |
|start |int   |当前起点  |
|total |int   |图片总数  |
|photos |array   |图片链接，一次最多30张 |

##### 备注 

- 图片大小默认为中等尺寸m，原图改链接中的m为r


------------


### 3.3 影人作品

    
##### 简要描述

- 获取影人作品

##### 请求URL
- `/api/douban/person/work `
  
##### 请求方式
- GET

##### 参数

|参数名|必选|类型|说明|
|:----    |:---|:----- |-----|
|id |是  |string |影人id   |
|sort |否  |string |排序方式，按时间time，按评价vote|
|start|否  |int |起点 *10   |

##### 返回示例 

``` 
{
    "code": 200,
    "data": {
        "id": "1016681",
        "start": 0,
        "total": 130,
        "works": [
            {
                "average": 0.0,
                "id": "10546745",
                "poster": "https://img3.doubanio.com/view/photo/s_ratio_poster/public/p1966199971.jpg",
                "stars": "00",
                "title": "木偶奇遇记"
            },
            {
                "average": 0.0,
                "id": "20451138",
                "poster": "https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2570486869.jpg",
                "stars": "00",
                "title": "大侦探福尔摩斯3"
            },
            {
                "average": 5.9,
                "id": "27000981",
                "poster": "https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2614594787.jpg",
                "stars": "30",
                "title": "多力特的奇幻冒险"
            },
            ...
        ]
    },
    "msg": "获取成功"
}
```

##### 返回参数说明 

|参数名|类型|说明|
|:-----  |:-----|-----|
|id |string   |影人id  |
|start |int   |当前起点  |
|total |int   |作品总数  |
|works |array   |作品列表，一次最多10部 |

##### 备注 

- 无

------------

> Yuncong   
> yuncongzt@163.com   
> 2020.10  
