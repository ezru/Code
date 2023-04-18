import cv2
import mediapipe as mp
import time

""" 
    This module is to be used for tracking hand.
    It returns a list of "Landmarks" as defined in mediapipe.

"""
class handDetector:
    def __init__(self, mode=False, maxHands=2, detectCon=0.5, trackCon=0.5):
        # These attributes are for initialising mediapipe object hands
        self.mode = mode
        self.maxHands = maxHands
        self.detectCon = detectCon
        self.trackCon = trackCon


        self.mpHands = mp.solutions.hands   # This creates the hands object of mediapipe
                                            # As defined in the media pipe this exists under the solutions
        self.hands = self.mpHands.Hands(static_image_mode=self.mode, max_num_hands=self.maxHands,
                                        min_detection_confidence=self.detectCon, 
                                        min_tracking_confidence = self.trackCon)    #This initialises the hand object
                                                                                    # using the attributes passed above
        self.mpDraw = mp.solutions.drawing_utils    # This is another object that allows us to draw 
                                                    # the landmarks on the hands

    # method that enables us to find a hand
    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)   # the colour of the images needs to be converted for it to 
                                                        # be processed using the method below
        self.results = self.hands.process(imgRGB)   # Returns object containing all the detected hands
        #print(results.multi_hand_landmarks)
        #print(self.results)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    # the draw_landmarks has the option for drawing the connection of the landmarks
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
                    #self.mpDraw.draw_landmarks(img, handLms) 
     
    
        return img

 
    def findPosition(self, img, handNo=0, draw=True):
        lmList = []

        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo] #We are taking only one hand for our project purpose
            for id, lm in enumerate(myHand.landmark):
                #print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                #print(id, cx, cy)
                lmList.append([id, cx, cy])
                if id == 4:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 0), cv2.FILLED)
                if id == 8:
                    cv2.circle(img, (cx, cy), 15, (0, 255, 255), cv2.FILLED)
                #if draw:
                    #cv2.circle(img, (cx, cy), 15, (0, 0, 255), cv2.FILLED)

        return lmList


def main():
    cTime = 0
    pTime = 0
    cap = cv2.VideoCapture(0)

    detector = handDetector()

    while True:
        success, img = cap.read()

        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        #if (len(lmList) != 0):
            #print(lmList[4])

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (10, 50), cv2.FONT_HERSHEY_COMPLEX, 3,
        (255, 0, 255), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()           