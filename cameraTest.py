from cvzone.HandTrackingModule import HandDetector
from cvzone.SerialModule import SerialObject

import cv2

import time

cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1, detectionCon = 0.7)
myserial = SerialObject("COM7", 115200, 1)

while True:
    success, img = cap.read()
    hands, img = detector.findHands(img)
    #img = detector.findHands(img)
    #lmList, bbox = detector.findPosition(img)
    if hands:
        # Hand 1
        hand = hands[0]
        lmList = hand["lmList"]  # List of 21 Landmark points
        bbox = hand["bbox"]  # Bounding box info x,y,w,h
        #centerPoint = hand['center']  # center of the hand cx,cy
        #handType = hand["type"]  # Handtype Left or Right
        fingers = detector.fingersUp(hand)
        #print(fingers)
        myserial.sendData(fingers)
        time.sleep(0.1)
    cv2.imshow("Image", img)
    cv2.waitKey(1)