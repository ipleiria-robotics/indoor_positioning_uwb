'''

'''
import numpy as np
import itertools as ite
from numpy import linalg as LA
import sys
sys.path.append(".")
sys.path.append("..")
from utilities import sli_algorithms as trilateration
from utilities import loading_data as dataset
from utilities import sli_gdop as gdop


# define the index from the file to obtain ranges
# index_load = [4, 18, 32, 46, 60, 74, 88, 102]
# index_load = [4, 8, 12, 16, 20, 24, 28, 32]  # move
# filename = "\data_test\\128_move_fast"
# anchors_coords = "\\anchor_coordinates"
# position = [0, 0, 0]
# start = 0
# end = 1
# start_comb = 4
# end_comb = 8

def run_itls(index_load, filename, anchors_coords, position, start, end, start_comb, end_comb, saving_directory):
    # loading data
    data = dataset.LoadingData(position, filename, anchors_coords, index_load, start, end, start_comb, end_comb)
    dataSet = data.loadDataWithoutHeaders()
    anchors_coordinates = data.loadAnchorsCoordinates()
    true_position = data.true_position 
    data_timestamps = dataset.LoadingData(position, filename, anchors_coords, [0], start, end, start_comb, end_comb)
    timestamps = data_timestamps.loadDataWithoutHeaders()
    
    # fill combination
    if data.start_comb <= data.end_comb:
        combination_all = np.arange(data.start_comb, data.end_comb+1)
    else:
        combination_all = np.array([end_comb])


    # init position for the itls method
    pos_init = [0, 0, 0]

    # define the variable for the stats and data analysis
    pos = np.zeros(3)
    error_pos = np.zeros([data.end-data.start, len(data.indexes)])
    rmse_pos = np.zeros([data.end-data.start, len(data.indexes)])
    avg_pos = np.zeros(len(data.indexes))
    std_pos = np.zeros(len(data.indexes))
    avg_rmse = np.zeros(len(data.indexes))
    std_rmse = np.zeros(len(data.indexes))

    # vars to auxiliary work
    header = "iter,timestamp,range_set,num_comb,combination,pox_x,pos_y,pos_z,error_x,error_y,error_z,rms_x,rms_y,rms_z,rms_norm,hdop,vdop,pdop\n"

    # runs the all ranges and combinations and store file
    with open(saving_directory, "w", encoding='UTF8') as file:
        file.write(header)
        counter = 0
        for index, data_row in enumerate(dataSet):
            for number_combination in combination_all:
                for combination in ite.combinations(data.ranges_order, number_combination):
                    ranged_combined = np.take(data_row, combination)
                    anchors_combined = np.take(anchors_coordinates, combination, axis=0)
                    if not np.isnan(ranged_combined).any():
                        timestamp_val = str(timestamps[index])
                        result = (trilateration.iterative_least_square(ranged_combined, anchors_combined, pos_init))
                        result = result.astype(int)                        
                        hdop, vdop, pdop = gdop.gdop_calculatio(result, anchors_combined)

                        error = true_position - result
                        error_rms = (np.sqrt(error**2)).astype(int)
                        norm_rms = int(LA.norm(error_rms))
                        print(index, timestamp_val, number_combination, str(combination), result, error, error_rms, norm_rms, hdop, vdop, pdop)

                        aux_to_save = str(counter) + "," + timestamp_val + "," + str(index) + "," + \
                            str(number_combination) + ",'" + \
                            np.array2string(np.array(combination), precision=0, separator="") + "'," + \
                            np.array2string(result, precision=0, separator=',') + "," + \
                            np.array2string(error, precision=0, separator=',') + "," + \
                            np.array2string(error_rms, precision=0, separator=',') + "," + str(norm_rms) + "," + \
                            str(hdop) + "," + str(vdop) + "," + str(pdop) + "\n"

                        aux_to_save = aux_to_save.replace("[", "").replace("]", "")
                        file.write(aux_to_save)
                        counter += 1

    file.close()
