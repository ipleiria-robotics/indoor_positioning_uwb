import math as op
import numpy as np


ANCHORS_0_ON_X = 0 # select the anchor that works as 0 referece on X axis
ANCHORS_0_ON_Y = 7 # select the anchor that works as 0 referece on Y axis


COORDINATES = 3

title_coord = ["Anchor 0", "Anchor 1", "Anchor 2", "Anchor 3" ,"Anchor 4", "Anchor 5", "Anchor 6", "Anchor 7", 
    "Position 1", "Position 2 ", "Slow start point", "Slow end point", "Fast start point", "Fast end point" ]

# [range diag, V, Hz, h]
Coords = np.array([
    [3362, 69.6833, 300.4394, 1347],  # anchor 1 - amarela
    [8060, 87.8498, 372.8554, 1347],  # anchor 2 vermelha
    [22675, 95.7657, 9.2884, 1347],  # anchor 3 - azul
    [14588, 93.2569, 14.3621, 1347],  # anchor 4 - verde
    [3626, 72.0548, 93.3550, 1347],  # anchor 5 - laranja
    [14515, 93.2244, 385.1666, 1347],  # anchor 6 - preta
    [7674, 87.4947, 28.9076, 1347],  # anchor 7 - rosa
    [22488, 95.6680, 390.3180, 1347],  # anchor 8 - roxa
    [12892, 98.4616, 397.9438, 1347], # pos 1
    [3264, 112.1617, 345.8066, 1347], # pos 2
    [6874, 104.2829, 390.1796, 1347],  # move pos start slow
    [12165, 102.3920, 394.6645, 1347], # move pos end slow
    [6820, 104.2839, 390.1788, 1347],  # move pos start fast
    [12282, 102.3472, 394.6575, 1347]  # move pos end fasWWt
])

num_acoord = np.size(Coords, 0)
print(f"Number of measures: {num_acoord}")
result = np.zeros((num_acoord, COORDINATES))

for i in range(np.size(Coords, 0)):
    result[i, 0] = Coords[i, 0] * op.sin(((90 * Coords[i, 1]) / 100) * (op.pi) / 180) * op.cos(((90 * Coords[i, 2]) / 100) * (op.pi) / 180)
    result[i, 1] = Coords[i, 0] * op.sin(((90 * Coords[i, 1]) / 100) * (op.pi) / 180) * op.sin(((90 * Coords[i, 2]) / 100) * (op.pi) / 180)
    result[i, 2] = Coords[i, 0] * op.cos(((90 * Coords[i, 1]) / 100) * (op.pi) / 180) + Coords[i, 3]

result = result.astype(int)
result = np.array(result)
print("Coords:")
print(np.array2string(result, separator=','))

# matrix transformation
new_result = np.zeros((num_acoord, COORDINATES))
new_result = np.copy(result)

# X and Y value to correct coordinates
dist_x_correction = op.fabs(result[ANCHORS_0_ON_X, 0])
dist_y_correction = op.fabs(result[ANCHORS_0_ON_Y, 1])

last_result = np.zeros((num_acoord, COORDINATES))
last_result[:, 0] = new_result[:, 0] - dist_x_correction
last_result[:, 1] = new_result[:, 1] + dist_y_correction
last_result[:, 2] = new_result[:, 2]

print("Matrix Transformed form")
print(np.array2string(last_result, separator=','))

print("Matrix script form")
for a, i in enumerate(last_result):
    print(f"{int(i[0])}, {int(i[1])}, {int(i[2])} - {title_coord[a]}")
