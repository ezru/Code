import cv2
import mediapipe as mp
import math, time
import serial

arduinoSer1 = serial.Serial('com7', 9600)

def calcDist(p1, p2):
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    dist = math.sqrt((x2-x1)**2 +(y2-y1)**2)
    return dist

def calcAngle(ln1, ln2, ln3):
    cosC = (ln1**2 +ln2**2 - ln3**2) / (2*ln1*ln2)
    angleRad = math.acos(cosC)
    angleDeg = math.degrees(angleRad)
    return math.floor(angleDeg)

def fingerPos(tips, lmLista):
    #itterate through the lm listes based on the tips and check if finger is open or closed
    pass
    

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
mpPose = mp.solutions.pose
mpDraw = mp.solutions.drawing_utils
mpDrawing = mp.solutions.drawing_utils
mpDrawStyle = mp.solutions.drawing_styles
mpDrawingStyle = mp.solutions.drawing_styles

hand = mpHands.Hands(static_image_mode=False,
               max_num_hands=1,
               model_complexity=1,
               min_detection_confidence=0.5,
               min_tracking_confidence=0.5)

pose = mpPose.Pose()

print(hand)
print(mpPose)
rightArmList = [12, 14, 16, 24]
fingerTips = [4, 8, 12, 16, 20]

while True:
    success, img = cap.read()
    if not success:
        print('Ignoring empty camera frame.')
        continue
    
    img.flags.writeable = False
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hand.process(img)
    resultsPose = pose.process(img)
    
    img.flags.writeable = True
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    # print('Handness: ', results.multi_handedness)
    
    # imageHeight, imageWidth, _ = img.shape
    # annotatedImage = img.copy()
    
    if resultsPose.pose_landmarks is not None:
        armLms = {}
        for idx, landmark in enumerate(resultsPose.pose_landmarks.landmark):
            if idx in rightArmList:
                armLms[idx] = [landmark.x, landmark.y, landmark.z]
        
        shel = calcDist(armLms[12], armLms[14])        
        wrel = calcDist(armLms[14], armLms[16])
        shwr = calcDist(armLms[12], armLms[16]) 
        bicepAngle = calcAngle(shel, wrel, shwr)
        shel = calcDist(armLms[12], armLms[14])        
        hish = calcDist(armLms[12], armLms[24])
        elhi = calcDist(armLms[14], armLms[24]) 
        bicepAngle = calcAngle(shel, wrel, shwr)
        armpitAngle = calcAngle(shel, hish, elhi)
        
    
    
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
            mpDrawing.draw_landmarks(
                img,
                resultsPose.pose_landmarks,
                mpPose.POSE_CONNECTIONS,
                landmark_drawing_spec=mpDrawingStyle.get_default_pose_landmarks_style())
            
            cv2.rectangle(img, (bbox[0] -20, bbox[1] - 20),
                          (bbox[0] + bbox[2] +20, bbox[1] + bbox[3] + 20),
                          (255, 0, 255), 2)
            
            
        for tip in fingerTips:
            if tip == 4:
                if myLmList[tip][0] < myLmList[tip-3][0]:
                    print("Thumb: closed")
                else:
                    print("Thumb: open")
            else:
                if myLmList[tip][1] < myLmList[tip-3][1]:
                    print(f'{tip}: closed')
                else:
                    print(f'{tip}: open')
    
    
    print(f'BicepAngle: {bicepAngle} - ArmpitAngle: {armpitAngle}')
    bicepAngleStr = str(180 - bicepAngle) + '\r'
    arduinoSer1.write(bicepAngleStr.encode())
            
    img = cv2.flip(img,1) 
    cv2.imshow("My Hand Detection",img)
    if cv2.waitKey(5) & 0xff == 27:
        break
    
cap.release()
cv2.destroyAllWindows()
arduinoSer1.close()