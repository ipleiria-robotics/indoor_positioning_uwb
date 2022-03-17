'''
Script responsible to obtain dataset generated of positions estimated 
and analyse it (after the python generate script run)
@parameters:
    ranges_col - array with the indexes of all collumns
    comb_index - index of the coombination number collumn from
    pos_index - array with the index of position (x,y,z) collumns
    error_index - array with the index  of the positoin error (x,y,z) collumns
    error_rms_index - array with the index of the position rms error (x,y,z) collumns
    rms_norm_ind - index with the error normative collumn 
    filename - directrory and filename to load the generated data file
    anchors_coords - directory and filename to load the anchors coordinates file
    position - real position x y and z for the test
    comb_to_plot - define here the combination anchors 
    combination_search - string with anchors combination to analayse - if None all anchors will be used - min 4
    start - define the starting line to load teh data from the generated file
    end - define the ending line to load teh data from the generated file
    start_comb - Not used here
    end_comb -  Not used here
    saving_filename - filename to save the plots generated
    folder_to_save_plot - folder path where the plots will be saved
'''

from utilities import sli_gdop as gdop
from utilities import loading_data as dataset
from cProfile import label
from collections import Counter
from turtle import color
import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append(".")
sys.path.append("..")

# iter,timestamp,range_set,num_comb,combination,pox_x,pos_y,pos_z,error_x,error_y,error_z,rms_x,rms_y,rms_z,rms_norm,hdop,vdop,pdop
# ranges_col = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]


def sli_plot_run(ranges_col, comb_index, pos_index, error_index, error_rms_index, rms_norm_ind,
                 filename, anchors_coords, position, combination_search, start, end, start_comb, end_comb, saving_filename, folder_to_save_plot):

    #validates the number of anchors to use
    if combination_search is not None:
        comb_to_plot = len(combination_search)
    else:
        comb_to_plot = 8

    # loading data
    data = dataset.LoadingData(position, filename, anchors_coords, ranges_col, start, end, start_comb, end_comb)
    dataSet = data.loadingPosDataWithCondition(comb_to_plot, combination_search)
    anchors_coordinates = data.loadAnchorsCoordinates()

    # indexes = dataSet[:, index].astype(int)
    combinations = dataSet[:, comb_index].astype(int)
    indexes_result = np.where(combinations == comb_to_plot)
    # ranges_set = np.take(dataSet[:, rang_set_index].astype(float), indexes_result)
    x_points = np.take(dataSet[:, error_index[0]].astype(float), indexes_result)
    y_points = np.take(dataSet[:, error_index[1]].astype(float), indexes_result)
    z_points = np.take(dataSet[:, error_index[2]].astype(float), indexes_result)
    # hdop_points = np.take(dataSet[:, 15].astype(float), indexes_result)
    # hdop_points = np.take(dataSet[:, 16].astype(float), indexes_result)
    # hdop_points = np.take(dataSet[:, 17].astype(float), indexes_result)

    # stats calculations
    avg_x = np.average(dataSet[:, pos_index[0]].astype(float))
    avg_error_x = np.average(dataSet[:, error_index[0]].astype(float))
    std_error_x = np.std(dataSet[:, error_index[0]].astype(float))
    avg_rms_x = np.average(dataSet[:, error_rms_index[0]].astype(float))
    error_x_max = np.max(dataSet[:, error_index[0]].astype(float))
    error_x_min = np.min(dataSet[:, error_index[0]].astype(float))

    avg_y = np.average(dataSet[:, pos_index[1]].astype(float))
    avg_error_y = np.average(dataSet[:, error_index[1]].astype(float))
    std_error_y = np.std(dataSet[:, error_index[1]].astype(float))
    avg_rms_y = np.average(dataSet[:, error_rms_index[1]].astype(float))
    error_y_max = np.max(dataSet[:, error_index[1]].astype(float))
    error_y_min = np.min(dataSet[:, error_index[1]].astype(float))

    avg_z = np.average(dataSet[:, pos_index[2]].astype(float))
    avg_error_z = np.average(dataSet[:, error_index[2]].astype(float))
    std_error_z = np.std(dataSet[:, error_index[2]].astype(float))
    avg_rms_z = np.average(dataSet[:, error_rms_index[2]].astype(float))
    error_z_max = np.max(dataSet[:, error_index[2]].astype(float))
    error_z_min = np.min(dataSet[:, error_index[2]].astype(float))

    norm_rms = np.average(dataSet[:, rms_norm_ind].astype(float))

    print(f"Média x: {avg_x: .0f} Média Erro x: {avg_error_x: .0f} STD x:{std_error_x: .0f} RMSE x:{avg_rms_x: .0f} MAX x:{error_x_max: .0f} MIN x:{error_x_min: .0f}")
    print(f"Média y: {avg_y: .0f} Média Erro y: {avg_error_y: .0f} STD y:{std_error_y: .0f} RMSE y:{avg_rms_y: .0f} MAX y:{error_y_max: .0f} MIN y:{error_y_min: .0f}")
    print(f"Média z: {avg_z: .0f} Média Erro z: {avg_error_z: .0f} STD z:{std_error_z: .0f} RMSE z:{avg_rms_z: .0f} MAX z:{error_z_max: .0f} MIN z:{error_z_min: .0f}")
    print(f"RMS Overall: {norm_rms}")

    anchors_seleted = []
    if not combination_search == None:
        for a in combination_search:
            anchors_seleted.append(anchors_coordinates[int(a), :])
    else:
        anchors_seleted = anchors_coordinates

    hdop, vdop, pdop = gdop.gdop_calculatio(position, anchors_seleted)

    print(f"HDOP:{hdop} VDOP:{vdop} PDOP:{pdop}")

    # plotting data 3D and projections on 2D
    fig = plt.figure()
    ax = fig.suptitle(f"{saving_filename} 3D - {comb_to_plot} âncoras")
    ax = fig.add_subplot(111, projection='3d')
    scatter = ax.scatter(x_points, y_points, z_points, color='red', alpha=0.3, label="Erro xyz")
    # textstr = f"\nX coord -> Avg={avg_error_x: .0f} std={std_error_x: .0f} rms={avg_rms_x: .0f} max={error_x_max: .0f} min={error_x_min: .0f}\n" \
    #             f"Y coord -> Avg={avg_error_y: .0f} std={std_error_y: .0f} rms={avg_rms_y: .0f} max={error_y_max: .0f} min={error_y_min: .0f}\n" \
    #             f"Z coord -> Avg={avg_error_z: .0f} std={std_error_z: .0f} rms={avg_rms_z: .0f} max={error_z_max: .0f} min={error_z_min: .0f}"
    # ax.legend(*scatter.legend_elements(), loc="upper right", title="Erro 3D stats[mm]:" + textstr)

    ax.legend()
    # ax.scatter(position[0], position[1], position[2], marker='*', label=f"Ponto de referência\n{position}", color="black")
    ax.set_xlabel('X [mm]')
    ax.set_ylabel('Y [mm]')
    ax.set_zlabel('Z [mm]')
    ax.grid()
    # ax.legend()
    # ax.view_init(25, -124)
    ax.view_init(45, 45)
    plt.gca().set_aspect('auto', adjustable='box')
    plt.gca().set(zlim=(error_z_min, error_z_max))
    # plt.show()
    # fig.savefig("error_pos.png",dpi=600)
    fig.savefig(folder_to_save_plot+"_error_pos_3d.png")

    #Axis projection
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
    fig.suptitle(f'{saving_filename} 2D - {comb_to_plot} âncoras')
    scatter = ax1.scatter(x_points, y_points, color='red', alpha=0.3, label="Erro xy")
    # ax1.scatter(position[0], position[1], marker='*', label=f"Ponto de referência\n{position}", color="black")
    # ax1.legend(*scatter.legend_elements(), loc="lower left", title="Erro XY")
    ax1.set_xlabel("X [mm]")
    ax1.set_ylabel("Y [mm]")
    ax1.axis('equal')
    ax1.grid()
    ax1.legend()

    scatter2 = ax2.scatter(x_points, z_points, color='red', alpha=0.3, label="Erro xz")
    # ax2.scatter(position[0], position[2], marker='*', label=f"Ponto de referência\n{position}", color="black")
    # ax2.legend(*scatter.legend_elements(), loc="lower left", title="Erro XZ")
    ax2.set_xlabel("X [mm]")
    ax2.set_ylabel("Z [mm]")
    ax2.axis('equal')
    ax2.grid()
    ax2.legend()

    scatter3 = ax3.scatter(y_points, z_points, color='red', alpha=0.3, label="Erro yz")
    # ax3.scatter(position[1], position[2], marker='*', label=f"Ponto de referência\n{position}", color="black")
    # ax3.legend(*scatter.legend_elements(), loc="lower left", title="Erro YZ")
    ax3.set_xlabel("Y [mm]")
    ax3.set_ylabel("Z [mm]")
    ax3.axis('equal')
    ax3.grid()
    ax3.legend()
    # fig.savefig("error_pos_axis.png",dpi=600)
    # plt.gca().set_aspect('auto', adjustable='box')
    plt.show()

    fig.savefig(folder_to_save_plot+"_axis_proj.png")
