import sys
sys.path.append(".")
sys.path.append("..")
from tools import sli_pos_plot as sli_plot
import os

# user config's - ONLY THING TO CHANGE
filename = "Pos_ITLS_SLI_teste2"
anchors_coords = "anchor_coordinates"
position = [12861, 2983, 1658]
combination_search = "23467"
start = 0
end = 5000
save_datafolder = "position1\\plots"
saving_filename = "Erro Posição Teste 2"

# collumn indexes definition here
ranges_col = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
rang_set_index = 2
comb_index = 3
pos_index = [5, 6, 7]
error_index = [8, 9, 10]
error_rms_index = [11, 12, 13]
rms_norm_ind = 14


#default config's - NO NEED TO CHANGE
parent_directory = os.getcwd()
dataset_directory = os.path.dirname(parent_directory)
filename = parent_directory + "\\position1\\position1_dataset\\" + filename
anchors_filename = dataset_directory + "\\" + anchors_coords
saving_directory = parent_directory + "\\" + save_datafolder
saving_directory_filename = saving_directory + "\\" + saving_filename


if saving_filename:
    if not os.path.exists(saving_directory):
        print("Directory you pretend created!")
        os.makedirs(saving_directory)

    sli_plot.sli_plot_run(ranges_col, comb_index, pos_index, error_index, error_rms_index, rms_norm_ind, \
    filename, anchors_filename, position, combination_search, start, end, 0, 0, saving_filename, saving_directory_filename)
else:
    print("Filename is not defined! Please define a file to save data.")