import sys
sys.path.append(".")
sys.path.append("..")
from tools import sli_pos_plot as sli_plot
import os


index_ranges = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]

index = 0
rang_set_index = 2
comb_index = 3
pos_index = [5, 6, 7]
error_index = [8, 9, 10]
error_rms_index = [11, 12, 13]
rms_norm_ind = 14


filename = "Pos_ITLS_SLI_pos2_teste3"
anchors_coords = "anchor_coordinates"
position = [2091, 989, 727]
# position = [0, 0, 0]
comb_to_plot = 5  # define the combinations to plot
combination_search = "03457"
start = 0
end = 5000
start_comb = 8
end_comb = 8
save_datafolder = "position2\\plots"
saving_filename = "Erro Posição Teste 3"


iterative_process = None  # define if iterative plot is shown

#default config's - no need to change
parent_directory = os.getcwd()
dataset_directory = os.path.dirname(parent_directory)
filename = parent_directory + "\\position2\\position2_dataset\\" + filename
anchors_filename = dataset_directory + "\\" + anchors_coords
saving_directory = parent_directory + "\\" + save_datafolder
saving_directory_filename = saving_directory + "\\" + saving_filename


if saving_filename:
    if not os.path.exists(saving_directory):
        print("Directory you pretend created!")
        os.makedirs(saving_directory)

    sli_plot.sli_plot_run(index_ranges, index, rang_set_index, comb_index, pos_index, error_index, error_rms_index, rms_norm_ind, \
    filename, anchors_filename, position, comb_to_plot, combination_search, start, end, start_comb, end_comb, iterative_process, saving_filename, saving_directory_filename)
else:
    print("Filename is not defined! Please define a file to save data.")

