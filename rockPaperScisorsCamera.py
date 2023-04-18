import cv2
import mediapipe as mp
import math, time
import serial

def fingerPos(tips, lmLista):
    #itterate through the lm listes based on the tips and check if finger is open or closed
    pass
    

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
mpDraw = mp.solutions.drawing_utils
mpDrawStyle = mp.solutions.drawing_styles



hand = mpHands.Hands(static_image_mode=False,
               max_num_hands=1,
               model_complexity=1,
               min_detection_confidence=0.5,
               min_tracking_confidence=0.5)

print(hand)

fingerTips = [4, 8, 12, 16, 20]
playCall = ''

while True:
    fingerPosList = []
    success, img = cap.read()
    if not success:
        print('Ignoring empty camera frame.')
        continue
    
    img.flags.writeable = False
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hand.process(img)
    
    img.flags.writeable = True
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    
    # imageHeight, imageWidth, _ = img.shape
    # annotatedImage = img.copy()
    
    h, w, c = img.shape
    if results.multi_hand_landmarks:
        for handtype, handLms in zip(results.multi_handedness, results.multi_hand_landmarks):
            myHand = {}
            myLmList = []
            xList = []
            yList = []
            
            for id, lm in enumerate(handLms.landmark):
                px, py, pz = int(lm.x *w), int(lm.y * h), int(lm.z * w)
                myLmList.append([px, py, pz])
                xList.append(px)
                yList.append(py)
                                
            ##bbox
            xmin, xmax = min(xList), max(xList)
            ymin, ymax = min(yList), max(yList)
            boxW, boxH = xmax - xmin, ymax - ymin
            bbox = xmin, ymin, boxW, boxH
            cx, cy = bbox[0] + (bbox[2] // 2), bbox[1] + (bbox[3] // 2)
            
            myHand["myLmList"] = myLmList
            myHand["bbox"] = bbox
            myHand["center"] = (cx, cy)
                     
            mpDraw.draw_landmarks(
                img,
                handLms,
                mpHands.HAND_CONNECTIONS,
                mpDrawStyle.get_default_hand_landmarks_style())
            
            cv2.rectangle(img, (bbox[0] -20, bbox[1] - 20),
                          (bbox[0] + bbox[2] +20, bbox[1] + bbox[3] + 20),
                          (255, 0, 255), 2)
            
            
        for tip in fingerTips:
            if tip == 4:
                if myLmList[tip][0] < myLmList[tip-1][0]:
                    print("Thumb: closed")
                    fingerPosList.append(0)
                else:
                    print("Thumb: open")
                    fingerPosList.append(1)
            else:
                if myLmList[tip][1] < myLmList[tip-2][1]:
                    print(f'{tip}: closed')
                    fingerPosList.append(1)
                else:
                    print(f'{tip}: open')
                    fingerPosList.append(0)
        
        print(fingerPosList)
        call = 0
        for fing in fingerPosList:
            call = call + fing
        
        if call == 0:
            playCall = "ROCK!"
        elif call == 5:
            playCall = "PAPER!"
        elif (fingerPosList[1] == 1 and fingerPosList[2] == 1 and call == 2):
            playCall = "SCISSORS!"
        else:
            playCall = "Bad Call! :-("
        
        
        #cv2.putText(img, str(int(fps)), (10, 50), cv2.FONT_HERSHEY_COMPLEX, 3,(255, 0, 255), 3)
        
        time.sleep(0.2)
                
        img = cv2.flip(img,1)
        cv2.putText(img, playCall, (bbox[0] -20, bbox[1] - 20), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 0, 255),3)
    cv2.imshow("My Hand Detection",img)
    if cv2.waitKey(5) & 0xff == 27:
        break
    
cap.release()
cv2.destroyAllWindows()