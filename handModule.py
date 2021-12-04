import cv2
import mediapipe as mp
import time
import math

class handDetector():
    def __init__(self,mode = False, maxHands = 1, minDCon = 0.5, minTCon = 0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.minDCon = minDCon
        self.minTCon = minTCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(mode,maxHands,minDCon,minTCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHand(self,img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
                for handLM in self.results.multi_hand_landmarks:
                    if draw:
                        self.mpDraw.draw_landmarks(img, handLM, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPos(self,img, handNo = 0, draw = True):

            lmList = []

            if self.results.multi_hand_landmarks:
                myHand = self.results.multi_hand_landmarks[handNo]
                for id, lm in enumerate(myHand.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmList.append([id,cx,cy])
                    # if draw:
                    #     # cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)
            return lmList
def main():
    pTime = 0
    cTime = 0
    cam = cv2.VideoCapture(0)
    detector = handDetector()
    while True:
        success, img = cam.read()
        img = detector.findHand(img, draw = True)
        lmList = detector.findPos(img)
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (252, 219, 3), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)
if __name__ == "__main__":
    main()