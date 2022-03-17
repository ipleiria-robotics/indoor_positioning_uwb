from threading import local
from dateutil import parser
import math as mth
from datetime import datetime
import csv
# import KalmanFilter as kalman
from numpy import linalg as lin_a
import numpy as np
import matplotlib.pyplot as plt

import sys
sys.path.append("..")
from utilities import loading_data as dataset


def run_moving_script(encoder_filename, filename, anchors_coords, startPoint, endPoint, index_ranges, line_index, timestamp_index, range_set_index, combinations_index, pos_index, position, comb_to_plot, combination_search, start, end, start_comb, end_comb, folder_to_save_plot):
    timestamp_encoder_load = []
    timestamp_data_load = []
    startPoint = np.array(startPoint)
    endPoint = np.array(endPoint)

    with open(encoder_filename, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            format = '%H:%M:%S.%f'
            datetime_str = datetime.strptime(row[0], format)
            timestamp_encoder_load.append(datetime_str.time().strftime('%d-%m-%Y %H:%M:%S.%f')[:])

    travel_distance = int(lin_a.norm(endPoint - startPoint))
    # print(f"True distance: {travel_distance} mm")

    pulses = len(timestamp_encoder_load)
    line_travel = np.linspace(startPoint, endPoint, pulses)

    # iterative_process = None  # define if iterative plot is shown

    # loading data
    data = dataset.LoadingData(position, filename, anchors_coords, index_ranges, start, end, start_comb, end_comb)
    dataSet = data.loadingPosDataWithCondition(comb_to_plot, combination_search)
    anchors_coordinates = data.loadAnchorsCoordinates()

    indexes = dataSet[:, line_index].astype(int)
    timestamp_loaded = dataSet[:, timestamp_index]
    combinations = dataSet[:, combinations_index].astype(int)
    indexes_result = np.where(combinations == comb_to_plot)
    ranges_set = np.take(dataSet[:, range_set_index].astype(float), indexes_result)
    x_points = np.take(dataSet[:, pos_index[0]].astype(float), indexes_result)[0]
    y_points = np.take(dataSet[:, pos_index[1]].astype(float), indexes_result)[0]
    z_points = np.take(dataSet[:, pos_index[2]].astype(float), indexes_result)[0]

    for data_t in timestamp_loaded:
        format = '%H:%M:%S.%f'
        test = datetime.strptime(data_t.replace("'", ""), format)
        timestamp_data_load.append(test.time().strftime('%d-%m-%Y %H:%M:%S.%f')[:])

    counter = 0
    before_val = None
    after_val = None
    dataXYZ = []
    dataRealXYZ = []
    last_index = 0
    t0_0 = 0
    t1_0 = 0
    first_timestamp = timestamp_encoder_load[0]
    last_timestamp = timestamp_encoder_load[-1]
    test_duration = parser.parse(last_timestamp) - parser.parse(first_timestamp)

    for ite, dat in enumerate(timestamp_encoder_load):
        for ite2 in range(last_index, len(timestamp_data_load)):
            if parser.parse(dat) == parser.parse(timestamp_data_load[ite2]):
                print(f"Value founded: {ite} - {ite2} - {parser.parse(dat) - parser.parse(timestamp_data_load[ite2])}")
                before_val = [x_points[ite2], y_points[ite2], z_points[ite2]]
                dataRealXYZ.append(line_travel[ite])
                dataXYZ.append(before_val)
                break

            elif parser.parse(dat) > parser.parse(timestamp_data_load[ite2]):
                print(f"Value before founded: {ite} - {ite2} - {parser.parse(dat) - parser.parse(timestamp_data_load[ite2])}")
                before_val = [x_points[ite2], y_points[ite2], z_points[ite2]]
                t0 = parser.parse(timestamp_data_load[ite2])
                t0_0 = parser.parse(dat) - parser.parse(timestamp_data_load[ite2])
                
            else:
                print(f"Value after  founded: {ite} - {ite2} - {parser.parse(timestamp_data_load[ite2]) - parser.parse(dat)}")
                print(f"Encoder timestamp:{parser.parse(dat)}")
                
                t1 = parser.parse(timestamp_data_load[ite2])
                t1_0 = parser.parse(timestamp_data_load[ite2]) - parser.parse(dat)
                # print(t0_0 / (t0_0 + t1_0))

                after_val = [x_points[ite2], y_points[ite2], z_points[ite2]]
                last_index = ite2 - 1
                print(before_val)
                print(after_val)
                distance_travel = mth.sqrt((after_val[0] - before_val[0])**2 + (after_val[1] - before_val[1])**2 + (after_val[2] - before_val[2])**2)
                distance_travel_x = after_val[0] - before_val[0]
                distance_travel_y = after_val[1] - before_val[1]
                distance_travel_z = after_val[2] - before_val[2]
                print(f"Distance travel: {distance_travel}")
                # print(f"Distance travel / 2: {distance_travel / 2}")
                print(f"Distance x: {distance_travel_x}, y:{distance_travel_y}, z:{distance_travel_z}")
                print(f"encoder position: {line_travel[ite]}")

                racio = t0_0 / (t0_0 + t1_0)
                print(f"racio %: {racio}")
                # racio_dist = racio * distance_travel
                # print(f"racio dist [mm]: {racio_dist}")
                dist_x_racio = racio * distance_travel_x
                dist_y_racio = racio * distance_travel_y
                dist_z_racio = racio * distance_travel_z
                print(f"x_travel:{dist_x_racio}, y_travel:{dist_y_racio}, z_travel:{dist_z_racio}")
                # mid_point = [before_val[0] + (after_val[0] - before_val[0]) / 2, before_val[1] + (after_val[1] - before_val[1]) / 2, before_val[2] + (after_val[2] - before_val[2]) / 2]                
                # mid_point = [before_val[0] + (racio_dist), before_val[1] + (racio_dist), before_val[2] + (racio_dist)]
                mid_point = [before_val[0] + dist_x_racio, before_val[1] + dist_y_racio, before_val[2] + dist_z_racio]
                print(f"ite: {ite} - mid_point: {mid_point}")
                
                dataRealXYZ.append(line_travel[ite])
                dataXYZ.append(mid_point)
                break

    dataXYZ = np.array(dataXYZ)
    dataRealXYZ = np.array(dataRealXYZ)
    # determine the error
    dataXYZ_error = np.array(dataRealXYZ - dataXYZ)
    # rms error

    dataXYZ_rms_error = []

    for real, meas in zip(dataRealXYZ, dataXYZ):
        dataXYZ_rms_error.append([mth.sqrt((real[0] - meas[0])**2), mth.sqrt((real[1] - meas[1])**2), mth.sqrt((real[2] - meas[2])**2)])

    dataXYZ_rms_error = np.array(dataXYZ_rms_error)

    # print(dataXYZ_error)
    # print(dataXYZ_rms_error)
    # print(dataXYZ_rms_error.shape)
    x_avg = int(np.average(dataXYZ_error[:, 0]))
    x_std = int(np.std(dataXYZ_error[:, 0]))
    x_rms = int(np.average(dataXYZ_rms_error[:, 0]))
    y_avg = int(np.average(dataXYZ_error[:, 1]))
    y_std = int(np.std(dataXYZ_error[:, 1]))
    y_rms = int(np.average(dataXYZ_rms_error[:, 1]))
    z_avg = int(np.average(dataXYZ_error[:, 2]))
    z_std = int(np.std(dataXYZ_error[:, 2]) )
    z_rms = int(np.average(dataXYZ_rms_error[:, 2]))

    print(f"True distance: {travel_distance} mm")    
    print(f"Time duration: {test_duration}")
    print(f"average X: {x_avg} - std X: {x_std} - rms error: {x_rms}")
    print(f"average Y: {y_avg} - std Y: {y_std} - rms error: {y_rms}")
    print(f"average Z: {z_avg} - std Z: {z_std} - rms error: {z_rms}")

    # plotting data 3D and projections on 2D
    fig = plt.figure()
    ax = fig.suptitle(f"Posição - 3D -> {comb_to_plot} âncoras")
    ax = fig.add_subplot(111, projection='3d')
    scatter = ax.scatter(dataXYZ[:, 0], dataXYZ[:, 1],dataXYZ[:, 2], color='red', alpha=0.2, label="Posições Estimadas")
    scatter = ax.scatter(dataRealXYZ[:, 0], dataRealXYZ[:, 1], dataRealXYZ[:, 2], marker='_', label="Posições Reais", color="blue", alpha=0.2)
    ax.legend(*scatter.legend_elements(), loc="lower left", title="Posições 3D")

    scatter = ax.scatter(startPoint[0], startPoint[1], startPoint[2],marker='*', label=f"Ponto inicial\n{startPoint}", color="black", s=100)
    scatter = ax.scatter(endPoint[0], endPoint[1], endPoint[2], marker='*', label=f"Ponto final\n{endPoint}", color="green", s=100)
    # if KALMAN_USAGE:
    #     scatter = ax.scatter(X_points_kalman, Y_points_kalman, Z_points_kalman, marker='*', label=f"KF", color="cyan")
    ax.set_xlabel('X [mm]')
    ax.set_ylabel('Y [mm]')
    ax.set_zlabel('Z [mm]')
    ax.grid()
    ax.legend(loc="best")
    ax.view_init(45, 45)
    plt.gca().set_aspect('auto', adjustable='box')
    save_name = f"_{comb_to_plot}_anc.png"
    fig.savefig(folder_to_save_plot + save_name)
    # plt.show()
    
    fig = plt.figure()
    x0 = np.arange(0, len(dataXYZ_error[:, 0]))
    x1 = np.array(dataXYZ_error[:, 0])
    x2 = np.zeros((len(dataXYZ_error[:, 0])))
    x_rms_plot = np.full(len(dataXYZ_error[:, 0]), x_rms)
    x_avg_plot = np.full(len(dataXYZ_error[:, 0]), x_avg)
    plt.plot(x0, dataXYZ_error[:, 0], label="Erro")
    plt.plot(x_rms_plot, label="RMSE", linestyle='--', color='k')
    plt.plot(x_avg_plot, label="Erro médio", linestyle='--', color='r')
    plt.xlabel("Pulsos Encoder")
    plt.ylabel("Erro [mm]")
    plt.title("Erro 3D - eixo X")
    plt.tight_layout()
    plt.fill_between(x0, x1, x2, where=(x1 < x2), alpha=0.30, color='red', interpolate=True)
    plt.fill_between(x0, x1, x2, where=(x1 >= x2), alpha=0.30, color='green', interpolate=True)
    plt.grid()
    plt.legend()
    save_name = f"_{comb_to_plot}_anc_x.png"
    fig.savefig(folder_to_save_plot + save_name)
    # plt.show()

    fig = plt.figure()
    y0 = np.arange(0, len(dataXYZ_error[:, 1]))
    y1 = np.array(dataXYZ_error[:, 1])
    y2 = np.zeros((len(dataXYZ_error[:, 1])))
    y_line_plot = np.full(len(dataXYZ_error[:, 1]), y_rms)
    y_avg_plot = np.full(len(dataXYZ_error[:, 1]), y_avg)
    plt.plot(y0, dataXYZ_error[:, 1], label="Erro")
    plt.plot(y_line_plot, label="RMSE", linestyle='--', color='k')
    plt.plot(y_avg_plot, label="Erro médio", linestyle='--', color='r')
    plt.xlabel("Pulsos Encoder")
    plt.ylabel("Erro [mm]")
    plt.title("Erro 3D - eixo Y")
    plt.tight_layout()
    plt.fill_between(y0, y1, y2, where=(y1 < y2), alpha=0.30, color='red', interpolate=True)
    plt.fill_between(y0, y1, y2, where=(y1 >= y2), alpha=0.30, color='green', interpolate=True)
    plt.grid()
    plt.legend()
    save_name = f"_{comb_to_plot}_anc_y.png"
    fig.savefig(folder_to_save_plot + save_name)
    # plt.show()

    fig = plt.figure()
    z0 = np.arange(0, len(dataXYZ_error[:, 2]))
    z1 = np.array(dataXYZ_error[:, 2])
    z2 = np.zeros((len(dataXYZ_error[:, 2])))
    z_line_plot = np.full(len(dataXYZ_error[:, 2]), z_rms)
    z_avg_plot = np.full(len(dataXYZ_error[:, 2]), z_avg)
    plt.plot(y0, dataXYZ_error[:, 2], label="Erro")
    plt.plot(z_line_plot, label="RMSE", linestyle='--', color='k')
    plt.plot(z_avg_plot, label="Erro médio", linestyle='--', color='r')
    plt.xlabel("Pulsos Encoder")
    plt.ylabel("Erro [mm]")
    plt.title("Erro 3D - eixo Z")
    plt.tight_layout()
    plt.fill_between(z0, z1, z2, where=(z1 < z2), alpha=0.30, color='red', interpolate=True)
    plt.fill_between(z0, z1, z2, where=(z1 >= z2), alpha=0.30, color='green', interpolate=True)
    plt.grid()
    plt.legend()
    save_name = f"_{comb_to_plot}_anc_z.png"
    fig.savefig(folder_to_save_plot + save_name)
    plt.show()
    




    # if KALMAN_USAGE:
    #     # kalman filter
    #     dt = 0.005
    #     std_acc = 0
    #     std_pos = 0.03

    #     # kf = KalmanFilter(dt, std_acc)
    #     kf = kalman.KalmanFilter(dt, std_acc, std_pos)
    #     X_points_kalman = []
    #     Y_points_kalman = []
    #     Z_points_kalman = []

    #     kf.Y = np.array([dataXYZ[0, 0], dataXYZ[0, 1], dataXYZ[0, 2], 0, 0, 0])

    #     # kalman filter run
    #     for pos in dataXYZ:
    #         (kf.X, kf.P) = kf.predict(kf.X, kf.P, kf.A, kf.Q, kf.B, kf.U)
    #         (kf.X, kf.P, kf.K) = kf.update(kf.X, kf.P, kf.Y, kf.H, kf.R)
    #         vel_x = (pos[0] - kf.X[0, 0]) / dt
    #         vel_y = (pos[1] - kf.X[0, 1]) / dt
    #         vel_z = (pos[2] - kf.X[0, 2]) / dt
    #         print(vel_x, vel_y, vel_z)

    #         kf.Y = np.array([pos[0], pos[1], pos[2], vel_x, vel_y, vel_z])
    #         pos_filtered = [int(kf.X[0, 0]), int(kf.X[0, 1]), int(kf.X[0, 2])]

    #         X_points_kalman.append(pos_filtered[0])
    #         Y_points_kalman.append(pos_filtered[1])
    #         Z_points_kalman.append(pos_filtered[2])
    #         # print(pos_x, pos_y, pos_z)
    #         # print(pos_filtered)
    #         # input()
