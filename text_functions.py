from mongofunction import dbmethod
import threading

'''切換營業狀態提醒文字'''
def getOpenText():
    '''切換營業狀態提醒文字'''
    lock = threading.Lock()
    with lock:
        try:
            mycol = dbmethod("buff_online","state")
            mycol.update_one({"_id":0},{"$set":{"state":1}}) 
            message = {
                "type":"text",
                "text":f"切換狀態為營業中\nstate:1"
                 }
        except:
            print("切換失敗")
            message = {
                        "type":"text",
                        "text":"切換狀態為營業中，失敗"
            }
    return message

'''切換休息狀態提醒文字'''
def getClosedText():
    '''切換休息狀態提醒文字'''
    lock = threading.Lock()
    with lock:
        try:
            mycol = dbmethod("buff_online","state")
            mycol.update_one({"_id":0},{"$set":{"state":0}}) 
            message = {
                "type":"text",
                "text":"切換狀態為休息\nstate:0"
                 }
        except:
            print("切換失敗")
            message = {
                        "type":"text",
                        "text":"切換狀態為休息，失敗"
            }
    return message

'''今日休息告知文字'''
def getTodayClosedText():
    '''今日休息告知文字'''
    message = {
                "type":"text",
                "text":"今日休息，請多多見諒"
    }
    return message

'''告知領取點數卡成功文字'''
def getRewardCardSuccesslyText():
    '''告知領取點數卡成功文字'''
    message = {
                "type":"text",
                "text":"已領取點數卡，可以進行預約了"
                }
    

    return message

'''當日已額滿文字'''
def getHavenoTimeText():
    '''當日已額滿文字'''
    message ={
        
                "type": "text",
                "text": "今日預約已額滿，造成不便敬請見諒"
             }

    return message

'''超過服務時間文字'''
def getOverServicetimeText():
    '''超過服務時間文字'''
    message ={
        
                "type": "text",
                "text": "已超過21:54，服務時間已結束，請於每日21:54之前進行預約"
             }

    return message

'''已達一天預約上線的提示訊息'''
def getReservedtimeIsTwo_Text():
    '''已達一天預約上線的提示訊息'''
    message ={ 
            "type":"text",
            "text":"您已預約兩個時間，若需修改時間請先刪除一個再預約新的時間，謝謝"
    }

    return message

'''刪除訂單提醒文字'''
def getDeleteOrderText():
    '''刪除訂單提醒文字'''
    message ={
                "type": "text",
                "text": "預約資訊："
             }
    return message

'''提醒點數不夠文字'''
def getDenyExchangeText(point):
    '''提醒點數不夠文字'''
    message = {
        "type":"text",
        "text":f"目前點數：{point}\n累積5點才能兌換唷！"

    }

    return message

'''回傳兌換成功'''
def getExchangeSuccesslyText(point):
    '''回傳兌換成功'''
    message = [
                {
                    "type":"text",
                    "text":"兌換免費Buff一次成功，已扣除5點"
                },
                {
                    "type":"text",
                    "text":f"剩餘點數：{point}"
                }
    ]

    return message[0],message[1]

'''選擇時間不在服務時間上所以重選(選擇非五的倍數時間或已被預約的時間)'''
def getWrongTimeFormat(reservedDate, reservedTime):
    '''選擇時間不在服務時間上所以重選(選擇非五的倍數時間或已被預約的時間)'''
    message ={
        
                "type": "text",
                "text": f"您輸入的日期時間為{reservedDate} {reservedTime}，請輸入正確時間\n如23：05、23：10"
             }

    return message

'''時間被預訂走了的提示訊息'''
def getReservedTimeText():
    '''時間被預訂走了的提示訊息'''
    message ={
        
                "type": "text",
                "text": "您輸入的日期時間已被預定，請重新選擇時間"
             }

    return message

'''被其他使用者搶先預約'''
def getAfterOtherUsersText(reservedtime):
    '''被其他使用者搶先預約'''
    message = {
                "type":"text",
                "text":f"差一點，就在剛剛{reservedtime}被其他人預約走了，請選擇其他時間"
    }

    return message

'''輸入交易角色ID，組隊角色ID'''
def getRoleNames():
    '''輸入交易角色ID，組隊角色ID'''
    message ={
                "type": "text",
                "text": "請輸入交易角色ID及組隊角色ID\n用(空格)隔開"
             }
    

    return message

'''預約範例1'''
def getRoleNamesExample1():
    '''預約範例1'''
    message ={
                "type": "text",
                "text": "例如："
             }

    return message

'''預約範例2'''
def getRoleNamesExample2():
    '''預約範例2'''
    message ={
                "type": "text",
                "text": "歸01 歸01"
             }

    return message

'''暱稱範例'''
def getNicknameExample():
    '''暱稱範例'''
    message = [{
                "type":"text",
                "text":"\'Auto Reply\'"
                },
                {
                "type":"text",
                "text":"例如：\n我的暱稱：明明"
                },
                {
                "type":"text",
                "text":"注意！\n點數卡將會顯示您輸入的暱稱"
                }
    ]

    return message[0], message[1], message[2]

'''角色ID格式錯誤'''
def getWrongIdFormat():
    '''角色ID格式錯誤'''
    message = {
        "type" : "text",
        "text" : "角色ID長度不符合，請重新輸入"
    }
    return message

'''使用者挑選的欲預定時間'''
def getUserPickedTimeText(reservedDate,reservedtime):
    '''使用者挑選的欲預定時間'''
    message = {
                "type":"text",
                "text":f"**您選擇的時間是{reservedDate} {reservedtime}**"
    }

    return message

'''自動回覆提醒字串'''
def getAutoReplyText():
    message = {
  "type": "flex",
  "altText": "this is a flex message",
  "contents": {
  "type": "bubble",
  'size': "micro",
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "\'Auto Reply\'",
        "decoration": "underline",
        "size":"24px"
      }
    ]
  }
}
    }
    return message





{
  "type": "bubble",
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "hello, world",
        "decoration": "underline"
      }
    ]
  }
}