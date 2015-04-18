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

## 參數說明
名稱 | 型態 | 說明
---- | ---- | ----
user_name | string | 使用者帳號
password | string | 使用者密碼
display_name | string | 使用者顯示名稱
age | int | 使用者年齡 age >= 0
gender | int | 使用者性別 0:女生, 1:男生
avatar | string | 使用者大頭照網址
direct | int | 方向性, -1:往後, 1:往前
ts | int | 時間戳記
offset | int | 第N筆
limit | int | 筆數


## APIs
API | 方法 | URL
---- |----- | -----
取得API版本 | GET | /version
建立帳號 | POST | /signup
使用者登入 | POST | /login
使用者清單 | GET | /users
傳送訊息 | POST | /msgs
取得訊息 | GET | /msgs
我的聊天室頻道 | GET | /channels


### 取得API版本 [GET] /version

#### 參數

#### 回應
```
{
    "version": "0.0.1" ,
    "status": 1
}
```


### 建立帳號 [POST] /signup

#### 參數
名稱 | 型態 | 說明
---- |----- | -----
user_name | string | 
password | string | 
avatar | string | 
display_name | string | 
gender | int | 
age | int |


#### 回應
```
{
    "data": {
        "age": 18,
        "avatar": "http://www.online-image-editor.com//styles/2014/images/example_image.png",
        "created_at": "Sat, 18 Apr 2015 09:39:42 GMT",
        "display_name": "James",
        "gender": 0,
        "guid": "USTZXHaeu4eTnAk89AN6koWb",
        "user_name": "kingsman12"
    },
    "status": 1
}
```


### 使用者登入 [POST] /login

#### 參數
名稱 | 型態 | 說明
---- |----- | -----
user_name | string |
password | string | 

#### 回應
```
{
    "data": {
        "access_token": "QoiesMe4uEcFYFqLuJXfFH",
        "age": 18,
        "avatar": "http://www.online-image-editor.com//styles/2014/images/example_image.png",
        "created_at": "2015-04-18 07:56:08.867575",
        "display_name": "James",
        "gender": 0,
        "updated_at": "2015-04-18 09:39:04.945852",
        "user_name": "kingsman"
    },
    "status": 1
}
```


### 使用者清單 [GET] /users

#### 參數
名稱 | 型態 | 說明
---- |----- | -----
access_token | string | 自己的access token
offset | int | optional, 預設 = 0
limit| int | optional, 預設 = 10

#### 回應
```
{
    "data": [
        {
            "age": 18,
            "avatar": "http://www.online-image-editor.com//styles/2014/images/example_image.png",
            "display_name": "Yo",
            "gender": 1,
            "updated_at": "Sat, 18 Apr 2015 08:42:26 GMT",
            "user_name": "yoyoman"
        },
        {
            "age": 70,
            "avatar": "http://z.m.ipimg.com/-150c-/8/D/8/7/0/4/1/B/8D87041BE46F9711B4BBA88B3409C1EB.jpg",
            "display_name": "yoyo3",
            "gender": 1,
            "updated_at": "Sat, 18 Apr 2015 08:41:44 GMT",
            "user_name": "yoyo3"
        }
    ],
    "total":2,
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
    "data": {
        "channel_guid": "CDiHzTHLB687sQYcxcz1ZVD",
        "created_at": "Sat, 18 Apr 2015 10:56:21 GMT",
        "guid": "MJN4PxCCajJHgKBFhrDH7J3",
        "msg": "asdfsadfffffff",
        "user_guid": "USA8M3BSXNcG2EEJz8ZCen3M"
    },
    "status": 1
}
```

### 取得聊天訊息 [GET] /msgs

#### 參數
名稱 | 型態 | 說明
---- |----- | -----
access_token | string | 自己的access token
user_name | string | 接收者user_name
ts | int | optional
direct | int | optional, default = -1
limit | int | optional, default=10

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
    "total": 2,
    "status": 1
}
```

### 我的聊天室頻道  [GET] /channels

#### 參數
名稱 | 型態 | 說明
---- |----- | -----
access_token | string | 自己的access token

#### 回應

```
{
    "data": [
        {
            "age": 65,
            "avatar": "http://z.m.ipimg.com/-150c-/8/D/8/7/0/4/1/B/8D87041BE46F9711B4BBA88B3409C1EB.jpg",
            "created": "Sat, 18 Apr 2015 08:46:27 GMT",
            "display_name": "yoyo5",
            "channel_guid": "CDiHzTHLB687sQYcxcz1ZVD",
            "gender": 0,
            "msgs": 4,
            "user_name": "yoyo5"
        }
    ],
    "status": 1,
    "total": 1
}
```
