import cv2
import time

# Start video capture
cap = cv2.VideoCapture(0)

# Check if camera opened successfully
if not cap.isOpened():
    print("Error opening video stream")

# Set the video resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

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
cv2.imshow("Captured Frame", frame)
cv2.waitKey(0)

# Release the capture
cap.release()
cv2.destroyAllWindows()
