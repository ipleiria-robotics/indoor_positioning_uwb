# indoor_positioning_uwb

## Overview

On this folder the Python scripts and dataset are presented that we used to generate the position data and then analyse it later. The scripts are separated by folders depending on wich function. The main principle of this part of the repository is to collect the ranges measured from the Indoor Localization System using the Decawave's UWB kit's we installed and use a pos-processing analysis to study the error on the ranges and position. The ranges are obtained by the Tag device and the position is calcualted after. The method to compute the position using the ranges obtained was the Iterative Least-square.

### Python packages

For the Python scripts developed we used this packages:

- Pandas - https://pandas.pydata.org/

- Numpy - https://numpy.org/

- Matplotlib - https://matplotlib.org/

To run all script correctly it is necessary to install all the necessary packages. Each link leads to the weibsite where it is possible to install them.

***

```
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

---

## Obtaining data from tag

We implemented a script to capture data from tag using the serial port. This script is used mainly just to acquire the data and store it for future processing.

With this application, it is possible start the UART communication with the Tag device and send commands to interface with the Tag. At the same time, when it start, the anchors coordinates are loaded too from the respective csv file.

For the connection it is necessary to choose the Baudrate (115200) and Serial port COM detected and the operating system used. Another options are possible to determine.

To run this script go to folder where is located and run:

```
python sli_localization_app.py
```

***

## Analysis scripts

Inside the folder static_test and movement_test exists the different correspondent scripts to run on each test described prevously. To run the scripts some options must be configured. In each test, 2 main script must be used, one to generate the estimated positions file and the other to analyse the resultant data from the estimated positions. On the beggining on each file it is necessary to fullfill the options like filename to load, anchors_coordinates file, number of anchors to analyse,.. so on. 

#### GDOP analysis

A script to draw a GDOP map to help understand the installation of the anchors and evaluate it. This is important to evaluate the conditions of the indoor localization system will work and if there is a possiblity to adapt or change to a better anchor disposition. The user must define the heigh to run the script and draw the map.

To work with this script the next values must be filled:

```
Max_Y = 7     # max size on Y direction in meters
Max_X = 23    # max size on X direction in meters
Max_Z = 2.8   # Heigh to use on the gdop mapping
scale = 1     # define the scale to use 1 meters,...

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

```
python sli_localization_app.py
```

<img title="" src="https://github.com/ipleiria-robotics/indoor_positioning_uwb/blob/main/img/gdop.jpg" alt="">

#### Static tests:

An example to run the scripts to generate data and analyse for the first test (Teste 1) is now showed.

1. **python teste1_los_generate.py** - loads the dataset file with the ranges acquired and runs the script to calculate the positions and store on another file. The method used on this script to compute positions was teh Iterative Least-square.

2. **python teste1_los_ranges_analysis.py** - loads the result dataset with the distance obtained and generate an analysis on the error using the real position to determine the real distances. Generates histogram plots to represent the error.

3. **python teste1_los_plot_result.py** - loads the file with the results of estimated positions and determine the error comparin with the real position. It generates plots to help understanding the results.

For the next tests, the procedure is equal.

Note: this scripts must be executed on the folder were they are.

***

#### Movement tests:

In the case, for the dynamic tests, another dateset must be loaded - encoder acquisitions. To determine the error on thi case a linear regrassion was necessary to execute. This is because the equipment to acquire the tag data and the encoder data weren't syncronized. To solve that problem, an aproximation was necessary to elaborate.

An example to exe

1. **python slow_data_generate.py** - load the file containing the ranges obtained on the on the test and generates the file with the positions calculations.

2. **python slow_analysis.py** - runs the analysis of the position error during his deslocation. Plots are shown to demonstrate the results.

Note: this scripts must be executed on the folder were they are.

***
