import numpy as np
import LoadingData as dataset
from numpy import linalg as LA


# define the index from the file to obtain ranges
index_ranges = [4, 18, 32, 46, 60, 74, 88, 102]
filename_ranges = "\data_test\\128_nlos_pos2"
index_pos = [1, 2, 3, 4, 5, 6]
filename_position = "\\Pos_ITLS_SLI_pos2"
anchors_coords = "\\anchor_coordinates"
position = [2091, 989, 727]
start = 0
end = 1
start_comb = 4
end_comb = 8

dataRange = dataset.LoadingData(position, filename_ranges, anchors_coords, index_ranges, start, end, start_comb, end_comb)
rangesSet = dataRange.loadDataWithoutHeaders()

dataPos = dataset.LoadingData(position, filename_position, anchors_coords, index_pos, start, end, start_comb, end_comb)
anchors_coordinates = dataPos.loadAnchorsCoordinates()
# print(dataPos.loadingPosDataFromRangeIter(140))
# print(anchors_coordinates)


# vars to auxiliary work
header = "i,rangeIter,range0,range1,range2,range3,range4,range5,range6,range7,n_comb,comb,x,y,z,range_cal0,range_cal1,range_cal2,range_cal3,range_cal4,range_cal5,range_cal6,range_cal7,res0,res1,res2,res3,res4,res5,res6,res7,res_used0,res_used1,res_used2,res_used3,res_used4,res_used5,res_used6,res_used7\n"


# runs the all ranges and combinations and store file
with open("Pos_ITLS_Residuals_SLI", "w", encoding='UTF8') as file:
    file.write(header)
    counter = 0
    for i, range in enumerate(rangesSet):
        pos_data = dataPos.loadingPosDataFromRangeIter(i)   
        for pos in pos_data:
            comb_number = pos[1]
            comb = pos[2]
            xyz = [int(pos[3]), int(pos[4]), int(pos[5])]
            calc_ranges = []
            residual = []
            res_used = []
            
            for j, anchor_pos in enumerate(anchors_coordinates):
                calc_ranges.append(int(LA.norm(anchor_pos - xyz)))
                residual.append(range[j] - calc_ranges[j])

            for p, val in enumerate(comb):
                if p > 0 and p < len(comb) - 1:
                    res_used.append(residual[int(val)])
                
            aux_to_save = str(counter) + "," + \
                str(i) + "," + \
                np.array2string(np.array(range), separator=",") + "," + \
                str(comb_number) + "," + \
                str(comb) + "," + \
                str(xyz) + "," + \
                str(calc_ranges) + "," + \
                str(residual) + "," + \
                str(res_used) + "\n"
            

            
            aux_to_save = aux_to_save.replace("[", "").replace("]", "")
            # print(aux_to_save)
            print(i, range, comb_number, comb, xyz, calc_ranges, residual, res_used)
            file.write(aux_to_save)
            counter += 1
            # input()

file.close()
