import sys
sys.path.append(".")
sys.path.append("..")
from tools import sli_ranges as sli_rng
import os


# user config's - change depending on the needs
index_load = [4, 18, 32, 46, 60, 74, 88, 102]  # static file indexes
filename = "128_nlos_pos1"
anchors_coords = "anchor_coordinates"
position = [12861, 2983, 1658]
start = 0
end = 5000
start_comb = 4
end_comb = 8
save_datafolder = "position1\\plots"
saving_filename = "Erro Distância Teste 2"
#histogram properties
max_limit = 400
number_bins = 70 


#default config's - no need to change
parent_directory = os.getcwd()
dataset_directory = os.path.dirname(parent_directory)
filename = dataset_directory + "\\dataset\\" + filename
anchors_filename = dataset_directory + "\\" + anchors_coords
saving_directory = parent_directory + "\\" + save_datafolder
saving_directory_filename = saving_directory + "\\" + saving_filename

if not os.path.exists(saving_directory):
    print("Directory you pretend created!")
    os.makedirs(saving_directory)

sli_rng.ranges_analisys(index_load, filename, anchors_filename, position, start, end, start_comb, end_comb, saving_directory_filename, max_limit, number_bins)
