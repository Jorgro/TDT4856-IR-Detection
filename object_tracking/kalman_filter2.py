import numpy as np

class KalmanFilter:
    def __init__(self, x0: 'np.ndarray', P0: 'np.ndarray', A: 'np.ndarray', 
                 C: 'np.ndarray', Q: 'np.ndarray', R: 'np.ndarray', 
                 u_x: 'np.ndarray'=None, u_y: 'np.ndarray'=None, B: 'np.ndarray'=None):
        
        self.x = x0                     # State vector

        if u_x == 0 or u_y == None:     # Control vector
            self.u = np.zeros((2, 1))
        else:
            self.u = np.array([[u_x],    
                               [u_y]])

        self.P = P0                     # Covariance matrix

        self.A = A                      # State-transition model
        if B == None:                   # Control input model
            self.B = np.zeros((self.A.shape[0], self.u.shape[0]))  
        else:
            self.B = B

        self.C = C                      # Measurement model

        self.Q = Q                      # Process noise covariance matrix
        self.R = R                      # Measurement noise covariance matrix


    def predict(self):
        self.x = np.dot(self.A, self.x) + np.dot(self.B, self.u)
        self.P = np.dot(np.dot(self.A, self.P), self.A.T) + self.Q
        return self.x

    def correct(self, meas: 'np.ndarray'):
        inv = np.dot(np.dot(self.C, self.P), self.C.T) + self.R
        K = np.dot(np.dot(self.P, self.C.T), np.linalg.inv(inv))
        IKC = np.eye(self.A.shape[1]) - np.dot(K, self.C)

        self.x = self.x + np.dot(K, (meas - np.dot(self.C, self.x)))
        self.P = np.dot(np.dot(IKC, self.P), IKC.T) + np.dot(np.dot(K, self.R), K.T)

        return self.x
    
