import cv2
import time
import math
import numpy as np
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import mediapipe as mp


# Khai báo lớp HandTracker
class HandTracker():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, modelComplexity=1, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.modelComplex = modelComplexity
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComplex, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def handsFinder(self, image, draw=True):
        imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imageRGB)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(image, handLms, self.mpHands.HAND_CONNECTIONS)
        return image

    def positionFinder(self, image, handNo=0, draw=True):
        lmlist = []
        if self.results.multi_hand_landmarks:
            Hand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(Hand.landmark):
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmlist.append([id, cx, cy])
            if draw:
                cv2.circle(image, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
        return lmlist


# Thiết lập âm lượng hệ thống
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
vol_range = volume.GetVolumeRange()
minVol = vol_range[0]
maxVol = vol_range[1]


# Thiết lập cấu hình video
cap = cv2.VideoCapture(0)
cap.set(16, 640)
cap.set(9, 480)

# Khởi tạo bộ theo dõi bàn tay
detector = HandTracker(detectionCon=0.7)

# Khởi tạo các biến
pTime, cTime = 0, 0
vol, volBar, volPer = 0, 0, 0

while True:
    success, img = cap.read()
    if not success:
        break

    # Lật ảnh nếu bị ngược
    img = cv2.flip(img, 1)

    # Nhận diện và theo dõi bàn tay
    img = detector.handsFinder(img)
    lmList = detector.positionFinder(img, draw=False)

    if lmList:
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        # Vẽ các điểm trên ngón tay và kết nối chúng lại
        cv2.circle(img, (x1, y1), 10, (0, 255, 0), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (0, 255, 0), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 3)
        cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)

        # Tính chiều dài giữa 2 điểm
        length = math.hypot(x2 - x1, y2 - y1)

        # Quy đổi chiều dài sang giá trị âm lượng
        volBar = np.interp(length, [50, 150], [400, 150])
        volPer = np.interp(length, [50, 150], [0, 100])
        vol = np.interp(length, [50, 150], [minVol, maxVol])

        # Đặt giá trị âm lượng
        volume.SetMasterVolumeLevel(vol, None)

        # Vẽ thanh âm lượng
        cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
        cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 2)

    # Hiển thị ảnh
    cv2.imshow('Image', img)

    # Nhấn 'q' để thoát
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Giải phóng tài nguyên
cap.release()
cv2.destroyAllWindows()
