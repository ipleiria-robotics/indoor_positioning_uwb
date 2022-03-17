import math as op
import platform
import matplotlib.pyplot as plt
import csv
import numpy as np
from sklearn import preprocessing


def calculate_GDOP():
    Max_Y = 7
    Max_X = 23
    Max_Z = 2.8
    scale = 1
    NORMALIZED = 0

    Max_Z_init = Max_Z

    fileName = "resultGDOP_"+str(Max_Z)

    operatingSystem = platform.system()

    if operatingSystem == 'Linux':
        text_file = open(fileName, "w")
    else:
        text_file = open(fileName, "w", newline="\n")

    # 8 ancoras
    acoord = np.array([
        [0, 0.412, 2.888],
        [7.185, 0.127, 2.875],
        [22.364, 6.688, 2.854],
        [14.118, 6.643, 2.889],
        [0.321, 6.663, 2.888],
        [14.022, 0.067, 2.888],
        [6.743, 6.700, 2.844],
        [22.156, 0, 2.876]
    ])

    Max_Y = int(Max_Y * scale)
    Max_X = int(Max_X * scale)
    Max_Z = int(Max_Z * scale)
    acoord = acoord * scale

    print("coords", acoord)
    print("max x, y and z area:", Max_X, Max_Y, Max_Z)

    for indexX in range(1, Max_X + 1):
        for indexY in range(1, Max_Y + 1):
            R = []
            A = []
            Q = []

            x = indexX
            y = indexY
            z = Max_Z

            for row in acoord:
                R = op.sqrt((row[0] - x)**2 + (row[1] - y)
                            ** 2 + (row[2] - z)**2)

                T = np.array([(np.array(row[0] - x) / R),
                              (np.array(row[1] - y) / R),
                              (np.array(row[2] - z) / R),
                              1])
                A.append(T)

            # Test = np.cov(A)
            Q = np.linalg.inv(np.matmul(np.transpose(A), A))
            # inv(A.' * A) * A.' * b
            # print(Q)
            PDOP = round(op.sqrt(Q[0, 0] + Q[1, 1] + Q[2, 2]), 2)
            VDOP = round(op.sqrt(Q[2, 2]), 2)
            HDOP = round(op.sqrt(Q[0, 0] + Q[1, 1]), 2)
            TDOP = round(op.sqrt(Q[3, 3]), 2)
            GDOP = round(op.sqrt(pow(PDOP, 2) + pow(TDOP, 2)), 2)

            # print(str(x) +";"+str(y)+";"+str(z)+";HDOP:"+ str(int(HDOP)) + ";PDOP:" + str(int(PDOP))+";GDOP"+str(int(GDOP))+"\r\n")
            text_file.writelines(str(x) + ";"+str(y)+";"+str(z) + ";" + str(
                HDOP) + ";" + str(VDOP) + ";" + str(PDOP) + ";" + str(GDOP) + "\r\n")
            # print(HDOP)
            # input()

    text_file.close()

    x = []
    y = []
    z = []
    _dataGDOP = []
    _dataHDOP = []
    _dataVDOP = []
    _dataPDOP = []

    with open(fileName, 'r') as f:
        reader = csv.reader(f, dialect='excel', delimiter='\t')
        for row in reader:
            string_row_splitted = str(row[0]).split(';')
            x.append(float(string_row_splitted[0]))
            y.append(float(string_row_splitted[1]))
            z.append(float(string_row_splitted[2]))

            _dataHDOP.append(float(string_row_splitted[3]))
            _dataVDOP.append(float(string_row_splitted[4]))
            _dataPDOP.append(float(string_row_splitted[5]))
            _dataGDOP.append(float(string_row_splitted[6]))

        _dataGDOP_matrix = []
        _dataHDOP_matrix = []
        _dataVDOP_matrix = []
        _dataPDOP_matrix = []

        line = []
        line2 = []
        line3 = []
        line4 = []
        counter = 0

        for inde_x in range(Max_X):
            for inde_y in range(Max_Y):
                line.append(_dataGDOP[counter])
                line2.append(_dataHDOP[counter])
                line3.append(_dataVDOP[counter])
                line4.append(_dataPDOP[counter])
                counter = counter+1
            _dataGDOP_matrix.append(line)
            _dataHDOP_matrix.append(line2)
            _dataVDOP_matrix.append(line3)
            _dataPDOP_matrix.append(line4)
            line = []
            line2 = []
            line3 = []
            line4 = []

    print("HDOP Mean: " + str(np.average(_dataHDOP_matrix)) + " STD: " + str(np.std(_dataHDOP_matrix)
                                                                             ) + " MAX: " + str(np.max(_dataHDOP_matrix)) + " MIN: " + str(np.min(_dataHDOP_matrix)))
    print("VDOP Mean: " + str(np.average(_dataVDOP_matrix)) + " STD: " + str(np.std(_dataVDOP_matrix)
                                                                             ) + " MAX: " + str(np.max(_dataVDOP_matrix)) + " MIN: " + str(np.min(_dataVDOP_matrix)))
    print("PDOP Mean: " + str(np.average(_dataPDOP_matrix)) + " STD: " + str(np.std(_dataPDOP_matrix)
                                                                             ) + " MAX: " + str(np.max(_dataPDOP_matrix)) + " MIN: " + str(np.min(_dataPDOP_matrix)))
    print("GDOP Mean: " + str(np.average(_dataGDOP_matrix)) + " STD: " + str(np.std(_dataGDOP_matrix)
                                                                             ) + " MAX: " + str(np.max(_dataGDOP_matrix)) + " MIN: " + str(np.min(_dataGDOP_matrix)))

    # marking the coordinates of the anchors map
    CoordsMap = np.zeros((Max_X, Max_Y))
    for coord in acoord:
        # print("pos: x:{} y:{}".format(int(coord[0]), int(coord[1])))
        if coord[0] == 0:
            coord[0] = 1
        if coord[1] == 0:
            coord[1] = 1
        CoordsMap[int(coord[0])][int(coord[1])] = coord[2]
    if NORMALIZED:
        _dataHDOP_matrix = preprocessing.normalize(_dataHDOP_matrix)
        _dataVDOP_matrix = preprocessing.normalize(_dataVDOP_matrix)
        _dataPDOP_matrix = preprocessing.normalize(_dataPDOP_matrix)
        _dataGDOP_matrix = preprocessing.normalize(_dataGDOP_matrix)

    fig, axes = plt.subplots(nrows=1, ncols=3)
    im = axes[2].imshow(_dataPDOP_matrix, cmap='magma')
    axes[2].set_title("PDOP")
    axes[2].set_ylabel("Coordenada X [m]")
    axes[2].set_xlabel("Coordenada Y [m]")
    clim = im.properties()['clim']

    axes[0].imshow(_dataHDOP_matrix, clim=clim, cmap='magma')
    axes[0].set_title("HDOP")
    axes[0].set_ylabel("Coordenada X [m]")
    axes[0].set_xlabel("Coordenada Y [m]")

    axes[1].imshow(_dataVDOP_matrix, clim=clim, cmap='magma')
    axes[1].set_title("VDOP")
    axes[1].set_ylabel("Coordenada X [m]")
    axes[1].set_xlabel("Coordenada Y [m]")
    fig.colorbar(im)
    fig_title = f"Mapeamento do DOP - z = {float(Max_Z_init/scale)}m"
    fig.suptitle(fig_title, fontsize=20)
    plt.show()


# main function
if __name__ == "__main__":
    calculate_GDOP()


# TODO LIST:
'''

'''
