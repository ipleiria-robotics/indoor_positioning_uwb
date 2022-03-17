'''
Generates a file with the positions determined with the number of combinations

Requires: 
    - true position
    - filename with dataset to load
    - define index to read from the dateset to load
    - anchors coordinates file to load
    - define start and end limits of ranges to analyse
    - start and end number of combinations to use
Output:
    - save data on a file
'''

import pandas as pd
import numpy as np
import SLI_Algorithms as trilateration
import itertools as ite
from numpy import linalg as LA
import LoadingData as dataset


# define the index from the file to obtain ranges
index_ranges = [4, 18, 32, 46, 60, 74, 88, 102]
filename = "\data_test\\128_los_pos1"
anchors_coords = "\\anchor_coordinates"
position = [12861, 2983, 1658]
start = 0
end = 10
start_comb = 3
end_comb = 3

data = dataset.LoadingData(position, filename, anchors_coords, index_ranges, start, end, start_comb, end_comb)
dataSet = data.loadDataWithoutHeaders()
anchors_coordinates = data.loadAnchorsCoordinates()

# fill combination
if data.start_comb <= data.end_comb:
    combination_all = np.arange(data.start_comb, data.end_comb+1)
else:
    combination_all = np.array([end_comb])

number_combination = 3

# define the variable for the stats and data analysis
pos = np.zeros(3)
error_pos = np.zeros([data.end-data.start, len(data.indexes)])
rmse_pos = np.zeros([data.end-data.start, len(data.indexes)])
avg_pos = np.zeros(len(data.indexes))
std_pos = np.zeros(len(data.indexes))
avg_rmse = np.zeros(len(data.indexes))
std_rmse = np.zeros(len(data.indexes))

#vars to auxiliary work
header = "range_set,num_comb,combination,pox_x,pos_y,pos_z,error_x,error_y,error_z,rms_x,rms_y,rms_z,rms_norm\n"


#runs the all ranges and combinations and store file
with open("Pos_FANGS_SLI", "w", encoding='UTF8') as file:
    file.write(header)
    for index, data_row in enumerate(dataSet):
        for combination in ite.permutations(data.ranges_order, number_combination):
            ranged_combined = np.take(data_row, combination)
            anchors_combined = np.take(
                anchors_coordinates, combination, axis=0)
            if not np.isnan(ranged_combined).any():
                result = trilateration.fangs_trilateration(ranged_combined, anchors_combined)
                error = data.true_position - result
                error_rms = np.sqrt(error**2)
                norm_rms = LA.norm(error_rms)
                print(index, number_combination, str(combination), result, error, error_rms, norm_rms)
                aux_to_save = str(index) + "," + \
                    str(number_combination) + ",'" + \
                    np.array2string(np.array(combination), separator="") + "'," + \
                    np.array2string(result, precision=2, separator=',') + "," + \
                    np.array2string(error, precision=2, separator=',') + "," + \
                    np.array2string(error_rms, precision=2, separator=',') + "," + "{0:.2f}".format(norm_rms) + "\n"

                aux_to_save = aux_to_save.replace("[", "").replace("]", "")
                file.write(aux_to_save)

file.close()