import numpy as np
import matplotlib.pyplot as plt
from moving_object_detection.moving_object_detector import MovingObjectDetector
import object_tracking.kalman_filter2 as KF
from object_classifier.classified_object import ClassifiedObject
import cv2

cap = cv2.VideoCapture("./data/videos/street.mp4")

mod = MovingObjectDetector()

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        mod.run(frame)
        img = mod.get_image_with_bounding_boxes(frame)

        cv2.imshow('Frame', img)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    else:
        break
cap.release()
cv2.destroyAllWindows()

positions = mod.moving_objects[0].positions
n_measurements = len(positions)
measurements = np.asarray(positions).T

# Defines
n_states = 4
dt = 0.025
std_pos_x = 1
std_pos_y = 1

# Initial state
x0 = np.array([[measurements[0, 0]],
               [measurements[1, 0]],
               [0],
               [0]])

# Initial covariance matrix
P0 = np.eye(n_states)

# Constant velocity model
A = np.array([[1, 0, dt, 0],
              [0, 1, 0, dt],
              [0, 0, 1, 0],
              [0, 0, 0, 1]])

# Measurement model
C = np.array([[1, 0, 0, 0], 
              [0, 1, 0, 0]])

# Process noise covariance matrix
Q = np.array([[3, 0, 0, 0],
              [0, 3, 0, 0],
              [0, 0, 1, 0],
              [0, 0, 0, 1]])

# Measurement noise covariance matrix
R = np.array([[std_pos_x*7, 0],
              [0, std_pos_y*7]])

# Initialize Kalman filter
kf = KF.KalmanFilter(x0, P0, A, C, Q, R)

# Run Kalman filter on measurements
pos_estim = np.zeros((2, n_measurements))
vel_estim = np.zeros((2, n_measurements))

for i in range(n_measurements):
    z = measurements[:, i].reshape((2, 1))
    kf.correct(z)
    x_hat = kf.predict()
    pos_estim[:, i] = x_hat[:2].reshape(pos_estim[:, i].shape)
    vel_estim[:, i] = x_hat[2:].reshape(vel_estim[:, i].shape)


############### Plotting ###############
measurement_x = measurements[0]
measurement_y = measurements[1]

pred_x = pos_estim[0]
pred_y = pos_estim[1]

min_x, max_x = np.min(pred_x), np.max(pred_x)
min_y, max_y = np.min(pred_y), np.max(pred_y)

vel_x = vel_estim[0, :]
vel_y = vel_estim[1, :]
t = np.linspace(0, vel_x.size, vel_x.size)

plt.figure(figsize=(10, 7))
plt.plot(measurement_x, measurement_y, color='blue', label="Measurement")
plt.plot(pred_x, pred_y, color='green', label='Predictions')
plt.xlabel('Position X [m]')
plt.ylabel('Position Y [m]')
plt.legend()

plt.figure(figsize=(10, 7))
plt.plot(t, vel_x, color='blue', label="Velocity X")
plt.xlabel('t [s]')
plt.ylabel('Velocity [m/s]')
plt.legend()

plt.figure(figsize=(10, 7))
plt.plot(t, vel_y, color='blue', label="Velocity Y")
plt.xlabel('t [s]')
plt.ylabel('Velocity [m/s]')
plt.legend()

plt.show()