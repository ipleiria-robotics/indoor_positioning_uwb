# # Indoor Localization System - UWB - Software folder

## Overview

This part of the repository contains the Python development scripts that provides the storage and analysis of the data from the UWB tag device. Tests are separated between different folders and auxiliary scripts are stored on the goodies and utilities folders. The file [anchor_coordinates](https://github.com/ipleiria-robotics/indoor_positioning_uwb/blob/main/software/anchor_coordinates) contains the coordinates from all the anchors installed on the implemented indoor localization system.

```context
Firmware/
├── dataset/            // contains the acquired datasets
├── goodies/            // contains the script for acquiring data from tag                     
├── examples/              
│   ├── static_test     // content related with the static test
│   │   ├── ...            
│   │   └── ... 
│   └── movement_test   // content related with the dynamic test
│       ├── ...            
│       └── ...                 
├── utilities/          // contains auxiliary scripts
├── anchor_coordinates  // conatins anchors coordinates
└── README.md
```

The distances are measured by the Tag and then the position is estimated from those ranges. To compute the position of the tag using the ranges, we used the Iterative Least-Square.

---

## Python packages

For the developed Python scripts, we used these packages:

- Pandas - [https://pandas.pydata.org/](https://pandas.pydata.org/)

- Numpy - [https://numpy.org/](https://numpy.org/)

- Matplotlib - [https://matplotlib.org/](https://matplotlib.org/)

To run all scripts correctly, one has to install all the required packages. Each link points to the corresponding website, where you can find instructions on how to install each of the required packages.

---

## Anchors coordinates and installation

This point is crucial for the proper functioning of this uwb-based localization system. To obtain improved results, follow these recommendations:

- The tag should work “inside” the area delimited by the anchors. For instance, if the installed anchors for a squared/cubed shape, than the tag should be used inside that area/volume.
- The devices, namely the antenna, must be away from any metal object in a radius of ~20cm. Additionally, it is recommended to use the antenna in a vertical direction.
- Study the implementation, taking account the DOP (dilution of precision) impact. In this case, the anchors must have dispersed coordinates, so the geometry does not cause a big impact on the position estimates.

In our case we used a theodolite to measure all the coordinates. So, to help us on the processing coordinates in the Cartesian axis, we developed a Python script ([sli_teodelito.py](https://github.com/ipleiria-robotics/indoor_positioning_uwb/tree/main/software/goodies)) to convert the results from the theodolite reference frame to the x, y and z coordinates on the world reference frame.

After that, we copy and paste the console results on the [anchor_coordinates](https://github.com/ipleiria-robotics/indoor_positioning_uwb/blob/main/software/anchor_coordinates) file, with the anchors measures ordered by the anchor number in each line.

***

## GDOP analysis

We developed a script to visualize the DOP (HDOP, VDOP and PDOP) map, to help understand and guuide the installation of the anchors and evaluate their distribution. This is important to evaluate the conditions in which the indoor localization system will work, and if there is the possibility to adapt or change to a better anchor distribution. The user must pre-define the height at which he wants the script to run and draw the map.

To work with this script, the next values must be introduced beforehand:

```python
Max_Y = 7     # max size on Y direction (in meters)
Max_X = 23    # max size on X direction (in meters)
Max_Z = 2.8   # Heigh to use on the gdop mapping (in meters)
scale = 1     # define the scale to use (1 meters, ...)

# array with the x,y and z coordinates
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
```

To run this script, just go to the corresponding folder and run:

```python
python sli_mapping_gdop.py
```

<img title="" src="https://github.com/ipleiria-robotics/indoor_positioning_uwb/blob/main/img/gdop.jpg" width="800" height="600" alt="">

---

## Obtaining data from tag

We implemented a script to capture data from the tag using the serial port. This script is used mainly to acquire the data and store it for future processing.

It is possible to start the UART communication with the Tag device and send commands to the serial interface with the Tag. At the same time, when it starts, the anchors coordinates are loaded from the corresponding csv file.

For the successful connection, one needs to choose the Baudrate (115200), the serial port where the device got attached, and the operating system being used.  

To run this script, go to folder where is located and execute:

```python
python sli_localization_app.py
```

<img title="" src="https://github.com/ipleiria-robotics/indoor_positioning_uwb/blob/main/img/app_decawave.jpg" alt="">

Using this script, it is possible to interact with the tag device via serial port. You need to define the port to use, which depends on the operating system. To send commands, or to rename the file where to save data, use the respective textbox and the Button "Send" to execute. To save the datra acquired on a file, put a check on the respective checkbox and name the file on the textbox.

Other options can be used, like inserting the real position and obtain the GDOP values.

**Note**: this script stores the timestamps for each acquistion, so has to allow analysing the acquired data over time.

---

## Analysis scripts

Inside the folder [static_test](https://github.com/ipleiria-robotics/indoor_positioning_uwb/tree/main/software/static_test) and [movement_test](https://github.com/ipleiria-robotics/indoor_positioning_uwb/tree/main/software/movement_test) you find the different scripts to run each test, has described previously. To run the scripts, some options must be configured first. In each test, two main script must be used: one to generate the estimated positions file; and the other to analyse the resulting data from the estimated positions. On the beggining of each file, fill the needed options, such as the filename to load, the anchors_coordinates file path/name, the number of anchors to analyse, etc..

#### Static tests:

Here you find an example on how to run the scripts to generate data and perform analysis for the first test (Teste 1):

1. **python [teste1_los_generate.py](https://github.com/ipleiria-robotics/indoor_positioning_uwb/blob/main/software/static_test/teste1_los_generate.py)** - loads the dataset file with the estimated distances, and runs the script to calculate the positions, using the Iterative Least-Square, storing the results on another dataset file.

2. **python [teste1_los_ranges_analysis.py](https://github.com/ipleiria-robotics/indoor_positioning_uwb/blob/main/software/static_test/teste1_los_ranges_analysis.py)** - loads the result dataset with the obtained distance, and performs an analysis on the error using the real position to determine the real distances and compute the estimation errors. It also generates an histogram plots to represent the error.

3. **python [teste1_los_plot_result.py](https://github.com/ipleiria-robotics/indoor_positioning_uwb/blob/main/software/static_test/teste2_nlos_plot_result.py)** - loads the file with the results of the estimated positions and determines the error by comparing with the real position. It generates plots to visualize and better help understanding the results.

For the next tests, the procedure is identical.

**Note**: this scripts must be executed on the folder in which they are stored.

***

#### Dynamic tests:

In the dynamics tests' case, another dataset must be loaded, namely, the encoder acquisitions with the corresponding timestamps. The script [sli_encoder.py](https://github.com/ipleiria-robotics/indoor_positioning_uwb/blob/main/software/utilities/sli_encoder.py) was used for this. 

To determine the error in this case, a linear regression was made to estinate the enccoder-based tag position for the same timestamp as the UWB-based estimation, since the acquired data was to triggered at the sime time instants. To do so, we had to guarantee that the equipment used to acquire the tag data and the encoder data were synchronized.

The following describes an example to execute the dynamic test for the slow velocity:

1. **python [slow_data_generate.py](https://github.com/ipleiria-robotics/indoor_positioning_uwb/blob/main/software/movement_test/slow_data_generate.py)** - load the file containing the distances obtained on the test, and generates the file with the positions estimations.

2. **python [slow_analysis.py](https://github.com/ipleiria-robotics/indoor_positioning_uwb/blob/main/software/movement_test/slow_analysis.py)** - runs the analysis of the position error evolution during the tag motion, loading the dataset resulting from the previous script and, at the same time, loading the dataset containing the encoder pulses with timestamps to be analysed. Plots are shown to visualize the results.

**Note**: these scripts must be executed on the folder were they are stored.

***

## Input file configuration

All the options for each python script are defined at the beginning of each script, and only the initial parameters need to be changed. For instance, on the file [teste1_los_generate.py](https://github.com/ipleiria-robotics/indoor_positioning_uwb/blob/main/software/static_test/teste1_los_generate.py) we used the following options to run the script:

```python
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
```

The the other options, not shown here, do not need to be change.

#### Generate your own data analysis

In case the user has its own datase, or wants to run a different test using the same dataset we uploaded, the same procedure must be used. First, use the corresponding folder to load the dataset. Second, copy/create another Python script file and change the corresponding header on the beginning of the file. Then, proceed with the scrips execution.

**Note**: our advice about this topic is to be careful about the collum indexes where the data on each line on the loaded file. Changing them, or using another format, could lead to a different value to send to the positioning calculation.
