import cv2
import time

# set up video capture
cap = cv2.VideoCapture(0)

# initialize countdown variables
countdown = 3
countdown_start_time = None
countdown_delay = 1 # delay in seconds

# set up font and color for countdown display
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1
font_color = (0, 0, 255)

# loop until frame is captured and key is pressed
while True:
    # get frame from video capture
    ret, frame = cap.read()
    if not ret:
        break
    
    # display countdown if countdown is not finished
    if countdown > 0:
        # check if countdown start time has been set
        if countdown_start_time is None:
            countdown_start_time = time.time()
            
        # calculate time left in countdown
        time_left = countdown_delay - (time.time() - countdown_start_time)
        time_left = max(0, round(time_left))
        
        # display countdown
        cv2.putText(frame, str(countdown), (50, 50), font, font_scale, font_color, 2, cv2.LINE_AA)
        if time_left > 0:
            cv2.putText(frame, "Wait " + str(time_left) + " seconds...", (50, 100), font, 0.75, font_color, 2, cv2.LINE_AA)
        else:
            cv2.putText(frame, "Go!", (50, 100), font, 0.75, font_color, 2, cv2.LINE_AA)
            if countdown == 1:
                # wait for half a second before capturing frame and waiting for key press
                time.sleep(0.5)
                cv2.imwrite("captured_frame.jpg", frame)
                cv2.imshow("Captured Frame", frame)
                cv2.waitKey(0)
                
            countdown -= 1
            countdown_start_time = None
    
    # display frame
    cv2.imshow("Live Stream", frame)
    if cv2.waitKey(1) == ord("q"):
        break

# release video capture and close windows
cap.release()
cv2.destroyAllWindows()
