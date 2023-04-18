# this is a test to test the logic of the game rock paper scissors played with the robotic hand
import cv2
import mediapipe as mp
import math, time, random
import serial

handSignal = ''
arduinoSerial1 = serial.Serial('com10',9600)
choice = 0

def robotPlay():
    choice = random.randint(1, 3)
    
    if choice == 1:
        handSignal = '00000\r'
    elif choice == 2:
        handSignal = '11111\r'
    else:
        handSignal = '01100\r'
        
    arduinoSerial1.write(handSignal.encode())
        
    print(f'Robot move: {handSignal}')
    #time.sleep(2)

move = 0

def fingerPos(tips, lmLista):
    #itterate through the lm listes based on the tips and check if finger is open or closed
    pass

# Start video capture
cap = cv2.VideoCapture(0)

# Check if camera opened successfully
if not cap.isOpened():
    print("Error opening video stream")
    
mpHands = mp.solutions.hands
mpDraw = mp.solutions.drawing_utils
mpDrawStyle = mp.solutions.drawing_styles

# Set the video resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

hand = mpHands.Hands(static_image_mode=True,
               max_num_hands=1,
               model_complexity=1,
               min_detection_confidence=0.5,
               min_tracking_confidence=0.5)

print(hand)
fingerTips = [4, 8, 12, 16, 20]
playCall = ''

# Wait for 5 seconds before starting the countdown
start_time = time.time()
while True:
    ret, frame = cap.read()
    cv2.imshow("Live Stream", frame)
    if time.time() - start_time >= 5:
        break
    cv2.waitKey(1)

# Initialize the countdown
count = 4

# Loop through the countdown and capture a frame at the end
while count >= 0:
    # Display the countdown on the frame
    ret, frame = cap.read()
    cv2.putText(frame, str(count), (int(frame.shape[1]/2)-50, int(frame.shape[0]/2)), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 2)
    cv2.imshow("Live Stream", frame)

    # Check if 1 second has elapsed
    if time.time() - start_time >= 1:
        # Decrement the count
        count -= 1
        # Reset the start time for the next iteration
        start_time = time.time()

    cv2.waitKey(1)

# Capture a frame and display it
ret, frame = cap.read()

#robot moves

#PROCESSING
fingerPosList = []
success, img = cap.read()
if not success:
    print('Ignoring empty camera frame.')

    
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
        
    print(f'Human finger position: {fingerPosList}')
    call = 0
    for fing in fingerPosList:
        call = call + fing
        
    if call == 0:
        playCall = "ROCK!"
        move = 1
    elif call == 5:
        playCall = "PAPER!"
        move = 2
    elif (fingerPosList[1] == 1 and fingerPosList[2] == 1 and call == 2):
        playCall = "SCISSORS!"
        move = 2
    else:
        playCall = "Bad Call! :-("
        print("N/A")
    print(f'Person move: {move}')    
        #cv2.putText(img, str(int(fps)), (10, 50), cv2.FONT_HERSHEY_COMPLEX, 3,(255, 0, 255), 3)
        
    #time.sleep(0.2)
    robotPlay()
    print("Sent message to Robot")            
    img = cv2.flip(img,1)
    cv2.putText(img, playCall, (bbox[0] -20, bbox[1] - 20), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 0, 255),3)
cv2.imshow("My Hand Detection",img)
print('finished processing image')
#END PROCESSING

#winner code condition
# 1- rock, 2- paper, 3-scissors
print(choice, playCall)
if choice == playCall:
    print("It's a tie!")

elif choice == 1 and playCall == 2:
    print("The Robot wins!")
    
elif choice == 1 and playCall == 3:
    print("The Player wins!")
    
elif choice == 2 and playCall == 1:
    print("The Player wins!")
    
elif choice == 2 and playCall == 3:
    print("The Robot wins!")
    
elif choice == 3 and playCall == 2:
    print("The Player wins!")
    
elif choice == 3 and playCall == 1:
    print("The Robot wins!")
    
else:
    print("error")

cv2.waitKey(0)

# Release the capture
cap.release()
cv2.destroyAllWindows()
