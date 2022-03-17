import sys
sys.path.append(".")
sys.path.append("..")
from utilities import sli_pos_itls as sli_itls
import os

# user config's - change depending on the needs
index_load = [4, 18, 32, 46, 60, 74, 88, 102]  # static file indexes
filename = "128_los_pos1"
anchors_coords = "anchor_coordinates"
position = [12861, 2983, 1658]
start = 0
end = 1
start_comb = 4
end_comb = 8
save_datafolder = "position1\\position1_dataset"
saving_filename = "teste"


#default config's - no need to change
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

    sli_itls.run_itls(index_load, filename, anchors_filename, position, start, end, start_comb, end_comb, saving_directory_filename)
else:
    print("Filename is not defined! Please define a file to save data.")

print(saving_directory_filename)