# README
## Getting Started
```

deploy
pip install -r requirement.txt
pip install -r test-requirement.txt
python setup.py develop

initdb: python setup.py initdb
Run server: python setup.py runapp

```

## APIs
API | 方法 | URL
---- |----- | -----
使用者登入 | POST | /login
使用者清單 | GET | /users
傳送訊息 | POST | /msgs
取得訊息 | GET | /msgs


### 使用者登入 [POST] /login

#### 參數
名稱 | 型態 | 說明
---- |----- | -----
user_name | string | user's account
password | string | user's password

#### 回應
```
{
    "data": {
        "access_token": "9zyp6UMdvxi6mFcNmgm2XM",
        "avatar": "http://z.m.ipimg.com/-150c-/5/3/5/D/8/5/1/6/535D851628FEF4E797362755F02E7194.jpg",
        "create_at": "2015-04-17 12:45:15.884010",
        "updated_at": "2015-04-17 13:47:27.320351",
        "user_name": "admin"
    },
    "status": 1
}
```


### 使用者清單 [GET] /users

#### 參數
名稱 | 型態 | 說明
---- |----- | -----
access_token | string | 自己的access token

#### 回應
```
{
    "data": [
        {
            "avatar": "http://z.m.ipimg.com/-150c-/5/3/5/D/8/5/1/6/535D851628FEF4E797362755F02E7194.jpg",
            "updated_at": "Fri, 17 Apr 2015 13:49:12 GMT",
            "user_name": "admin"
        },
        {
            "avatar": "",
            "updated_at": "Fri, 17 Apr 2015 13:07:14 GMT",
            "user_name": "test_user0"
        },
        {
            "avatar": "",
            "updated_at": "Fri, 17 Apr 2015 13:07:14 GMT",
            "user_name": "test_user1"
        }
    ],
    "status": 1
}
```


### 傳送訊息 [POST] /msgs

#### 參數
名稱 | 型態 | 說明
---- |----- | -----
access_token | string | 自己的access token
user_name | string | 接收者user_name
msg | string | 訊息

#### 回應
```
{
    "data": [
        {
            "channel_guid": "CU6zqc5MYMuB5ghT8awcEef",
            "created_at": "Fri, 17 Apr 2015 13:30:04 GMT",
            "guid": "MU73vpG5Z4qTWKhquqn5u95",
            "msg": "fuck fuck fuck",
            "user_guid": "USKs7pozenwxXSo6e8nBk9jy"
        },
        {
            "channel_guid": "CU6zqc5MYMuB5ghT8awcEef",
            "created_at": "Fri, 17 Apr 2015 13:30:11 GMT",
            "guid": "MUdEogH21srAcnwtQgBvy6B",
            "msg": "fuck fuck fuck fuck",
            "user_guid": "USKs7pozenwxXSo6e8nBk9jy"
        }
    ],
    "status": 1
}
```

### 取得聊天訊息 [GET] /msgs

#### 參數
名稱 | 型態 | 說明
---- |----- | -----
access_token | string | 自己的access token

user_name | string | 接收者user_name

ts | int | 時間戳記, optional

limit | int | 筆數, optional, default=10

#### 回應

```
{
    "data": [
        {
            "channel_guid": "CU6zqc5MYMuB5ghT8awcEef",
            "created_at": "Fri, 17 Apr 2015 13:30:04 GMT",
            "guid": "MU73vpG5Z4qTWKhquqn5u95",
            "msg": "fuck fuck fuck",
            "user_guid": "USKs7pozenwxXSo6e8nBk9jy"
        },
        {
            "channel_guid": "CU6zqc5MYMuB5ghT8awcEef",
            "created_at": "Fri, 17 Apr 2015 13:30:11 GMT",
            "guid": "MUdEogH21srAcnwtQgBvy6B",
            "msg": "fuck fuck fuck fuck",
            "user_guid": "USKs7pozenwxXSo6e8nBk9jy"
        }
    ],
    "status": 1
}
```
