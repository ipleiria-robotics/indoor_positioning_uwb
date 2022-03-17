import sys
sys.path.append(".")
from tools import sli_pos_move as mov_test
import os

# user config's - ONLY THING TO CHANGE
encoder_filename = "Pos_encoder_slow" #filename to load the encoder dataset of this test
dataset_filename = "Pos_ITLS_SLI_move_slow" # filname to load the dataset generated with the positions estimated
save_plot_name = "Erro 3D slow" # name for the plot to save
anchors_coordinates_filename = "anchor_coordinates" # filename for the anchors coordinates dataset
starting_coordinate = [6757, 2346, 884] # coordinate for the starting position
ending_coordinate = [12093, 2382, 890] # coordinate for the ending position
position = None
combination_search = None # string to define the anchros to use - use None will use all
start = 0 # starting line from wich data is loaded form the generated position file
end = 5000 # ending line from wich data is loaded form the generated position file
start_comb = 8 
end_comb = 8

# collumn indexes definition here
# iter,timestamp,range_set,num_comb,combination,pox_x,pos_y,pos_z,error_x,error_y,error_z,rms_x,rms_y,rms_z,rms_norm,hdop,vdop,pdop
index_ranges = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16] 
timestamp_index = 1
combinations_index = 3
pos_index = [5, 6, 7]


#default config's - NO NEED TO CHANGE
directory = os.getcwd()
dataset_directory = os.path.dirname(directory)
dataset_folder = directory + "\\movement_dataset\\" + dataset_filename
encoder_folder = directory + "\\encoder_dataset\\" + encoder_filename
anchors_file = dataset_directory + "\\" + anchors_coordinates_filename
folder_to_save_plot = directory + "\\plots\\" + save_plot_name


mov_test.run_moving_script(encoder_folder, dataset_folder, anchors_file, starting_coordinate, ending_coordinate, \
    index_ranges, timestamp_index, combinations_index, pos_index, position, \
        combination_search, start, end, start_comb, end_comb, folder_to_save_plot)
