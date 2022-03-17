import sys
sys.path.append(".")
sys.path.append("..")
from tools import sli_ranges as sli_rng
import os

# user config's - ONLY THING TO CHANGE
index_load = [4, 18, 32, 46, 60, 74, 88, 102]  # static file indexes array wich are the ranges collumns
filename = "128_nlos_pos2" # filename containing the dataset to load
anchors_coords = "anchor_coordinates" # filename for the anchors coordinates dataset
position = [2091, 989, 727] # real position for this test
start = 0 # start loading line from dataset
end = 5000 # end loading line from dataset
start_comb = 4 # combination of anchors to start (min 4)
end_comb = 8 # combination of anchors to end (max 8)
save_datafolder = "position2\\plots" # folder path to save the generated data
saving_filename = "Erro Distância Teste 3" # filename to save the generated data

# Histogram properties
max_limit = 400
number_bins = 70 

#default config's - NO NEED TO CHANGE
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
