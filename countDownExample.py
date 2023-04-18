import cv2
import time

# Set up video capture
cap = cv2.VideoCapture(0)

# Define font and text color for countdown
font = cv2.FONT_HERSHEY_SIMPLEX
color = (0, 255, 0)  # Green

# Countdown from 5 to 1
for i in range(5, 0, -1):
    # Read a frame from the video capture
    ret, frame = cap.read()

    # Draw the countdown text on the frame
    text = str(i)
    textsize = cv2.getTextSize(text, font, 4, 5)[0]
    x = int((frame.shape[1] - textsize[0]) / 2)
    y = int((frame.shape[0] + textsize[1]) / 2)
    cv2.putText(frame, text, (x, y), font, 4, color, 5, cv2.LINE_AA)

    # Display the frame with the countdown text
    cv2.imshow('Countdown', frame)
    cv2.waitKey(1000)  # Wait for 1 second

# Loop over video frames
while True:
    # Read a frame from the video capture
    ret, frame = cap.read()

    # Draw the current time on the frame
    current_time = time.strftime("%H:%M:%S", time.localtime())
    cv2.putText(frame, current_time, (50, 50), font, 1, color, 2, cv2.LINE_AA)

    # Display the frame with the time
    cv2.imshow('Video Stream', frame)

    # Check for 'q' key to quit
    if cv2.waitKey(1) == ord('q'):
        break

# Release the video capture and close the windows
cap.release()
cv2.destroyAllWindows()
