import numpy as np
import cv2
from datetime import datetime
import time
import json
import re
from module import firebase_work as fw

from utils import sort, imagezmq
from module import FCMManager as fcm
from module import dbModule as dbm


class Yolo:
    def __init__(self, args):
        self.args = args

        # YOLO 모델이 학습된 coco 클래스 레이블
        with open(self.args.label, "r") as f:
            self.LABELS = [line.strip() for line in f.readlines()]

        with open('./config/app-token.json', 'r') as file:
            get_token = json.load(file)
        self.token = [get_token['token']]

        # 객체를 표시할 bounding box와 text의 랜덤 색상
        self.COLORS = np.random.randint(0, 255, size=(200, 3), dtype="uint8")

        # COCO 데이터 세트(80 개 클래스)에서 훈련된 YOLO 객체 감지기 load
        self.net = cv2.dnn.readNet(self.args.weights, self.args.configure)

        # YOLO에서 필요한 output 레이어 이름
        self.ln = self.net.getLayerNames()
        self.ln = [self.ln[i[0] - 1]
                   for i in self.net.getUnconnectedOutLayers()]
        # self.ln = [self.ln[i - 1] for i in self.net.getUnconnectedOutLayers()]

        self.tracker = sort.Sort()
        self.dbmodule = dbm.Database()
        # self.memory = {}
        self.object_dict = {
            'water_deer': '고라니',
            'wild_pig': '멧돼지',
            'cat': '고양이',
            'person': '사람'
        }
        self.object_frame_count = {}
        self.object_to_json = {}
        self.detected_object_list = []

        # 영상선택 pi / 웹캠 / 동영상
        if self.args.input == "pi":
            self.image_hub = imagezmq.ImageHub()

        elif self.args.input == "0":
            self.vs = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        else:
            self.vs = cv2.VideoCapture(self.args.input)

    # Video stream frame을 생성하고 웹으로 전송함
    def gen_frames(self):

        (W, H) = (None, None)

        # loop over frames from the video file stream
        while True:
            # read the next frame from the file
            if self.args.input == "pi":
                try:
                    grabbed, frame = self.image_hub.recv_image()
                except:
                    print("Except Error!")
                    self.image_hub.send_reply(b"OK")
                    time.sleep(0.1)
                    continue

            else:
                grabbed, frame = self.vs.read()

            # if the frame was not grabbed, then we have reached the end of the stream
            if grabbed == False:
                self.image_hub.send_reply(b"OK")
                continue

            frame = self.detect(W, H, frame)

            if self.args.input == "pi":  # 파이카메라 영상 송출 부분 (필수)
                self.image_hub.send_reply(b"OK")

            yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")

            # object_frame_count의 최대값이 미리 설정된 임계값을 넘을 경우 현재 프레임을 캡쳐하고 초기화
            # 그와 동시에 json 형식으로 출력한다. 추후 구현 예정
            if self.object_frame_count.values():
                if max(self.object_frame_count.values()) > self.args.frame:
                    # self.json = json.dumps(self.object_to_json, indent="\t")
                    # print(self.json)
                    # with open("text.json", "w", encoding="utf-8") as make_file:
                    #     json.dump(self.object_to_json, make_file, indent="\t")

                    # cv2.imwrite(
                    #     f"static/images/{datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S').replace(':','')}.jpeg",
                    #     self.frame,
                    # )
                    # self.dbmodule.insertInfo(self.object_to_json[datetime.datetime.now().strftime("%Y%m%d")][0]["name"])
                    # print(self.object_to_json)
                    object_name = re.sub(
                        r'[0-9]+', '', max(self.object_frame_count.keys()))

                    if fw.pushIntensity() == 2:
                        fcm.sendPush(self.object_dict[object_name], self.token)
                    self.object_frame_count = {}

    def detect(self, H, W, frame):
        # if the frame dimensions are empty, grab them
        if W is None or H is None:
            (H, W) = frame.shape[:2]

        # construct a blob from the input frame and then perform a forward
        # pass of the YOLO object detector, giving us our bounding boxes
        # and associated probabilities
        blob = cv2.dnn.blobFromImage(
            frame,
            scalefactor=0.00392,
            size=(416, 416),
            mean=(0, 0, 0),
            swapRB=True,
            crop=False,
        )

        # 객체 인식
        self.net.setInput(blob)
        layerOutputs = self.net.forward(self.ln)

        # initialize our lists of detected bounding boxes, confidences,
        # and class IDs, respectively
        boxes = []
        confidences = []
        classIDs = []

        # loop over each of the layer outputs
        for output in layerOutputs:
            # loop over each of the detections
            for detection in output:
                # extract the class ID and confidence (i.e., probability)
                # of the current object detection
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]

                # filter out weak predictions by ensuring the detected
                # probability is greater than the minimum probability
                if confidence > self.args.confidence:
                    # scale the bounding box coordinates back relative to
                    # the size of the image, keeping in mind that YOLO
                    # actually returns the center (x, y)-coordinates of
                    # the bounding box followed by the boxes' width and height
                    # bounding box 위치 계산
                    # (중심 좌표 X, 중심 좌표 Y, 너비(가로), 높이(세로))x
                    box = detection[0:4] * np.array([W, H, W, H])
                    (centerX, centerY, width, height) = box.astype("int")

                    # use the center (x, y)-coordinates to derive the top
                    # and and left corner of the bounding box
                    # bounding box 왼쪽 위 좌표
                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))

                    # update our list of bounding box coordinates,
                    # confidences, and class IDs
                    # bounding box, 확률 및 클래스 ID 목록 추가
                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
                    classIDs.append(classID)

        # apply non-maxima suppression to suppress weak, overlapping bounding boxes
        # bounding box가 겹치는 것을 방지
        idxs = cv2.dnn.NMSBoxes(
            boxes, confidences, self.args.confidence, self.args.threshold
        )
        dets = []
        if len(idxs) > 0:
            # loop over the indexes we are keeping
            for i in idxs.flatten():
                (x, y) = (boxes[i][0], boxes[i][1])
                (w, h) = (boxes[i][2], boxes[i][3])
                if x == x + w:
                    continue
                if y == y + h:
                    continue
                dets.append([x, y, x + w, y + h, confidences[i]])

        np.set_printoptions(
            formatter={"float": lambda x: "{0:0.3f}".format(x)})
        dets = np.asarray(dets)
        tracks = self.tracker.update(dets)

        boxes = []
        indexIDs = []
        # c = []
        # previous = self.memory.copy()
        # self.memory = {}

        try:
            for track in tracks:
                boxes.append([track[0], track[1], track[2], track[3]])
                indexIDs.append(int(track[4]))
                # self.memory[indexIDs[-1]] = boxes[-1]
        except:
            pass

        object_count = {}
        if len(boxes) > 0:
            i = int(0)
            for box in boxes:
                text = "{}{}".format(self.LABELS[classIDs[i]], indexIDs[i])

                # 탐지된 객체의 class counter
                if self.LABELS[classIDs[i]] in object_count:
                    object_count[self.LABELS[classIDs[i]]] += 1
                else:
                    object_count[self.LABELS[classIDs[i]]] = 1

                # 탐지된 객체의 frame counter
                if text in self.object_frame_count:
                    self.object_frame_count[text] += 1
                else:
                    self.object_frame_count[text] = 1

                # 객체가 처음 탐지되었을 때 출력하는 코드.
                if text not in self.detected_object_list:
                    object_name = re.sub(r'[0-9]+', '', text)
                    if fw.pushIntensity() == 1:
                        fcm.sendPush(self.object_dict[object_name], self.token)
                    self.detected_object_list.append(text)
                    cv2.imwrite(
                        f"static/images/{datetime.now().strftime('%Y-%m-%d')}/{datetime.now().strftime('%Y-%m-%d_%H:%M:%S').replace(':','')}_{text.replace('_','')}.jpeg",
                        frame,
                    )
                    # fw.storagePush("image", object_name,
                    #                datetime.now().strftime('%Y-%m-%d'))
                    # print(f"{text} has been detected...")
                    # 데이터베이스에 객체 정보 저장
                    self.dbmodule.insertInfo(re.sub(r'[0-9]+', '', text))

                # 매 객체를 출력하는 코드. 주석 해제할 경우 너무 많이 출력이 된다.
                # print(f"{self.detected_object_list} has been detecting...")

                # extract the bounding box coordinates
                (x, y) = (int(box[0]), int(box[1]))
                (w, h) = (int(box[2]), int(box[3]))
                # x, y, w, h = boxes[i]

                # draw a bounding box rectangle and label on the image
                # color = [int(c) for c in COLORS[classIDs[i]]]
                # cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

                color = [int(c)
                         for c in self.COLORS[indexIDs[i] % len(self.COLORS)]]
                cv2.rectangle(frame, (x, y), (w, h), color, 2)

                # 바운딩 박스 중앙의 선 출력
                # if indexIDs[i] in previous:
                #     previous_box = previous[indexIDs[i]]
                #     (x2, y2) = (int(previous_box[0]), int(previous_box[1]))
                #     (w2, h2) = (int(previous_box[2]), int(previous_box[3]))
                #     p0 = (int(x + (w - x) / 2), int(y + (h - y) / 2))
                #     p1 = (int(x2 + (w2 - x2) / 2), int(y2 + (h2 - y2) / 2))
                # cv2.line(frame, p0, p1, color, 3)

                cv2.putText(
                    frame, text, (x, y -
                                  5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2
                )
                i += 1

        # total count 출력
        count_text = ""
        # now = datetime.now().strftime("%Y-%m-%d")
        # self.object_to_json[now] = []
        for object in object_count:
            count_text += f"{object}: {object_count[object]} "

        #     object_dict = OrderedDict()
        #     object_dict["name"] = object
        #     object_dict["count"] = object_count[object]
        #     self.object_to_json[now].append(object_dict)

        cv2.putText(
            frame,
            count_text,
            (50, 50),
            cv2.FONT_HERSHEY_DUPLEX,
            1.0,
            (0, 255, 255),
            2,
        )

        self.frame = frame

        _, buffer = cv2.imencode(".jpg", frame)
        frame = buffer.tobytes()

        return frame
