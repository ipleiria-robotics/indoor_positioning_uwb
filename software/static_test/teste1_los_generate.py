import sys
sys.path.append(".")
sys.path.append("..")
from utilities import sli_pos_itls as sli_itls
import os

# user config's - ONLY THING TO CHANGE
index_load = [4, 18, 32, 46, 60, 74, 88, 102]  # static file indexes array wich are the ranges collumns
filename = "128_los_pos1" # filename containing the dataset to load
anchors_coords = "anchor_coordinates" # filename for the anchors coordinates dataset
position = [12861, 2983, 1658] # real position for this test
start = 0 # start loading line from dataset
end = 1 # end loading line from dataset
start_comb = 4 # combination of anchors to start (min 4)
end_comb = 8 # combination of anchors to end (max 8)
save_datafolder = "position1\\position1_dataset" # folder path to save the generated data
saving_filename = "teste" # filename to save the generated data
pos_init = [0,0,0] # init position where the iterative least-square algorithm will start


#default config's - NO NEED TO CHANGE
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

print(saving_directory_filename)