from __future__ import unicode_literals
from flask import Flask, request, abort, render_template
from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)

from datetime import datetime, timedelta, timezone
import threading
import csv
import os
import pymongo
import requests
import json
import configparser

#有關mongo指令的函式
import mongofunction as mf


import functions as f

import text_functions as tf

app = Flask(__name__, static_url_path='/static')
CHECKLIST = ['23:05', '23:10', '23:15', '23:20', '23:25', '23:30', '23:35', '23:40', '23:45', '23:50', '23:55', '23:59']
# CHECKLIST = [22]
# CHECKLIST = ['20:00', '20:05', '20:10', '20:15', '20:20', '20:25', '20:30', '20:35', '20:40', '20:45', '20:50', '20:55', '21:00', '23:05', '23:10', '23:15', '23:20', '23:25', '23:30', '23:35', '23:40', '23:45', '23:50', '23:55', '22:00']

USERID_TRADER_PARTNER = f.getusertraderpartner()
print(USERID_TRADER_PARTNER)
config = configparser.ConfigParser()
config.read('config.ini')

configuration = Configuration(access_token=config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))

username = config.get('mongodb', 'username')
password = config.get('mongodb', 'password')
hostlocation = config.get('mongodb', 'hostlocation')
# myclient = pymongo.MongoClient("mongodb://localhost:27017/")
cluster_url =f"mongodb+srv://{username}:{password}@{hostlocation}/?retryWrites=true&w=majority&appName=GueiMing"
myclient = pymongo.MongoClient(cluster_url, username=username,password=password)




HEADER = {
    'Content-type': 'application/json',
    'Authorization': F'Bearer {config.get("line-bot", "channel_access_token")}'
}

userids = ['developer1', 'developer2']

'''利用Line api 中 reply分類作為機器人回覆功能的主要函式'''
def replyMessage(payload):
    url='https://api.line.me/v2/bot/message/reply'
    response = requests.post(url,headers=HEADER,json=payload)
    
    print(response.status_code)
    print(response.text)
    return 'OK'



@app.route("/callback", methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        return 'ok'
    body = request.json
    events = body["events"]
    if request.method == 'POST' and len(events) == 0:
        return 'ok'
    print(body)
    if "replyToken" in events[0]:
        payload = dict()
        replyToken = events[0]["replyToken"]
        payload["replyToken"] = replyToken
        userId = events[0]["source"]["userId"]
        state = mf.getNowState()
        if state == 0:
            text = events[0]["message"]["text"]
            if text == "切換" and userId in userids:
                payload["messages"] = [tf.getOpenText()]
            else:
                print("今日休息")
                payload["messages"] = [tf.getTodayClosedText()]
            replyMessage(payload)
        else: 
            print(state,"營業中")
            # print("營業中")
            if events[0]["type"] == "message":
                if events[0]["message"]["type"] == "text":
                    text = events[0]["message"]["text"]
                    if userId not in mf.getuseridlist() :
                        if "我的暱稱：" in text:
                            nickname = text[5:]
                            payload["messages"] = [f.getConfirmNickname(nickname)]
                        else:
                            print("Insert Nickname")
                            payload["messages"] = [f.getUseridNickname()]
                    else:
                        Reserve_willing = mf.getUseridstate(userId)
                        nowdate_1,nowtime_1 = f.getnowdateandnowtime()
                        if text == "我要預約" :
                            if mf.CountOrdersofUserid(userId) < 2:
                                yeardate = f.getyeardatedict()
                                if len(yeardate[nowdate_1]) == len(CHECKLIST):
                                    payload["messages"] = [tf.getAutoReplyText(),tf.getHavenoTimeText()]
                                elif nowtime_1 > "23:59":
                                    print(nowtime_1,"超過22:00了")
                                    payload["messages"] = [tf.getOverServicetimeText()]
                                else:
                                    payload["messages"] = [tf.getAutoReplyText(),f.getConfirmReserve()]
                            else:
                                payload["messages"] = [tf.getAutoReplyText(),tf.getReservedtimeIsTwo_Text()]
                        elif Reserve_willing == 1 and len(text.split(" ")) == 2 or "一樣" in text:
                            if mf.CountOrdersofUserid(userId) < 2:
                                if len(text)==2 and "一樣" in text :
                                    tradeName, partyName = mf.writeintotemporder_thesame(userId)
                                    payload["messages"] = [tf.getAutoReplyText(),f.getConfirmRoleName(tradeName, partyName)]
                                elif len(text.split(" ")[0].encode("utf-8")) <= 18 and len(text.split(" ")[1].encode("utf-8")) <= 18 :
                                    mf.getChangeUserstate(userId=userId, state=2)
                                    tradeName, partyName = mf.writeintotemporder_nonthesame( text, userId)
                                    payload["messages"] = [tf.getAutoReplyText(),f.getConfirmRoleName(tradeName, partyName)]
                                else:
                                    payload["messages"] = [tf.getAutoReplyText(),tf.getWrongIdFormat()]
                            else:
                                payload["messages"] = [tf.getReservedtimeIsTwo_Text()]        
                        if text == "查詢預約資訊":
                            payload["messages"] = [f.getUseridOrder(userId)]
                        if text =="測試":
                            payload["messages"] = [test(userId)]
                        if text =="刪除預約":
                            _, nowtime_delete = f.getnowdateandnowtime()
                            if nowtime_delete > "23:59":
                                print(nowtime_delete,"超過22:00了")
                                payload["messages"] = [tf.getOverServicetimeText()]
                            else:
                                payload["messages"] = [
                                                        tf.getDeleteOrderText(),
                                                        f.getUseridOrder(userId),
                                                        f.getConfirmDeleteOrder()
                                                    ]
                        if text == "今日時間":
                            todayDate, _ = f.getnowdateandnowtime()
                            payload["messages"] = [tf.getAutoReplyText(),f.getFreeTime(todayDate, CHECKLIST)]
                        if text == "全部訂單" and userId in userids:
                            payload["messages"] = [mf.getGetAllorders()]
                        if  "指定時間：" in text and userId in userids:
                            Timelist = text[5:].split(" ")
                            payload["messages"] = [mf.getDeleteSomeOrderList(Timelist)]
                        if text == "我的點數" :
                            if  userId in mf.getuseridlist():
                                print(userId,"in USERIDSLIST")
                                payload["messages"] = [mf.getMypointsCard(userId),mf.getMyPointsText(userId)]
                        if text == "更新點數" and userId in userids:
                            payload["messages"] = [mf.getUpdatePoints()]
                        if text == "切換" and userId in userids:              
                            print("切換為休息")
                            payload["messages"] = [tf.getClosedText()]
                        if text == "兌換":
                            point = mf.getuserIdPoints(userId)
                            if point > 4:
                                payload["messages"] = [f.getConfirmFreeBuff()]
                            else:
                                payload["messages"] = [tf.getDenyExchangeText(point)]
                    replyMessage(payload)
            elif events[0]["type"] == "postback":
                data = json.loads(events[0]["postback"]["data"])
                action = data["action"]
                userId_state3 = mf.getUseridstate(userId)
                if "params" in events[0]["postback"] and action =='Time chosen' and userId_state3 == 3:
                    if mf.CountOrdersofUserid(userId) < 2:
                        reservedDatetime = events[0]["postback"]["params"]["datetime"].split("T")
                        reservedDate = reservedDatetime[0]
                        reservedTime = reservedDatetime[1]
                        if str(reservedTime)  not in  CHECKLIST :
                                data = json.loads(events[0]["postback"]["data"])
                                print(data)
                                print(f"{reservedTime}不符合格式")
                                payload["messages"] = [ tf.getAutoReplyText(),
                                                        tf.getWrongTimeFormat( str(reservedDate),reservedTime), 
                                                        f.getChooseTimeAgain()
                                                        ]
                        else:
                            payload["messages"] = [ tf.getAutoReplyText(),
                                                    tf.getUserPickedTimeText( str(reservedDate), reservedTime),
                                                    f.getConfirmChooseTime( str(reservedDate), reservedTime, userId=userId)
                                                    ]
                            yeardate = f.getyeardatedict()
                            if str(reservedTime) in yeardate[reservedDate]:
                                print(yeardate[reservedDate],"reservetime list")
                                data = json.dumps({'action':'Time chosen'})
                                mf.getChangeUserstate(userId=userId, state=3)
                                payload["messages"] = [ 
                                                    tf.getReservedTimeText(),
                                                    f.getFreeTime(reservedDate, CHECKLIST),
                                                    f.getChooseTimeAgain()
                                                    ]
                    else:
                        payload["messages"] = [tf.getReservedtimeIsTwo_Text()]  
                    replyMessage(payload)
                else:
                    data = json.loads(events[0]["postback"]["data"])
                    action = data["action"] 
                    userId_state = mf.getUseridstate(userId)
                    if userId_state == 4 and action == "Time_confirmed":
                        mf.writeintotemporder_secondtime(userId, data)
                        payload["messages"] = [tf.getAutoReplyText(),mf.getConfirmFinalOrder(userId)]
                    elif action == 'Reserve_willing':
                        mf.getChangeUserstate(userId=userId, state=1)
                        payload["messages"] = [ tf.getAutoReplyText(),
                                                tf.getRoleNames(),
                                                tf.getRoleNamesExample1(),
                                                tf.getRoleNamesExample2()
                                            ]
                    elif userId_state == 2 and action == 'tradeName&partyName confirmed':
                        todayDate, _ = f.getnowdateandnowtime()
                        mf.getChangeUserstate(userId=userId, state=3)
                        payload["messages"] = [tf.getAutoReplyText(),
                                               f.getFreeTime(todayDate, CHECKLIST),
                                               f.getChooseTime(data)
                                               ]
                    elif action == 'FinalOrder confirmed':
                        thisuser_yeardate_time = f.getuseridyeardatetime(userId)
                        mf.getChangeUserstate(userId=userId, state=5)
                        yeardate = f.getyeardatedict()
                        if thisuser_yeardate_time[1] not in yeardate[thisuser_yeardate_time[0]]:
                            yeardate[thisuser_yeardate_time[0]].append(thisuser_yeardate_time[1])
                            ordered_time_list = yeardate[thisuser_yeardate_time[0]]
                            print("時間未被選過",yeardate)
                            payload["messages"] = [mf.getRealFinalOrder(userId, ordered_time_list, checklist=CHECKLIST),
                                                   f.getUseridOrder(userId)]
                        else:
                            print(f"差一點，就在剛剛{thisuser_yeardate_time[1]}被預約走了，請選擇其他時間")
                            mf.getalmosttakeorder(userId, thisuser_yeardate_time)
                            data = json.dumps({'action':'Time chosen'})
                            payload["messages"] = [ tf.getAutoReplyText(),
                                                    tf.getAfterOtherUsersText(thisuser_yeardate_time[1]),
                                                    f.getChooseTimeAgain()
                                                    ]
                    if action == 'Delete order':
                        payload["messages"] = [mf.getChooseDeleteTime(userId)]
                    if action == 'Time want to delete':
                        deletedtime = data["time"]
                        payload["messages"] = [f.getComfirmTimetoDelete(deletedtime)]
                    if action == 'Surely delete the time':
                        surelydeletedtime = data["time"]
                        payload["messages"] = [mf.getDeleteTimeSurelyText(surelydeletedtime, userId),
                                               f.getUseridOrder(userId)]
                    if action == 'My nickname example':
                        example1, example2, example3 = tf.getNicknameExample()
                        payload["messages"] = [ example1, example2, example3]
                    if action == 'confirm nickname':
                        nickname = data["nickname"]
                        mf.getPoints_write_into_useridpoints( userId, nickname)
                        payload["messages"] = [tf.getRewardCardSuccesslyText()]
                    if action == 'Exchange confirmed':
                        point = mf.getuserIdPoints(userId)
                        if point < 5:
                            payload["messages"] = [tf.getDenyExchangeText(point)]
                        else:
                            point -= 5
                            lock = threading.Lock()
                            with lock:
                                try:
                                    mydb = myclient["buff_online"]
                                    mycol = mydb["userid_points"]
                                    mydoc = mycol.update_one({"_id":userId},{"$set":{"points":point}})
                                    print("兌換成功")
                                except:
                                    print("兌換失敗")
                            Text1, Text2 = tf.getExchangeSuccesslyText(point)
                            payload["messages"] = [Text1, Text2]
                    replyMessage(payload)

    return 'OK'




'''測試函式'''
def test(userId):
    message = {
                "type":"text",
                "text":"\'Auto Reply\'"
                }
    if userId in userids:
        return message



'''利用Line api 中 reply分類作為機器人回覆功能的主要函式'''
def replyMessage(payload):
    url='https://api.line.me/v2/bot/message/reply'
    response = requests.post(url,headers=HEADER,json=payload)
    
    print(response.status_code)
    print(response.text)
    return 'OK'

if __name__ == "__main__":
    app.debug = True
    # app.run(debug=True, port=5000, host="0.0.0.0")
    app.run()
