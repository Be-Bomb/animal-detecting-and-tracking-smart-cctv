from firebase_admin import messaging
from . import firebase_work as fw
from datetime import datetime
from . import dbModule

dbm = dbModule.Database()


def sendPush(object, registration_token, dataObject=None):
    noti_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    dbm.insertPushMessage(noti_date, object)
    if fw.getConfig():
        message = messaging.Message(
            notification=messaging.Notification(
                title=noti_date,
                body="{} 이(가) 탐지되었습니다.".format(object)
            ),
            data=dataObject,
            token=registration_token[0],
        )

        response = messaging.send(message)
        print(response)

        print("Succesfully sent message:", response)
