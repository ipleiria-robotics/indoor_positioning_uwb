'''
Generates graphs and file with the values from the ranges analysis
Requires:
    - true position
    - filename with dataset to load
    - define index to read from the dateset to load
    - anchors coordinates file to load
    - define start and end limits of ranges to analyse
    - start and end number of combinations to use
Output:
    - save the boxplot and historgrams of the ranges error analysis
    - save on file the stats from the analysis on file Ranges_SLI.csv
'''

import numpy as np
from numpy import linalg as lin_a
import matplotlib.pyplot as plt
import sys
sys.path.append(".")
sys.path.append("..")
from utilities import loading_data as dataset


def ranges_analisys(index_ranges, filename, anchors_filename, position, start, end, start_comb, end_comb, saving_directory_filename, limit_plot, num_bins):
    # loading data
    data = dataset.LoadingData(position, filename, anchors_filename, index_ranges, start, end, start_comb, end_comb)
    dataSet = data.loadDataWithoutHeaders()
    anchors_coordinates = data.loadAnchorsCoordinates()    

    #define the variable for the stats and data analysis
    trueRanges = np.zeros(len(data.indexes))
    error_ranges = np.zeros([data.end-data.start, len(data.indexes)])
    rmse_ranges = np.zeros([data.end-data.start, len(data.indexes)])
    avg_error = np.zeros(len(data.indexes))
    std_error = np.zeros(len(data.indexes))
    avg_rmse = np.zeros(len(data.indexes))
    std_rmse = np.zeros(len(data.indexes))    

    #vars to auxiliary work
    header = ""
    header_rms = ""
    data_to_save = np.zeros([data.end-data.start, len(data.indexes)*2])
    

    # obtain the true ranges from the position and determine of error and rms error
    # determine the average, std and average of rmse
    for i in range(0, len(trueRanges)):
        trueRanges[i] = int(lin_a.norm(data.true_position - anchors_coordinates[i, :]))
        error_ranges[:, i] = trueRanges[i] - dataSet[:, i]
        rmse_ranges[:, i] = np.sqrt((trueRanges[i] - dataSet[:, i])**2)
        avg_error[i] = np.nanmean(error_ranges[:, i])
        std_error[i] = np.nanstd(error_ranges[:, i])
        avg_rmse[i] = np.nanmean(rmse_ranges[:, i])
        std_rmse[i] = np.nanstd(rmse_ranges[:, i])
        header = header + f"error_{i},"
        header_rms = header_rms + f"rms_{i},"
        data_to_save[:,i] = error_ranges[:,i]
        data_to_save[:,i+len(trueRanges)] = rmse_ranges[:,i]


    # histogram
    for index in range(0, len(data.indexes)):
        x = error_ranges[:, [index]]
        mu = avg_error[index]
        sigma = std_error[index]
        max_value = limit_plot
        num_bins = num_bins
        # n, bins, patches = plt.hist(x, num_bins, facecolor='blue', edgecolor='black' ,alpha=0.5, label="Erro")
        plt.hist(x, num_bins, facecolor='blue', edgecolor='black' ,alpha=0.5, label="Erro")
        plt.xlabel('Erro[mm]')
        plt.ylabel('Frequência')
        plt.title(f'Erro âncora {index}')
        # plt.axvline(mu, color='r', label=f'Média={int(mu)}[mm]\nDesvio padrão={int(sigma)}[mm]', linestyle='dashed')
        plt.axvline(mu, color='r', label="Média", linestyle='dashed')
        plt.grid()
        plt.legend()
        plt.subplots_adjust(left=0.15)
        plt.yticks(range(0, max_value, 100))
        save_filename = saving_directory_filename + (f"-{index}")
        plt.savefig(save_filename)
        # plt.show()
        plt.close()

    

    # boxplot plots
    red_circle = dict(markerfacecolor='red', marker='o', markeredgecolor='white')
    fig, axs = plt.subplots(1, len(data.indexes), figsize=(15,7))
    for i, ax in enumerate(axs.flat):
        x = error_ranges[:, [i]]
        x = x[~np.isnan(x)]
        ax.boxplot(x, flierprops=red_circle, notch=True, vert=True, patch_artist=True, capprops=dict(color="blue"))
        title_name = f"Erro âncora {i}"
        ax.yaxis.grid(True)
        ax.set_title(title_name, fontsize=10, fontweight='bold')
        ax.tick_params(axis='y', labelsize=10) 

    plt.tight_layout()
    save_filename = saving_directory_filename + ("-BoxPlot")
    # plt.savefig("Boxplot - Erro Distâncias")
    plt.savefig(save_filename)
    # plt.show()

    
    #saving data analysis on a csv file
    with open(saving_directory_filename, "w", encoding='UTF8') as file:
        # write the header
        main_header = header + header_rms + "\n"
        file.write(main_header)
        data_to_save_str = data_to_save.astype(str)
        data_to_save_str[data_to_save_str=='nan'] = ''
        np.savetxt(file, data_to_save, delimiter=',', fmt="%s")
        file.close()

    
    # printing the stats
    print(f"Starting Limit {data.start} Analysis")
    print(f"ENDING Limit {data.end} Analysis")
    print("Anchors Coordinates Loaded")
    print(anchors_coordinates)
    print("Position [x, y, z]")
    print(data.true_position)
    print("True Ranges")
    print(trueRanges)
    print("Média Erro:")
    print(avg_error)
    print("STD Erro:")
    print(std_error)
    print("RMSE:")
    print(avg_rmse)
    