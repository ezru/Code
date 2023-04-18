import cv2
import time

# Initialize the video capture object
cap = cv2.VideoCapture(0)

# Wait for the camera to warm up
time.sleep(2)

# Define the countdown time in seconds
countdown = 3

# Define the font and color for the countdown text
font = cv2.FONT_HERSHEY_SIMPLEX
color = (0, 255, 0)
thickness = 2

# Loop through the countdown and display the text on the live stream
while countdown > 0:
    # Capture a frame from the live stream
    ret, frame = cap.read()

    # Display the current countdown value on the live stream
    text = str(countdown)
    textsize = cv2.getTextSize(text, font, 2, thickness)[0]
    textX = int((frame.shape[1] - textsize[0]) / 2)
    textY = int((frame.shape[0] - textsize[1]) / 2)
    cv2.putText(frame, text, (textX, textY), font, 2, color, thickness, cv2.LINE_AA)
    cv2.imshow('Live Stream', frame)
    cv2.waitKey(1000)  # Wait for 1 second
    
    # Decrement the countdown value
    countdown -= 1

# Display the final 'GO!' message on the live stream and wait for 0.5 seconds
text = 'GO!'
textsize = cv2.getTextSize(text, font, 2, thickness)[0]
textX = int((frame.shape[1] - textsize[0]) / 2)
textY = int((frame.shape[0] - textsize[1]) / 2)
cv2.putText(frame, text, (textX, textY), font, 2, color, thickness, cv2.LINE_AA)
cv2.imshow('Live Stream', frame)
cv2.waitKey(100)

# Capture a frame from the live stream
ret, frame = cap.read()

# Display the captured frame and wait for a key press
cv2.imshow('Captured Frame', frame)
cv2.waitKey(0)

# Release the video capture object and close the windows
cap.release()
cv2.destroyAllWindows()
