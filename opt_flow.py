import cv2
import numpy as np

# Video feed
filename = "cars.mp4"
cap = cv2.VideoCapture(filename)

# Initial frame
ret, first_frame = cap.read()

# Converts first pic to grayscale
prev_gray = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)

# Image with same dimension as frame, filled with zeros
mask = np.zeros_like(first_frame)

# Sets image saturation to maximum
mask[..., 1] = 255
i = 0
while(cap.isOpened()):
    # Read each frame in the video
    ret, frame = cap.read()
    cv2.imshow("Input", frame)

    # Convert frame to grayscale, required for opt. flow algorithm
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Calculates optical flow using Farneback method
    flow = cv2.calcOpticalFlowFarneback(prev_gray, gray,
                                        None,
                                        0.5, 3, 15, 3, 5, 1.2, 0)

    # Magnitude and angle of 2D vectors
    magnitude, angle = cv2.cartToPolar(flow[..., 0], flow[..., 1])

    # Sets the image hue accorting to opt. flow direction
    mask[..., 0] = angle * 180 / (np.pi / 2)

    # Sets image value according to opt. flow magnitude
    mask[..., 2] = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX)

    # Converts HSV to RGB again for display
    rgb = cv2.cvtColor(mask, cv2.COLOR_HSV2BGR)
    cv2.imshow("Dense optical flow", rgb)
    cv2.imwrite(f"optflow{i}.png", rgb)
    i += 1

    # Update the prev_gray variable
    prev_gray = gray

    if(cv2.waitKey(1) & 0xFF == ord('q')):
        break

cap.release()
cv2.destroyAllWindows()