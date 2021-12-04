import cv2
import mediapipe
import handModule as hand
import time
import numpy as np
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


w = 640
h = 480
cap = cv2.VideoCapture(0)
cap.set(3,w)
cap.set(4,h)
pTime = 0
detector = hand.handDetector(minDCon = 0.7, minTCon = 0.7)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
range = volume.GetVolumeRange()
minVol,maxVol = range[0], range[1]

while cap.isOpened():
    x, img = cap.read()

    detector.findHand(img, draw=False)
    lmList = detector.findPos(img)
    if len(lmList) !=0:
        x1,y1 = lmList[4][1],lmList[4][2]
        x2,y2 = lmList[8][1],lmList[8][2]
        cx,cy = (x1+x2)//2, (y1+y2)//2
        # length = int(math.hypot(x2-x1,y2-y1))
        length = int(y1-y2)
        print(length)


        vol = np.interp(length,[0,75],[minVol,maxVol])
        # sysVol=int(np.interp(vol,[minVol,maxVol],[0,100]))
        # print(sysVol)
        volume.SetMasterVolumeLevel(vol, None)
        cv2.line(img, (x1, y1), (x2, y2), (255, 255, 0), 3)
        cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
        cv2.circle(img,(x2,y2),15,(255,0,255),cv2.FILLED)
        color = (255, 150, 0)
        # if vol > minVol:
        #     # print(vol)
        # if length <20:
        #     color = (0,255,0)
        # if vol == minVol:
        #     # print('muted')
        cv2.circle(img, (cx, cy),7,color, cv2.FILLED)

    # if volume.GetMasterVolumeLevel() == maxVol:
    #     continue
    # elif len(lmList) == 0:
    #     volume.SetMasterVolumeLevel(0, None)


    # cTime = time.time()
    # fps = 1/(cTime-pTime)
    # pTime=cTime

    # cv2.putText(img, f'{int(fps)}', (10, 50), cv2.FONT_HERSHEY_DUPLEX, 2, (0, 0, 0), 4)
    # cv2.putText(img,f'{int(fps)}',(10,50),cv2.FONT_HERSHEY_DUPLEX,2,(0,234,255),2)

    cv2.imshow('Feed', img)
    cv2.waitKey(1)


