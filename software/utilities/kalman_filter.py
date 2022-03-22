'''
    KalmanFilter.py
'''

import numpy as np


# kalman filter class
class KalmanFilter:
    def __init__(self, _dt, _std_acc, _std_pos):
        #definicao do tempo
        self.dt = _dt
        #devio padrao do acelerometro = 0
        self.std_acc = _std_acc
        #desvio padrao da posicao
        self.std_pos = _std_pos
        #matrox de estado
        self.X = np.array([[0],
                           [0],
                           [0],
                           [0],
                           [0],
                           [0]])

        self.A = np.array([[1, 0, 0, self.dt, 0, 0],
                           [0, 1, 0, 0, self.dt, 0],
                           [0, 0, 1, 0, 0, self.dt],
                           [0, 0, 0, 1, 0, 0],
                           [0, 0, 0, 0, 1, 0],
                           [0, 0, 0, 0, 0, 1]])

        self.P = np.eye(self.A.shape[1])

        self.B = np.matrix([[(self.dt ** 2) / 2, 0, 0],
                            [0, (self.dt ** 2) / 2, 0],
                            [0, 0, (self.dt ** 2) / 2],
                            [self.dt, 0, 0],
                            [0, self.dt, 0],
                            [0, 0, self.dt]])

        self.H = np.array([[1, 0, 0, 0, 0, 0],
                           [0, 1, 0, 0, 0, 0],
                           [0, 0, 1, 0, 0, 0]])

        self.Q = np.matrix([[(self.dt ** 4) / 4, 0, 0, (self.dt ** 3) / 2, 0, 0],
                            [0, (self.dt ** 4) / 4, 0, 0,
                             (self.dt ** 3) / 2, 0],
                            [0, 0, (self.dt ** 4) / 4, 0,
                             0, (self.dt ** 3) / 2],
                            [(self.dt ** 3) / 2, 0, 0, self.dt ** 2, 0, 0],
                            [0, (self.dt ** 3) / 2, 0, 0, self.dt ** 2, 0],
                            [0, 0, (self.dt ** 3) / 2, 0, 0, self.dt ** 2]]) * self.std_acc ** 2

        self.U = np.array([[0.0], [0.0], [0.0]])

        self.Y = np.array([0, 0, 0, 0, 0, 0])

        self.R = np.array([[self.std_pos, 0, 0],
                           [0, self.std_pos, 0],
                           [0, 0, self.std_pos]])

    # predict
    def predict(self, X, P, A, Q, B, U):
        X = np.dot(A, X) + np.dot(B, U)
        # P = np.dot(A, np.dot(P, A.T)) + Q
        P = np.dot(A, np.dot(P, A.T)) + Q
        return(X, P)

    # update
    def update(self, X, P, Z, H, R):
        Y = Z - np.dot(H, X)  # H*X -> Y
        IS = R + np.dot(H, np.dot(P, H.T))  # (H*P*H.T) + R -> K gain
        K = np.dot(P, np.dot(H.T, np.linalg.inv(IS)))  # kalman gain
        X = X + np.dot(K, Y)
        I = np.eye(H.shape[1])
        P = np.dot((I-np.dot(K, H)), P)  # (I - K*H)*P
        return (X, P, K)


'''
Example to use right down 
'''
# if __name__ == "__main__":
# def kalman_filter(pos, acc, time_diff):
#     # dt = 0.01
#     # std_acc = 0
#     # dt = time_diff
#     # kf = KalmanFilter(dt, std_acc)
#
#     # for i, pos in enumerate(pos_x_y_z_read):
#     (kf.X, kf.P) = kf.predict(kf.X, kf.P, kf.A, kf.Q, kf.B, kf.U)
#     (kf.X, kf.P, kf.K) = kf.update(kf.X, kf.P, kf.Y, kf.H, kf.R)
#     multiplier = 0
#     pos_x = pos[0]+(i*multiplier)
#     pos_y = pos[1]+(i*multiplier)
#     pos_z = pos[2]+(i*multiplier)
#
#     vel_x = (pos_x - kf.X[0, 0])/dt
#     vel_y = (pos_y - kf.X[0, 1])/dt
#     vel_z = (pos_z - kf.X[0, 2])/dt

# print(f"{i} -> pos = {pos_x}, {pos_y}, {pos_z}")
# print(f"velocity = {vel_x}, {vel_y}, {vel_z}")
# vel_x = 0
# vel_y = 0
# Y = np.array([pos[0], pos[1], pos[2], 0, 0, 0])
# kf.Y = np.array([pos_x, pos_y, pos_z, vel_x, vel_y, vel_z])
#
# print(f"{int(kf.X[0, 0])},{int(kf.X[0, 1])},{int(kf.X[0, 2])}")
# # input()


# dt = 0.01
# std_acc = 0
#
# kf = KalmanFilter(dt, std_acc)

# for i, pos in enumerate(pos_x_y_z_read):
#     (kf.X, kf.P) = kf.predict(kf.X, kf.P, kf.A, kf.Q, kf.B, kf.U)
#     (kf.X, kf.P, kf.K) = kf.update(kf.X, kf.P, kf.Y, kf.H, kf.R)
#
#     multiplier = 0
#     pos_x = pos[0] + (i * multiplier)
#     pos_y = pos[1] + (i * multiplier)
#     pos_z = pos[2] + (i * multiplier)
#
#     vel_x = (pos_x - kf.X[0, 0]) / dt
#     vel_y = (pos_y - kf.X[0, 1]) / dt
#     vel_z = (pos_z - kf.X[0, 2]) / dt
#
#     kf.Y = np.array([pos_x, pos_y, pos_z, vel_x, vel_y, vel_z])
#
#     print(f"{int(kf.X[0, 0])},{int(kf.X[0, 1])},{int(kf.X[0, 2])}")


# https://www.intechopen.com/chapters/63164
# https://dsp.stackexchange.com/questions/26115/kalman-filter-to-estimate-3d-position-of-a-node
# https://pt.wikipedia.org/wiki/Filtro_de_Kalman
# https://github.com/balzer82/Kalman