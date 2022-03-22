import utilities.sli_algorithms as algorithm
import numpy as np
from numpy import linalg as lin_a

posInit = [0, 0, 0]
TAG_POSITION = [12861, 2983, 1658]
#6486, 1351, 899
#2091, 989, 727

ranges = [12881,6667,10366,3998,13196,3472,7242,9914]
# 7217, 2939, 16423, 8794, 8034, 8036, 4662, 15875 start_pos
# 2930., 5996.,22318.,13622., 6396.,12793., 7815.,20342 pos 2


# anchors coordinates
acoord = np.array([
    # new dataset
    [0, 412, 2888],
    [7185, 127, 2875],
    [22364, 6688, 2854],
    [14118, 6643, 2889],
    [321, 6663, 2888],
    [14022, 67, 2888],
    [6743, 6700, 2844],
    [22156, 0, 2876]
])

combination = [0, 1, 2, 3, 5, 6, 7]


# used to return the selected distances given an index to select them
def obtain_distances_with_index(distances, index_array):
    dist_array = np.zeros(len(index_array))
    for index, ele in enumerate(index_array):
        dist_array[index] = distances[ele]
    return dist_array

# used to return the selected 3D anchors coords given an index to select them
def obtain_anchors_coord_with_index(anchors_coord_array, index_array):
    anchors_array = []
    if index_array[0] != index_array[1]:
        anchors_array = np.zeros((len(index_array), 3))
        for ind, val in enumerate(index_array):
            anchors_array[ind] = anchors_coord_array[val]
    return anchors_array



distances_selected = obtain_distances_with_index(ranges, combination)
anchors_selected = obtain_anchors_coord_with_index(acoord, combination)
position_calculated = algorithm.iterative_least_square(distances_selected, anchors_selected, posInit)
# position_calculated = algorithm.least_square(distances_selected, anchors_selected)


# calculate real distances
real_distances = []
error_distance = []
for i, c in enumerate(acoord):
    real_distances.append(int(lin_a.norm(c - TAG_POSITION)))
    error_distance.append(ranges[i] - int(lin_a.norm(c - TAG_POSITION)))


print(f"Posição real: {TAG_POSITION}")
print(f"Posição calculada: {position_calculated.astype(int)}")
print(f"Erro posição: {TAG_POSITION - position_calculated.astype(int)}")
print(f"Erro overall: {int(lin_a.norm(TAG_POSITION - position_calculated.astype(int)))}")
print(f"Distancia real: {real_distances}")
print(f"Distancia medida: {ranges}")
print(f"Erro distancias: {error_distance}")



