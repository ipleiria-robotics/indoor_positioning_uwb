import sys
sys.path.append(".")
from tools import sli_pos_move as mov_test
import os

#initial configs necessary to fill
encoder_filename = "Pos_encoder_fast"
dataset_filename = "Pos_ITLS_SLI_move_fast"
save_plot_name = "Erro 3D fast"
anchors_coordinates_filename = "anchor_coordinates"
starting_coordinate = [6703, 2354, 888]
ending_coordinate = [12210, 2371, 894]

 # define the index from the file to obtain positions
# iter,timestamp,range_set,num_comb,combination,pox_x,pos_y,pos_z,error_x,error_y,error_z,rms_x,rms_y,rms_z,rms_norm,hdop,vdop,pdop
index_ranges = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
line_index = 0
timestamp_index = 1
range_set_index = 2
combinations_index = 3
pos_index = [5, 6, 7]
position = None
comb_to_plot = 8  # define the combinations to plot
combination_search = None
start = 0
end = 5000
start_comb = 8
end_comb = 8


#default configs - dont need to change unless folders are moved
directory = os.getcwd()
dataset_directory = os.path.dirname(directory)
dataset_folder = directory + "\\movement_dataset\\"+ dataset_filename
encoder_folder = directory + "\\encoder_dataset\\"+ encoder_filename
anchors_file = dataset_directory + "\\" + anchors_coordinates_filename
folder_to_save_plot = directory + "\\plots\\" + save_plot_name


mov_test.run_moving_script(encoder_folder, dataset_folder, anchors_file, starting_coordinate, ending_coordinate, index_ranges, line_index, timestamp_index, range_set_index, combinations_index, pos_index, position, comb_to_plot, combination_search, start, end, start_comb, end_comb, folder_to_save_plot)
