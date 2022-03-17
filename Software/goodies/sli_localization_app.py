import random
import multiprocessing
import matplotlib.pyplot as plt
import statistics as stat
import tkinter
from tkinter import *
from tkinter import ttk
import serial
import threading
import os
import time
import datetime as date_time
import numpy as np
import csv
import math
import matplotlib

matplotlib.use('TkAgg')

pos_data = ['NaN', 'NaN', 'NaN']
data_x = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
data_y = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
data_z = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
old_mean_x = 0
old_mean_y = 0
old_mean_z = 0
old_var_x = 0
old_var_y = 0
old_var_z = 0
killThread = 0
line_print = 'NaN,NaN,NaN'
counter_kalman = 0
serial_data = ''
filter_data = ''
calc_data = ''
text_file = None
anchors_matrix = None
index_ranges = None
ranges_flag = 0
pos_calculation_flag = 0
error_pos_cal_flag = 0
save_file_flag = 0
update_period = 5
serial_object = None
# kalman_calc_flag = 0
# cl_pos_calc_flag = 0
# pwr_pos_calc_flag = 0

weight = None

# init the gui interface and give it a name to the window
gui = Tk()
gui.title("Decawave LabRob Interface")


# """This function to read from serial an call functions to treat that data
#     """
def get_data():
    # global plot2D_flag
    global serial_object
    global filter_data
    global text_file
    global save_file_flag
    global pos_calculation_flag
    global error_pos_calc_flag
    # global cl_compute_flag
    global pos_data

    while (serial_object.is_open):
        try:
            filter_data = serial_object.readline()
            data = filter_data.decode().split(',')
            print(filter_data.decode())
            function_calc_position(data)

        except TypeError:
            print("get-error method error")

    print("Thread killed")


# """The function initiates the Connection to the UART device with the Port and Buad fed through the Entry
#     boxes in the application.
#     The radio button selects the platform, as the serial object has different key phrases
#     for Linux and Windows. Some Exceptions have been made to prevent the app from crashing,
#     such as blank entry fields and value errors, this is due to the state-less-ness of the
#     UART device, the device sends data at regular intervals irrespective of the master's state.</p><p>    The other Parts are self explanatory.
#     """
def connect():
    version_ = system_op.get()
    print("OS version selected: ", format(version_))
    global serial_object
    port = port_entry.get()
    baud = baud_entry.get()
    try:
        if version_ == 2:
            try:
                serial_object = serial.Serial('/dev/tty' + str(port), baud)
            except:
                print("Cant open specific Port")

        elif version_ == 1:
            try:
                serial_object = serial.Serial('COM' + str(port), baud)
            except:
                print("Cant open specific Port")

    except ValueError:
        print("Enter Baud and Port")
        return

    t1 = threading.Thread(target=get_data)
    t1.daemon = True
    t1.start()


# """This function is for sending data from the computer to the host controller.
# The value entered in the the entry box is pushed to the UART. The data can be of any format, since
#    the data is always converted into ASCII, the receiving device has to convert the data into the required f
#    format.
#     """
def send():
    global text_file
    global save_file_flag
    global pos_calculation_flag
    global error_pos_calc_flag
    # global plot2D_flag
    global ranges_flag
    # global anchors_matrix
    # global index_ranges
    # global pos_test_original
    # global cl_compute_flag
    # global kalman_calc_flag
    global counter_kalman
    global old_mean_x
    global old_mean_y
    global old_mean_z
    # global kalman_filter
    # global cl_pos_calc_flag
    # global pwr_pos_calc_flag
    # global wls_pos_calc_flag
    # kalman_result = 'NaN,NaN,NaN'
    counter_kalman = 0
    old_mean_x = 0
    old_mean_y = 0
    old_mean_z = 0
    send_data = cmd_entry.get()

    try:
        text_file.close()
    except:
        pass

    load_anchors_coordinates()
    # print(weight)

    save_file_flag = saveFile.get()
    save_filename = save_filename_entry.get()
    # plot2D_flag = plot2D.get()
    pos_calculation_flag = positionCalc.get()
    error_pos_calc_flag = error_pos_calc.get()
    # cl_compute_flag = cl_ranges_calc.get()
    # kalman_calc_flag = kalman_calc.get()

    # cl_pos_calc_flag = cl_eval.get()
    # pwr_pos_calc_flag = pwr_eval.get()
    # wls_pos_calc_flag = wls_eval.get()

    if save_filename != '' and save_file_flag:
        if system_op.get() == 2:
            text_file = open(save_filename, "w")
        elif system_op.get() == 1:
            text_file = open(save_filename, "w", newline="\n")
        else:
            print("Select the OS you use")

    if not send_data:
        print("No data to send")
    else:
        if send_data == '0' or send_data == '1':
            ranges_flag = 1
        else:
            ranges_flag = 0
        serial_object.write(send_data.encode())
        serial_object.write(b'\r\n')


#  """
#     This function is for disconnecting and quitting the application.</p><p>    Sometimes the application throws a couple of errors while it is being shut down, the fix isn't out yet
#     but will be pushed to the repo once done.
#     simple GUI.quit() calls.
#     """
def disconnect():
    killThread = True
    try:
        serial_object.close()
        text_file.close()
    except AttributeError:
        print("Closing")
    gui.quit()


# """
# function to fill a matrix with anchors coordinates
# """
def load_anchors_coordinates():
    global anchors_matrix
    global index_ranges

    anchors_matrix = np.empty((0, 3), float)
    index_ranges = np.empty((0, 1), int)

    if anchor_check_1.get():
        index_ranges = np.append(index_ranges, np.array(
            [[int(anchor_entry_1_index_entry.get())]]), axis=0)
        anchors_matrix = np.append(anchors_matrix, np.array(
            [[(anchor_entry_x_1.get()), (anchor_entry_y_1.get()), (anchor_entry_z_1.get())]]), axis=0)

    if anchor_check_2.get():
        index_ranges = np.append(index_ranges, np.array(
            [[int(anchor_entry_2_index_entry.get())]]), axis=0)
        anchors_matrix = np.append(anchors_matrix, np.array(
            [[anchor_entry_x_2.get(), anchor_entry_y_2.get(), anchor_entry_z_2.get()]]), axis=0)

    if anchor_check_3.get():
        index_ranges = np.append(index_ranges, np.array(
            [[int(anchor_entry_3_index_entry.get())]]), axis=0)
        anchors_matrix = np.append(anchors_matrix, np.array(
            [[anchor_entry_x_3.get(), anchor_entry_y_3.get(), anchor_entry_z_3.get()]]), axis=0)

    if anchor_check_4.get():
        index_ranges = np.append(index_ranges, np.array(
            [[int(anchor_entry_4_index_entry.get())]]), axis=0)
        anchors_matrix = np.append(anchors_matrix, np.array(
            [[anchor_entry_x_4.get(), anchor_entry_y_4.get(), anchor_entry_z_4.get()]]), axis=0)

    if anchor_check_5.get():
        index_ranges = np.append(index_ranges, np.array(
            [[int(anchor_entry_5_index_entry.get())]]), axis=0)
        anchors_matrix = np.append(anchors_matrix, np.array(
            [[anchor_entry_x_5.get(), anchor_entry_y_5.get(), anchor_entry_z_5.get()]]), axis=0)

    if anchor_check_6.get():
        index_ranges = np.append(index_ranges, np.array(
            [[int(anchor_entry_6_index_entry.get())]]), axis=0)
        anchors_matrix = np.append(anchors_matrix, np.array(
            [[anchor_entry_x_6.get(), anchor_entry_y_6.get(), anchor_entry_z_6.get()]]), axis=0)

    if anchor_check_7.get():
        index_ranges = np.append(index_ranges, np.array(
            [[int(anchor_entry_7_index_entry.get())]]), axis=0)
        anchors_matrix = np.append(anchors_matrix, np.array(
            [[anchor_entry_x_7.get(), anchor_entry_y_7.get(), anchor_entry_z_7.get()]]), axis=0)

    if anchor_check_8.get():
        index_ranges = np.append(index_ranges, np.array(
            [[int(anchor_entry_8_index_entry.get())]]), axis=0)
        anchors_matrix = np.append(anchors_matrix, np.array(
            [[anchor_entry_x_8.get(), anchor_entry_y_8.get(), anchor_entry_z_8.get()]]), axis=0)


# """
# function to load variances from ranges on GUI - weight matrix
# """
def load_variances():
    global weight

    # weight = np.empty((0, 8), float)
    index_weight = []

    # m = [0, 0, 0, 0, 0, 0, 0, 0]
    # m[0] = (1 / int(variance_1.get()))
    # m[1] = (1 / int(variance_2.get()))
    # m[2] = (1 / int(variance_3.get()))
    # m[3] = (1 / int(variance_4.get()))
    # m[4] = (1 / int(variance_5.get()))
    # m[5] = (1 / int(variance_6.get()))
    # m[6] = (1 / int(variance_7.get()))
    # m[7] = (1 / int(variance_8.get()))

    # if anchor_check_1.get():
    #     index_weight.append(0)
    # if anchor_check_2.get():
    #     index_weight.append(1)
    # if anchor_check_3.get():
    #     index_weight.append(2)
    # if anchor_check_4.get():
    #     index_weight.append(3)
    # if anchor_check_5.get():
    #     index_weight.append(4)
    # if anchor_check_6.get():
    #     index_weight.append(5)
    # if anchor_check_7.get():
    #     index_weight.append(6)
    # if anchor_check_8.get():
    #     index_weight.append(7)

    # weight = np.identity(len(index_weight))
    # for i in range(len(index_weight)):
    #     # print("{}".format(index_weight[i]))
    #     weight[i][i] = m[index_weight[i]]

    # print(weight)


# """
# function to calculate position given the ranges
# """
def function_calc_position(data):
    global text_file
    global save_file_flag
    global anchors_matrix
    global index_ranges
    global calc_data
    global pos_data
    # global kalman_calc_flag
    # global cl_pos_calc_flag
    # global pwr_pos_calc_flag
    # global wls_pos_calc_flag
    global error_pos_calc_flag
    data_for_kalman = []
    A = []
    b = []
    number_ranges_ok = 0
    line = ""
    cl = []
    getDate = None

    if int(len(data)) >= 12:
    
        getDate = date_time.datetime.now().time()
        print(f"timestamp - {getDate}")
        
        number_ranges_ok = 0
        dist = np.zeros((len(index_ranges), 1))
        cl = np.zeros((len(index_ranges), 1))
        pwr_dif = np.zeros((len(index_ranges), 1))

        number_ranges_ok, dist, cl, pwr_dif = obtaining_anchors_and_ranging_data(
            index_ranges, data)

        if number_ranges_ok >= 3:
            if pos_calculation_flag:
                pos_data = calculate_least_square(dist, anchors_matrix)
                line += "LS_pos,{},{},{},".format(
                    int(pos_data[0]), int(pos_data[1]), int(pos_data[2]))
                data_for_kalman = pos_data
                if error_pos_calc_flag and not "NaN" in pos_data[0]:
                    function_calc_error(pos_data)

            # if cl_pos_calc_flag:
            #     pos_data = calculate_least_square_decawave_cl(dist, cl)
            #     line += "LS_cl_eval,{},{},{},".format(
            #         int(pos_data[0]), int(pos_data[1]), int(pos_data[2]))

            # if pwr_pos_calc_flag:
            #     pos_data = calculate_least_square_pwr_dif(dist, pwr_dif)
            #     line += "LS_pwr_eval,{},{},{},".format(
            #         int(pos_data[0]), int(pos_data[1]), int(pos_data[2]))

            # if wls_pos_calc_flag:
            #     pass
                # pos_data = calculate_weight_least_squared(dist, anchors_matrix, weight)
                # line += "WLS_eval,{},{},{},".format(int(pos_data[0]), int(pos_data[1]), int(pos_data[2]))

            # if kalman_calc_flag:
            #     pass
                # kF = kalman_filter_calc(data_for_kalman)
                # line += "KF,{},{},{}".format(kF[0], kF[1], kF[2])

            print(line)

        else:
            pass
            # if pos_calculation_flag:
            #     line += "LS_pos,NaN,NaN,NaN"

            # if cl_pos_calc_flag:
            #     line += "LS_cl_eval,NaN,NaN,NaN"

            # if pwr_pos_calc_flag:
            #     line += "LS_pwr_eval,NaN,NaN,NaN"

            # if kalman_calc_flag:
            #     line += "KF,NaN,NaN,NaN"

            # print(line)

        if save_file_flag:
            # data_string += str(getDate)
            data_string = ','.join(data)
            text_file.writelines(str(getDate) + "," + data_string.strip(
                '\r\n') + ',' + str(line) + '\r\n')

    else:
        pos_data[0] = 'NaN'
        pos_data[1] = 'NaN'
        pos_data[2] = 'NaN'


# """
# function that return the number os anchors, the anchors coords, ceoficient level and pwr_diff result (fsl - rsl)
# """
def obtaining_anchors_and_ranging_data(indexes, data):
    ranges_ok_count = 0
    ranges = np.zeros((len(index_ranges), 1))
    coeficient_level = np.zeros((len(index_ranges), 1))
    power_diference = np.zeros((len(index_ranges), 1))

    # weight_list = [325,206,252,620,465,186,421,223]
    # weight = np.zeros((len(index_ranges), (len(index_ranges)))

    for index in range(0, len(indexes)):
        # if data_splitted[int(index_ranges[index])] != "NaN":
        if not "NaN" in data[int(index_ranges[index])]:
            ranges[index] = (int(data[int(index_ranges[index])]))
            coeficient_level[index] = (float(data[int(index_ranges[index]) + 1]))
            power_diference[index] = abs(float(
                data[int(index_ranges[index]) - 2]) - float(data[int(index_ranges[index]) - 1]))
            # weight[index] = weight_list[int(index_ranges[index])]
            ranges_ok_count += 1

    return ranges_ok_count, ranges, coeficient_level, power_diference


# """
# function that computes the least square method using the ranges and the number of anchors defined
# """
def calculate_least_square(distances, anchor_coords):
    try:
        A = np.zeros((len(anchor_coords) - 1, 3))
        b = np.zeros((len(anchor_coords) - 1, 1))
        # print(distances)
        # print(anchors_matrix)
        for index in range(1, len(anchor_coords)):
            A[index - 1][0] = float(anchor_coords[0][0]) - \
                              float(anchor_coords[index][0])
            A[index - 1][1] = float(anchor_coords[0][1]) - \
                              float(anchor_coords[index][1])
            A[index - 1][2] = float(anchor_coords[0][2]) - \
                              float(anchor_coords[index][2])
            b[index - 1] = pow(float(anchor_coords[0][0]), 2) + pow(float(anchor_coords[0][1]), 2) + pow(
                float(anchor_coords[0][2]), 2) - pow(float(
                anchor_coords[index][0]), 2) - pow(float(anchor_coords[index][1]), 2) - pow(
                float(anchor_coords[index][2]), 2) + pow(int(distances[index]), 2) - pow(int(distances[0]), 2)

        b = np.true_divide(b, 2)
        r = np.linalg.solve(A.T.dot(A), A.T.dot(b))
        pos_data[0] = r[0]
        pos_data[1] = r[1]
        pos_data[2] = r[2]
        return pos_data

    except:
        pos_data[0] = 0
        pos_data[1] = 0
        pos_data[2] = 0
        return pos_data


# """
# function that computes the least square method chosing the anchors with CL == 1
# """
def calculate_least_square_decawave_cl(distances, cl):
    # print("ranges ok {}".format(number_anchors))
    # print("ranges sent {}".format(distances))
    # print("ranges cl {}".format(cl))
    count_ele = []
    ranges = []
    anchors_coords = []

    for i in range(len(distances)):
        if cl[i] != 0:
            ranges.append(distances[i])
            count_ele.append(i)
            anchors_coords.append(
                [anchors_matrix[i][0], anchors_matrix[i][1], anchors_matrix[i][2]])

    # print(ranges)
    # print(anchors_coords)
    if len(count_ele) >= 3:
        pos_data = calculate_least_square(ranges, anchors_coords)
    else:
        pos_data = [0, 0, 0]
    return pos_data


# """
# function that computes the least square method chosing the anchors with the fsl - rsl pwr criteria
# """
def calculate_least_square_pwr_dif(distances, power_difference):
    # print(distances)
    # print(power_difference)
    count_ele = []
    ranges = []
    anchors_coords = []

    for i in range(len(distances)):
        if power_difference[i] < 10:
            ranges.append(distances[i])
            count_ele.append(i)
            anchors_coords.append(
                [anchors_matrix[i][0], anchors_matrix[i][1], anchors_matrix[i][2]])

    # print(ranges)
    # print(anchors_coords)
    if len(count_ele) >= 3:
        pos_data = calculate_least_square(ranges, anchors_coords)
    else:
        pos_data = [0, 0, 0]
    return pos_data


# """
# function that computes the weight least squared method
# """
def calculate_weight_least_squared(distances, anchor_coords, weights):
    try:
        A = np.zeros((len(anchor_coords) - 1, 3))
        b = np.zeros((len(anchor_coords) - 1, 1))

        W = weights
        # print(W)

        # print(distances)
        # print(anchors_matrix)

        for index in range(1, len(anchor_coords)):
            A[index - 1][0] = float(anchor_coords[0][0]) - \
                              float(anchor_coords[index][0])
            A[index - 1][1] = float(anchor_coords[0][1]) - \
                              float(anchor_coords[index][1])
            A[index - 1][2] = float(anchor_coords[0][2]) - \
                              float(anchor_coords[index][2])
            b[index - 1] = pow(float(anchor_coords[0][0]), 2) + pow(float(anchor_coords[0][1]), 2) + pow(
                float(anchor_coords[0][2]), 2) - pow(float(
                anchor_coords[index][0]), 2) - pow(float(anchor_coords[index][1]), 2) - pow(
                float(anchor_coords[index][2]), 2) + pow(int(distances[index]), 2) - pow(int(distances[0]), 2)

        b = np.true_divide(b, 2)
        # r = np.linalg.solve(A.T.dot(A), A.T.dot(b))
        r = np.linalg.solve(A.T.dot(W).dot(A), A.T.dot(W).dot(b))
        pos_data[0] = r[0]
        pos_data[1] = r[1]
        pos_data[2] = r[2]
        return pos_data

    except:
        pos_data[0] = 0
        pos_data[1] = 0
        pos_data[2] = 0
        return pos_data


# """
# function that calculates the error between the real position and the position computed
# """
def function_calc_error(data):
    pos_x = int(x_pos_original.get())
    pos_y = int(y_pos_original.get())
    pos_z = int(z_pos_original.get())
    pox_x_error = pos_x - int(data[0])
    pox_y_error = pos_y - int(data[1])
    pox_z_error = pos_z - int(data[2])
    print("Error: x={}, y={}, z={}\r\n".format(
        pox_x_error, pox_y_error, pox_z_error))


# """
# function to calculate de GDOP
# """
def GDOP_calc():
    # global anchors_matrix
    print("Calculating the pdop coeficient")
    # obtain original position
    pos_x = float(x_pos_original.get())
    pos_y = float(y_pos_original.get())
    pos_z = float(z_pos_original.get())
    # obtain anchors coords
    load_anchors_coordinates()

    R = []
    A = []
    Q = []
    for row in anchors_matrix:
        R = (math.sqrt(pow(float(row[0]) - pos_x, 2) +
                       pow(float(row[1]) - pos_y, 2) + pow(float(row[2]) - pos_z, 2)))

        T = np.array([(np.array(float(row[0]) - pos_x) / R),
                      (np.array(float(row[1]) - pos_y) / R),
                      (np.array(float(row[2]) - pos_z) / R),
                      1])
        A.append(T)

    Q = np.linalg.inv(np.matmul(np.transpose(A), A))
    # inv(A.' * A) * A.' * b

    PDOP = math.sqrt(Q[0, 0] + Q[1, 1] + Q[2, 2])
    VDOP = math.sqrt(Q[2, 2])
    HDOP = math.sqrt(Q[0, 0] + Q[1, 1])
    TDOP = math.sqrt(Q[3, 3])
    GDOP = math.sqrt(pow(PDOP, 2) + pow(TDOP, 2))

    print("HDOP: {}".format(HDOP))
    print("VDOP: {}".format(VDOP))
    print("PDOP: {}".format(PDOP))
    print("TDOP: {}".format(TDOP))
    print("GDOP: {}".format(GDOP))


# """
# used for plotting the filename selected on textbox and using indexes to choose the 2d (x,y) positions
# """
def plotting_position():
    fig = plt.gcf()
    fig.show()
    fig.canvas.draw()

    x_i = int(x_index.get())
    y_i = int(y_index.get())
    loading_file = filename_plot.get()

    with open(loading_file, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        counter = 1
        for row in spamreader:
            # load file to plot position x and y with the indexes filled on the two text boxes
            print("{} - {} {}".format(counter, row[x_i], row[y_i]))

            if not row[x_i] == 'NaN':
                x = int(row[x_i])
                y = int(row[y_i])
                plt.plot(x, y, 'r+')  # plot something

                # update canvas immediately
                # plt.xlim([-2000, 22000])
                # plt.ylim([-3100, 3100])
                # plt.pause(0.001)  # I ain't needed!!!

                fig.canvas.draw()
            plt.grid()

            counter += 1
    print("Done Loading")


# """
# used for compute the real ranges using the position defined on the textbox
# """
def calculate_real_ranges():
    print("calculate_real_ranges")
    global anchors_matrix
    # obtain original position
    pos_x = int(x_pos_original.get())
    pos_y = int(y_pos_original.get())
    pos_z = int(z_pos_original.get())
    # obtain anchors coords

    anchors_matrix = np.empty((0, 3), float)

    if anchor_check_1.get():
        anchors_matrix = np.append(anchors_matrix, np.array(
            [[(anchor_entry_x_1.get()), (anchor_entry_y_1.get()), (anchor_entry_z_1.get())]]), axis=0)

    if anchor_check_2.get():
        anchors_matrix = np.append(anchors_matrix, np.array(
            [[anchor_entry_x_2.get(), anchor_entry_y_2.get(), anchor_entry_z_2.get()]]), axis=0)

    if anchor_check_3.get():
        anchors_matrix = np.append(anchors_matrix, np.array(
            [[anchor_entry_x_3.get(), anchor_entry_y_3.get(), anchor_entry_z_3.get()]]), axis=0)

    if anchor_check_4.get():
        anchors_matrix = np.append(anchors_matrix, np.array(
            [[anchor_entry_x_4.get(), anchor_entry_y_4.get(), anchor_entry_z_4.get()]]), axis=0)

    if anchor_check_5.get():
        anchors_matrix = np.append(anchors_matrix, np.array(
            [[anchor_entry_x_5.get(), anchor_entry_y_5.get(), anchor_entry_z_5.get()]]), axis=0)

    if anchor_check_6.get():
        anchors_matrix = np.append(anchors_matrix, np.array(
            [[anchor_entry_x_6.get(), anchor_entry_y_6.get(), anchor_entry_z_6.get()]]), axis=0)

    if anchor_check_7.get():
        anchors_matrix = np.append(anchors_matrix, np.array(
            [[anchor_entry_x_7.get(), anchor_entry_y_7.get(), anchor_entry_z_7.get()]]), axis=0)

    if anchor_check_8.get():
        anchors_matrix = np.append(anchors_matrix, np.array(
            [[anchor_entry_x_8.get(), anchor_entry_y_8.get(), anchor_entry_z_8.get()]]), axis=0)

    print("Printing Real Ranges: ")
    for row in anchors_matrix:
        # d = √((x2-x1)2 + (y2-y1)2 + (z2-z1)2)
        range_compute = math.sqrt(math.pow((int(row[0]) - pos_x), 2) + math.pow(
            (int(row[1]) - pos_y), 2) + math.pow((int(row[2]) - pos_z), 2))
        print("Range {}".format(int(range_compute)))


# """
# The main loop consists of all the GUI objects and its placement.
# """
if __name__ == "__main__":
    global saveFileName

    killThread = FALSE
    # frames
    Frame(height=600, width=600, bd=3, relief='groove').place(x=5, y=5)
    # frame_2 =
    # Frame(height=110, width=600, bd=3, relief='groove').place(x=5, y=600)
    # text = Text(width=71, height=15)

    # threads
    # t2 = threading.Thread(target=update_gui)
    # t2.daemon = True
    # t2.start()

    # labels
    Label(text="Anchor Selection").place(x=10, y=190)
    Label(text="Coords X, Y, Z").place(x=160, y=190)
    Label(text="Options").place(x=450, y=190)
    Label(text="Range index").place(x=305, y=190)
    # Label(text="Variance").place(x=380, y=190)
    Label(text="Baudrate").place(x=150, y=50)
    Label(text="Port").place(x=250, y=50)

    # checkbox
    anchor_check_1 = IntVar()
    Checkbutton(gui, text="Anchor 1",
                variable=anchor_check_1).place(x=10, y=210)
    anchor_check_2 = IntVar()
    Checkbutton(gui, text="Anchor 2",
                variable=anchor_check_2).place(x=10, y=240)
    anchor_check_3 = IntVar()
    Checkbutton(gui, text="Anchor 3",
                variable=anchor_check_3).place(x=10, y=270)
    anchor_check_4 = IntVar()
    Checkbutton(gui, text="Anchor 4",
                variable=anchor_check_4).place(x=10, y=300)
    anchor_check_5 = IntVar()
    Checkbutton(gui, text="Anchor 5",
                variable=anchor_check_5).place(x=10, y=330)
    anchor_check_6 = IntVar()
    Checkbutton(gui, text="Anchor 6",
                variable=anchor_check_6).place(x=10, y=360)
    anchor_check_7 = IntVar()
    Checkbutton(gui, text="Anchor 7",
                variable=anchor_check_7).place(x=10, y=390)
    anchor_check_8 = IntVar()
    Checkbutton(gui, text="Anchor 8",
                variable=anchor_check_8).place(x=10, y=420)

    positionCalc = IntVar()
    Checkbutton(gui, text="LS pos",
                variable=positionCalc).place(x=450, y=210)
    # plot2D = IntVar()
    # Checkbutton(gui, text="Plot 2D", variable=plot2D).place(x=450, y=240)
    saveFile = IntVar()
    Checkbutton(gui, text="Save CSV File",
                variable=saveFile).place(x=450, y=270)
    error_pos_calc = IntVar()
    Checkbutton(gui, text="Pos. Error",
                variable=error_pos_calc).place(x=450, y=240)
    # cl_ranges_calc = IntVar()
    # Checkbutton(gui, text="Deca CL range eval", variable=cl_ranges_calc).place(x=450, y=360)
    # kalman_calc = IntVar()
    # Checkbutton(gui, text="Kalman Filter",
    #             variable=kalman_calc).place(x=450, y=330)

    # cl_eval = IntVar()
    # Checkbutton(gui, text="CL LS pos",
    #             variable=cl_eval).place(x=450, y=360)

    # pwr_eval = IntVar()
    # Checkbutton(gui, text="Power LS pos",
    #             variable=pwr_eval).place(x=450, y=390)

    # wls_eval = IntVar()
    # Checkbutton(gui, text="WLS pos",
    #             variable=wls_eval).place(x=450, y=420)

    # text box
    anchor_entry_x_1 = Entry(width=10)
    anchor_entry_x_1.place(x=90, y=210)
    anchor_entry_y_1 = Entry(width=10)
    anchor_entry_y_1.place(x=160, y=210)
    anchor_entry_z_1 = Entry(width=10)
    anchor_entry_z_1.place(x=230, y=210)
    anchor_entry_1_index_entry = Entry(width=5)
    anchor_entry_1_index_entry.place(x=320, y=210)
    anchor_entry_1_index_entry.insert(END, 3)
    # variance_1 = Entry(width=5)
    # variance_1.place(x=385, y=210)
    # variance_1.insert(END, 325)

    anchor_entry_x_2 = Entry(width=10)
    anchor_entry_x_2.place(x=90, y=240)
    anchor_entry_y_2 = Entry(width=10)
    anchor_entry_y_2.place(x=160, y=240)
    anchor_entry_z_2 = Entry(width=10)
    anchor_entry_z_2.place(x=230, y=240)
    anchor_entry_2_index_entry = Entry(width=5)
    anchor_entry_2_index_entry.place(x=320, y=240)
    anchor_entry_2_index_entry.insert(END, 7)
    # variance_2 = Entry(width=5)
    # variance_2.place(x=385, y=240)
    # variance_2.insert(END, 206)

    anchor_entry_x_3 = Entry(width=10)
    anchor_entry_x_3.place(x=90, y=270)
    anchor_entry_y_3 = Entry(width=10)
    anchor_entry_y_3.place(x=160, y=270)
    anchor_entry_z_3 = Entry(width=10)
    anchor_entry_z_3.place(x=230, y=270)
    anchor_entry_3_index_entry = Entry(width=5)
    anchor_entry_3_index_entry.place(x=320, y=270)
    anchor_entry_3_index_entry.insert(END, 11)
    # variance_3 = Entry(width=5)
    # variance_3.place(x=385, y=270)
    # variance_3.insert(END, 252)

    anchor_entry_x_4 = Entry(width=10)
    anchor_entry_x_4.place(x=90, y=300)
    anchor_entry_y_4 = Entry(width=10)
    anchor_entry_y_4.place(x=160, y=300)
    anchor_entry_z_4 = Entry(width=10)
    anchor_entry_z_4.place(x=230, y=300)
    anchor_entry_4_index_entry = Entry(width=5)
    anchor_entry_4_index_entry.place(x=320, y=300)
    anchor_entry_4_index_entry.insert(END, 15)
    # variance_4 = Entry(width=5)
    # variance_4.place(x=385, y=300)
    # variance_4.insert(END, 620)

    anchor_entry_x_5 = Entry(width=10)
    anchor_entry_x_5.place(x=90, y=330)
    anchor_entry_y_5 = Entry(width=10)
    anchor_entry_y_5.place(x=160, y=330)
    anchor_entry_z_5 = Entry(width=10)
    anchor_entry_z_5.place(x=230, y=330)
    anchor_entry_5_index_entry = Entry(width=5)
    anchor_entry_5_index_entry.place(x=320, y=330)
    anchor_entry_5_index_entry.insert(END, 19)
    # variance_5 = Entry(width=5)
    # variance_5.place(x=385, y=330)
    # variance_5.insert(END, 465)

    anchor_entry_x_6 = Entry(width=10)
    anchor_entry_x_6.place(x=90, y=360)
    anchor_entry_y_6 = Entry(width=10)
    anchor_entry_y_6.place(x=160, y=360)
    anchor_entry_z_6 = Entry(width=10)
    anchor_entry_z_6.place(x=230, y=360)
    anchor_entry_6_index_entry = Entry(width=5)
    anchor_entry_6_index_entry.place(x=320, y=360)
    anchor_entry_6_index_entry.insert(END, 23)
    # variance_6 = Entry(width=5)
    # variance_6.place(x=385, y=360)
    # variance_6.insert(END, 186)

    anchor_entry_x_7 = Entry(width=10)
    anchor_entry_x_7.place(x=90, y=390)
    anchor_entry_y_7 = Entry(width=10)
    anchor_entry_y_7.place(x=160, y=390)
    anchor_entry_z_7 = Entry(width=10)
    anchor_entry_z_7.place(x=230, y=390)
    anchor_entry_7_index_entry = Entry(width=5)
    anchor_entry_7_index_entry.place(x=320, y=390)
    anchor_entry_7_index_entry.insert(END, 27)
    # variance_7 = Entry(width=5)
    # variance_7.place(x=385, y=390)
    # variance_7.insert(END, 421)

    anchor_entry_x_8 = Entry(width=10)
    anchor_entry_x_8.place(x=90, y=420)
    anchor_entry_y_8 = Entry(width=10)
    anchor_entry_y_8.place(x=160, y=420)
    anchor_entry_z_8 = Entry(width=10)
    anchor_entry_z_8.place(x=230, y=420)
    anchor_entry_8_index_entry = Entry(width=5)
    anchor_entry_8_index_entry.place(x=320, y=420)
    anchor_entry_8_index_entry.insert(END, 31)
    # variance_8 = Entry(width=5)
    # variance_8.place(x=385, y=420)
    # variance_8.insert(END, 223)

    # fil anchor with coord file stored
    with open('..\\anchor_coordinates', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        count = 0
        for row in spamreader:
            # print(row)
            if count == 0:
                anchor_entry_x_1.insert(END, str(row[0]))
                anchor_entry_y_1.insert(END, str(row[1]))
                anchor_entry_z_1.insert(END, str(row[2]))
            if count == 1:
                anchor_entry_x_2.insert(END, str(row[0]))
                anchor_entry_y_2.insert(END, str(row[1]))
                anchor_entry_z_2.insert(END, str(row[2]))
            if count == 2:
                anchor_entry_x_3.insert(END, str(row[0]))
                anchor_entry_y_3.insert(END, str(row[1]))
                anchor_entry_z_3.insert(END, str(row[2]))
            if count == 3:
                anchor_entry_x_4.insert(END, str(row[0]))
                anchor_entry_y_4.insert(END, str(row[1]))
                anchor_entry_z_4.insert(END, str(row[2]))
            if count == 4:
                anchor_entry_x_5.insert(END, str(row[0]))
                anchor_entry_y_5.insert(END, str(row[1]))
                anchor_entry_z_5.insert(END, str(row[2]))
            if count == 5:
                anchor_entry_x_6.insert(END, str(row[0]))
                anchor_entry_y_6.insert(END, str(row[1]))
                anchor_entry_z_6.insert(END, str(row[2]))
            if count == 6:
                anchor_entry_x_7.insert(END, str(row[0]))
                anchor_entry_y_7.insert(END, str(row[1]))
                anchor_entry_z_7.insert(END, str(row[2]))
            if count == 7:
                anchor_entry_x_8.insert(END, str(row[0]))
                anchor_entry_y_8.insert(END, str(row[1]))
                anchor_entry_z_8.insert(END, str(row[2]))
            count += 1

    save_filename_entry = Entry(width=15)
    save_filename_entry.place(x=450, y=300)

    cmd_entry = Entry(width=15)
    cmd_entry.place(x=100, y=160)

    baud_entry = Entry(width=7)
    baud_entry.insert(END, '115200')
    baud_entry.place(x=150, y=80)

    port_entry = Entry(width=7)
    port_entry.insert(END, '3')
    port_entry.place(x=250, y=80)

    # x label
    Label(text="Position to test [x,y,z]").place(x=10, y=460)
    Label(text="X:").place(x=10, y=480)
    x_pos_original = Entry(width=7)
    x_pos_original.place(x=25, y=480)
    # y label
    Label(text="Y:").place(x=10, y=505)
    y_pos_original = Entry(width=7)
    y_pos_original.place(x=25, y=505)
    # z label
    Label(text="Z:").place(x=10, y=530)
    z_pos_original = Entry(width=7)
    z_pos_original.place(x=25, y=530)
    # buttonGDOP =
    Button(text="GDOP Evaluation", command=GDOP_calc,
           width=15).place(x=10, y=555)

    Label(text="Filename: ").place(x=150, y=515)
    filename_plot = Entry(width=20)
    filename_plot.place(x=220, y=515)
    Label(text="X _index: ").place(x=150, y=540)
    x_index = Entry(width=7)
    x_index.place(x=220, y=540)
    Label(text="Y _index: ").place(x=150, y=560)
    y_index = Entry(width=7)
    y_index.place(x=220, y=560)

    Button(text="Plot 2D position", command=plotting_position,
           width=15).place(x=150, y=480)

    Button(text="Calculate Real Ranges", command=calculate_real_ranges,
           width=15).place(x=300, y=480)

    # radio button
    system_op = IntVar()
    # radio_1 =
    Radiobutton(text="Windows", variable=system_op, value=1).place(x=10, y=10)
    # radio_2 =
    Radiobutton(text="Linux", variable=system_op, value=2).place(x=110, y=10)

    # button
    # button1 =
    Button(text="Send", command=send, width=6).place(x=15, y=156)

    # connect =
    Button(text="Connect", command=connect, width=10).place(x=15, y=50)
    # disconnect =
    Button(text="Disconnect", command=disconnect, width=10).place(x=15, y=80)

    # mainloop
    gui.geometry('615x615')
    gui.mainloop()

# Old code '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# """
# fucntion to compute the confidence level of the ranges~
# """
# def function_cl_compute(data):
#     try:
#         line = 'CL - '
#         if ((int(len(data))-1) / 12) > 4:
#             for i in range(0, int((int(len(data))-1) / 12)):
#                 mc = 0
#                 cl = 0
#                 luep = 0
#                 prNLOS = 0
#                 max_amp = [0, 0, 0]
#                 if i == 0:
#                     if data[4].isnumeric():
#                         max_amp[0] = int(data[5])
#                         max_amp[1] = int(data[6])
#                         max_amp[2] = int(data[7])
#                         mc = max(max_amp) / int(data[13])
#                         iDIFF = math.fabs(int(data[4]) - int(data[12]))
#                         if iDIFF <= 3.3:
#                             prNLOS = 0
#                         elif iDIFF < 6.0 and iDIFF > 3.3:
#                             prNLOS = 0.39178 * iDIFF - 1.31719
#                         else:
#                             prNLOS = 1

#                         if prNLOS == 0:
#                             cl = 1
#                         else:
#                             if mc >= 0.9:
#                                 cl = 1
#                             else:
#                                 cl = 1 - prNLOS

#                         line += str(cl)
#                     else:
#                         line += 'NaN'

#                 else:
#                     index_selector = 4 + (i * 13)
#                     if data[index_selector].isnumeric():
#                         max_amp[0] = int(data[index_selector+1])
#                         max_amp[1] = int(data[index_selector+2])
#                         max_amp[2] = int(data[index_selector+3])
#                         mc = max(max_amp) / int(data[13])
#                         iDIFF = math.fabs(
#                             int(data[index_selector]) - int(data[index_selector+8]))
#                         if iDIFF <= 3.3:
#                             prNLOS = 0
#                         elif iDIFF < 6.0 and iDIFF > 3.3:
#                             prNLOS = 0.39178 * iDIFF - 1.31719
#                         else:
#                             prNLOS = 1

#                         if prNLOS == 0:
#                             cl = 1
#                         else:
#                             if mc >= 0.9:
#                                 cl = 1
#                             else:
#                                 cl = 1 - prNLOS

#                         line += ',' + str(cl)
#                         #print(data[3 + (i * 13)])
#                     else:
#                         line += ',NaN'
#             print(line)
#         else:
#             print("Option to read antenna info on tag activated")
#     except TypeError:
#         pass


# """" This function is an update function which is also threaded. The function assimilates the data
#     and applies it to it corresponding progress bar. The text box is also updated every couple of seconds.</p><p>    A simple auto refresh function .after() could have been used, this has been avoid purposely due to
#     various performance issues.
# """
# def update_gui():
#     global filter_data
#     global calc_data
#     global update_period
#     global text_file
#     global killThread

#     text.place(x=15, y=10)
#     new = time.time()

#     while(not killThread):
#         if filter_data:
#             text.insert(END, filter_data)
#             text.insert(END, "\n")
#             text.see(END)
#             filter_data = ""
#         if calc_data:
#             text.insert(END, calc_data)
#             text.insert(END, "\n")
#             text.see(END)
#             calc_data = ''

#     print("Thread killed")


# """
# function to deal the data slitted from the serial data
# """
# def receving_data_from_serial(serial_string):
#     fps_received = []
#     rsl_received = []
#     ranges_received = []
#     cl_received = []

#     data = serial_string.decode().split(',')
#     fps

#     return
