import datetime
import cv2
import json
import os
from datetime import date
from datetime import timedelta
from datetime import datetime
import numpy as np
from firebase_admin import firestore

from utils import opts, handling_file
from yolo import Yolo
from module import dbModule as dbm
from module import firebase_work as fw

from threading import Thread
from flask import Flask, jsonify, render_template, Response, request, session


app = Flask(__name__)
app.secret_key = "인천대학교 컴퓨터공학과 캡스톤디자인 Be Bomb"


# video_output: output of video recording
# rec: recording status
video_output = None
rec = False


def createFolder(today_date):
    try:
        if not os.path.exists(today_date):
            os.makedirs("static/images/"+today_date)
            os.makedirs("static/videos/"+today_date)
    except:
        print('Error: Creating directory. ' + today_date)


def record(video_output):
    iter = 0
    while rec:
        if iter % 500 == 0:
            print("녹화 중 ...")

        video_output.write(yolo.frame)
        iter += 1


def reserve_record(video_output, start_time, end_time):
    now = datetime.now()
    iter = 0

    while start_time <= now and now <= end_time:
        if iter % 500 == 0:
            print("예약녹화 중 ...")
        video_output.write(yolo.frame)

        now = datetime.now()
        iter += 1

    video_output.release()
    print("예약녹화 완료")


# APP Token 받은 후 app-token.json 파일 생성
# @app.route("/get_token", methods=['POST'])
# def get_token():
#     if request.method == 'POST':
#         request_data = json.loads(request.data.decode('utf-8'))
#         with open('./config/app-token.json', 'w') as file:
#             json.dump(request_data, file)
#     return ""

# APP Token 받은 후 app-token.json 파일 생성
@app.route("/send_ip", methods=['GET'])
def send_IP():
    ip = fw.getIP()
    return ip


@app.route("/send_app", methods=['GET'])
def send_to_app():
    db = dbm.Database()
    # stacked bar chart: 시간대별 통계
    time_day = np.array(db.selectByTime()).transpose().tolist()
    # pie chart: 전체 통계
    day_total = db.selectTodayAll()
    return jsonify([time_day, day_total])


@app.route("/send_noti", methods=['GET', 'POST'])
def send_msg_app():
    db = dbm.Database()
    if request.method == 'GET':
        message = db.sendNotiList()
        return jsonify(message)
    else:
        request_index = json.loads(request.data.decode('utf-8'))
        idx = int(request_index['id'])
        db.removeNoti(idx)
        return ""


@ app.route("/video_feed")
def video_feed():
    # Video streaming route. Put this in the src attribute of an img tag
    return Response(
        yolo.gen_frames(), mimetype="multipart/x-mixed-replace; boundary=frame"
    )


# Video streaming home page.
@ app.route("/")
def index():
    global rec
    obdict = {
        'wat': '고라니',
        'wil': '멧돼지',
        'per': '사람',
        'cat': '고양이'
    }
    return render_template("index.html", rec=rec, obdict=obdict)


# Video streaming home page.
@ app.route("/result", methods=["GET", "POST"])
def result():
    global rec, video_output
    # now = datetime.now()

    if request.method == "POST":
        if request.form["button"][:2] == "녹화":
            rec = not rec
            if rec:
                fourcc = cv2.VideoWriter_fourcc(*"XVID")
                video_output = cv2.VideoWriter(
                    f"static/videos/{datetime.now().strftime('%Y-%m-%d')}/{datetime.now().strftime('%Y-%m-%d_%H:%M:%S').replace(':','')}.avi",
                    fourcc,
                    120,
                    (yolo.frame.shape[1], yolo.frame.shape[0]),
                )
                thread = Thread(
                    target=record,
                    args=[video_output],
                )
                thread.start()
            else:
                video_output.release()
                print("녹화 완료")

        elif request.form["button"] == "캡쳐":
            cv2.imwrite(
                f"static/images/{datetime.now().strftime('%Y-%m-%d')}/{datetime.now().strftime('%Y-%m-%d_%H:%M:%S').replace(':','')}.jpeg", yolo.frame)
            print("캡쳐 완료")

        elif request.form["button"] == "예약녹화":
            start_time = request.form["scheduler"][:19]
            start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")

            end_time = request.form["scheduler"][22:]
            end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")

            fourcc = cv2.VideoWriter_fourcc(*"XVID")
            video_output = cv2.VideoWriter(
                f"static/videos/{datetime.now().strftime('%Y-%m-%d_%H:%M:%S').replace(':','')}.avi",
                fourcc,
                120,
                (yolo.frame.shape[1], yolo.frame.shape[0]),
            )
            thread = Thread(
                target=reserve_record,
                args=[video_output, start_time, end_time],
            )
            thread.start()

    return render_template("index.html", rec=rec)


@ app.route("/get_images")
def get_images():
    session.clear()

    handling_file.remove_outdated_files()
    file_list = handling_file.get_detected_images()
    if file_list:
        session["imageName"] = file_list
    return "get images"


@ app.route("/charts_page")
def charts_page():
    db = dbm.Database()
    # stacked bar chart: 시간대별 통계
    time_day = json.dumps(db.selectByTime())
    time_weekly = json.dumps(db.selectByTimeWeekly())
    time_total = json.dumps(db.selectByTimeTotal())
    # pie chart: 전체 통계
    day_total = json.dumps(db.selectTodayAll())
    weekly_total = json.dumps(db.selectWeeklyAll())
    all_total = json.dumps(db.selectAll())
    obdict = {
        'wat': '고라니',
        'wil': '멧돼지',
        'per': '사람',
        'cat': '고양이'
    }

    return render_template("chart.html",
                           time_day=time_day, time_weekly=time_weekly, time_total=time_total,
                           day_total=day_total, weekly_total=weekly_total, all_total=all_total,
                           obdict=obdict)


if __name__ == "__main__":
    handling_file.remove_outdated_files()
    createFolder(datetime.now().strftime('%Y-%m-%d'))
    fw.getToken()
    opt = opts.parse_opt()
    yolo = Yolo(opt)
    # app.run(host="0.0.0.0", debug=True, port=3000)
    app.run(host="localhost", debug=True, port=3000)
