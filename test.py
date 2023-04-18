import cv2
import time

# Initialize the video capture object
cap = cv2.VideoCapture(0)

# Wait for the camera to warm up
time.sleep(2)

# Capture a single frame from the video stream
ret, frame = cap.read()

# Define the countdown time in seconds
countdown = 3

# Define the font and color for the countdown text
font = cv2.FONT_HERSHEY_SIMPLEX
color = (0, 255, 0)
thickness = 2

# Loop through the countdown and display the text on the frame
while countdown > 0:
    # Create a new image copy of the frame
    img = frame.copy()

    # Display the current countdown value on the frame
    text = str(countdown)
    textsize = cv2.getTextSize(text, font, 2, thickness)[0]
    textX = int((img.shape[1] - textsize[0]) / 2)
    textY = int((img.shape[0] - textsize[1]) / 2)
    cv2.putText(img, text, (textX, textY), font, 2, color, thickness, cv2.LINE_AA)
    cv2.imshow('Frame', img)
    cv2.waitKey(1000)  # Wait for 1 second
    
    # Decrement the countdown value
    countdown -= 1

# Create a new image copy of the frame
img = frame.copy()

# Display the final frame with countdown text
cv2.putText(img, 'GO!', (textX, textY), font, 2, color, thickness, cv2.LINE_AA)
cv2.imshow('Frame', img)
cv2.waitKey(0)

# Release the video capture object and close the window
cap.release()
cv2.destroyAllWindows()
