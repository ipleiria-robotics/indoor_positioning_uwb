import sys
sys.path.append(".")
sys.path.append("..")
from utilities import sli_pos_itls as sli_itls
import os

# user config's - ONLY THING TO CHANGE
filename = "128_move_slow" # filename with the dataset to load ranges data
anchors_coords = "anchor_coordinates" # filename to load anchors coordinates
start = 0 # starting line to use data from the file loaded
end = 1 # ending line to use data from the file loaded
start_comb = 4 # starting number of anchors combination to load from dataset file(min 4 anchors)
end_comb = 8 # ending number of anchors combination to load from dataset file(max 8 anchors)
save_datafolder = "movement_dataset" # folder where generated data will be saved
saving_filename = "teste" # filename were the generated will be saved
pos_init = [0,0,0] # init position where the iterative least-square algorithm will start

#default config's - NO NEED TO CHANGE
index_load = [4, 8, 12, 16, 20, 24, 28, 32]  # static file collumn indexes
position = [0, 0, 0] # no need
parent_directory = os.getcwd()
dataset_directory = os.path.dirname(parent_directory)
filename = dataset_directory + "\\dataset\\" + filename
anchors_filename = dataset_directory + "\\" + anchors_coords
saving_directory = parent_directory + "\\" + save_datafolder
saving_directory_filename = saving_directory + "\\" + saving_filename


if saving_filename:
    if not os.path.exists(saving_directory):
        print("Directory you pretend created!")
        os.makedirs(saving_directory)

    sli_itls.run_itls(index_load, filename, anchors_filename, position, start, end, start_comb, end_comb, saving_directory_filename, pos_init)
else:
    print("Filename is not defined! Please define a file to save data.")
