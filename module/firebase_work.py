import pyrebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import timedelta
import json

cred = credentials.Certificate("config/service-account-file.json")
f = open('config/config.json')
config = json.load(f)
f.close()

firebase_admin.initialize_app(cred)
firebase = pyrebase.initialize_app(config)
db = firebase.database()
storage = firebase.storage()
store = firestore.client()


def storagePush(type, name, today_date):
    if type == "video":
        storage.child(
            f"videos/{today_date}/{name}").put(f"videos/{today_date}/{name}")
    elif type == "image":
        storage.child(
            f"images/{today_date}/{name}").put(f"images/{today_date}/{name}")


def getConfig():
    push_config = store.collection("configuration").document(
        "config").get().to_dict()["push_token"]
    return push_config


def pushIntensity():
    intensity = store.collection("configuration").document(
        "config").get().to_dict()["push_intensity"]
    return intensity


def getToken():
    app_token = store.collection("configuration").document(
        "config").get().to_dict()["app_token"]
    with open('./config/app-token.json', 'w') as file:
        json.dump({"token": app_token}, file)


def getIP():
    ip = store.collection("configuration").document(
        "config").get().to_dict()["ip"]
    return ip


# now = datetime.datetime.now().strftime("%Y%m%d")
# print((datetime.datetime.now() - timedelta(1)).strftime("%Y%m%d"))
# target = (datetime.datetime.now() - timedelta(2)).strftime("%Y%m%d")
# get = store.collection("database").document("detected_info").collection("2022-03-16").document("고라니").get().to_dict()["count"]
# print(get)
