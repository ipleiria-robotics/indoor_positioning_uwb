# # Indoor Localization System - UWB - Software folder

## Overview

This part of the repository contains the Python development scripts that provides the storage and analysis of the data from the UWB tag device. Tests are separated between different folders and auxiliary scrits are stored on the goodies and utilities folders. The file anchor_coordinates contains the coordinates from all the anchors installed on this indoor localization system.

```context
Firmware/
├── dataset/            // contains the datasets acquired
├── goodies/            // contains script for acquiring data from tag                     
├── examples/              
│   ├── static_test     // content related with the static test
│   │   ├── ...            
│   │   └── ... 
│   └── movement_test   // content related with the dynamic test
│       ├── ...            
│       └── ...                 
├── utilities/          // containing auxiliary scripts
├── anchor_coordinates  // conatining anchors coordinates
└── README.md
```

The distances are measured by the Tag and the position is estimated after. The method to compute the position using the ranges obtained was the Iterative Least-square.

---

## Python packages

For the Python scripts developed we used this packages:

- Pandas - [https://pandas.pydata.org/](https://pandas.pydata.org/)

- Numpy - [https://numpy.org/](https://numpy.org/)

- Matplotlib - [https://matplotlib.org/](https://matplotlib.org/)

To run all scripts correctly it is necessary to install all the necessary packages. Each link leads to the website where it is possible to install them.

---

## Anchors coordinates and installation

This point is crucial for the good functioning of this uwb localization system. For the installation, we recommend following some important rules:

- The tag should work “inside” the area delimited by the anchors. For example, if the anchors shape installed is a square/cube, the tag should be used inside that area/volume.
- The devices (especially the antenna) must be away from any metal object in a radius of 20cm approx. Additionally, it is recommended to use the antenna in a vertical direction.
- Study the implementation, taking account of the DOP (dilution of precision) impact. In this case, the anchors must have dispersed coordinates, so the geometry does not cause a big impact on the position estimates.

In our case we used a theodolite to measure all the coordinates. So to help us on the processing coordinates in the Cartesian axis, we developed a Python script ([sli_teodelito.py](https://github.com/ipleiria-robotics/indoor_positioning_uwb/tree/main/software/goodies)) to convert the results from the theodolite in to the x, y and z coordinates.

After that, we copy and paste the console results on [anchor_coordinates](https://github.com/ipleiria-robotics/indoor_positioning_uwb/blob/main/software/anchor_coordinates) file, with the anchors measure order on each line.

***

## GDOP analysis

A script to draw a DOP (HDOP, VDOP and PDOP) map to help understand the installation of the anchors and evaluate it. This is important to evaluate the conditions of the indoor localization system will work and if there is a possibility to adapt or change to a better anchor disposition. The user must define the height to run the script and draw the map.

To work with this script, the next values must be filled:

```context
Max_Y = 7     # max size on Y direction in meters
Max_X = 23    # max size on X direction in meters
Max_Z = 2.8   # Heigh to use on the gdop mapping
scale = 1     # define the scale to use 1 meters,...

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

To run this script just go to the folder and run:

```python
python sli_mapping_gdop.py
```

<img>

---

## Obtaining data from tag

We implemented a script to capture data from tag using the serial port. This script is used mainly just to acquire the data and store it for future processing.

It is possible to start the UART communication with the Tag device and send commands to interface with the Tag. At the same time, when it starts, the anchors coordinates are loaded too from the respective csv file.

For the connection it is necessary to choose the Baudrate (115200) and Serial port COM detected and the operating system used. Another options are possible to determine.

To run this script go to folder where is located and run:

```
python sli_localization_app.py
```

<img>

Using this script, it is possible to interact with the tag device via Serial port. It is necessary to define the port, depending on the operating system. To send commands or to rename the file to save data use the respective textbox. 

**Note**: this script is important to used in case the timestamp is necessary to be stored too. So when using this script, all the set of distances obtained to all anchors are time stamped.

---

## Analysis scripts

Inside the folder static_test and movement_test exists the different correspondent scripts to run on each test described previously. To run the scripts, some options must be configured. In each test, 2 main script must be used, one to generate the estimated positions file and the other to analyse the resultant data from the estimated positions. On the beggining on each file it is necessary to fill the options like filename to load, anchors_coordinates file, number of anchors to analyse,.. so on.

#### Static tests:

An example to run the scripts to generate data and analyse for the first test (Teste 1) is now showed.

1. **python teste1_los_generate.py** - loads the dataset file with the distances estimated and runs the script to calculate the positions, using the Iterative Least-square, and store the results on another dataset file.

2. **python teste1_los_ranges_analysis.py** - loads the result dataset with the distance obtained and generate an analysis on the error using the real position to determine the real distances. Generates histogram plots to represent the error.

3. **python teste1_los_plot_result.py** - loads the file with the results of estimated positions and determine the error comparing with the real position. It generates plots to help to understand the results.

For the next tests, the procedure is equal.

**Note**: this scripts must be executed on the folder were they are.

***

#### Dynamic tests:

In the case, for the dynamic tests, another dataset must be loaded—encoder acquisitions with the timestamps when they occur. The script sli_encoder.py ([utilities folder](https://github.com/ipleiria-robotics/indoor_positioning_uwb/tree/main/software/utilities)) was used. 


To determine the error in this case, a linear regression was necessary to execute. This is because the equipment to acquire the tag data and the encoder data were synchronized.

An example to execute the dynamic test for the slow velocity:

1. **python slow_data_generate.py** - load the file containing the distances obtained on the on the test and generates the file with the positions estimations.

2. **python slow_analysis.py** - runs the analysis of the position error during his deslocation, loading the dataset resultant from the previous script and, at the same time, loading the dataset conmtainined the encoder pulses with timestamps to be analysed. Plots are shown to demonstrate the results.

**Note**: this scripts must be executed on the folder were they are.

***

## Input file configuration

All the options for each python script are defined on the beginning and only the initial parameters need to be changed. For example, on the file *teste1_los_generate.py* we used the next options to run the script:

```
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

What is defined with these variables is the filenames for each file to load and to be store, the number of anchors to use, start and end line from the loaded dataset file and so on...

The rest of the other options are not necessary to change.

#### Generate your own data analysis

In case the user has its own dataset or want to run a different test using the same dataset we uploaded, the same procedure must be used. First, using the respective folder to load the dataset. Second, copy/create another Python script file and change the respective header on the beginning of the file. Then  it is possible to run the scripts.

**Note**: our advice about this topic is to be careful how the indexes of each field are defined. Changing them or using another format could let to a different value to send to the positioning calculation.
