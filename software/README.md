# indoor_positioning_uwb

## Overview

On this folder the Python scripts and dataset are presented that we used to generate the position data and then analyse it later. The scripts are separated by folders depending on wich function.

### Python packages

For the Python scripts developed we used this packages:

- Pandas - https://pandas.pydata.org/

- Numpy - https://numpy.org/

- Matplotlib - https://matplotlib.org/

To run all script correctly it is necessary to install them.

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

## Scripts usage

Inside the folder static_test and movement_test exists the different correspondent scripts to run on each test described prevously. To run the scripts some options must be configured. In each test, 2 main script must be used, one to generate the estimated positions file and the other to analyse the resultant data from the estimated positions. On the beggining on each file it is necessary to fullfill the options like filename to load, anchors_coordinates file, number of anchors to analyse,.. so on. 

#### Static tests:

An example to run the scripts to generate data and analyse for the first test (Teste 1) is now showed.

1. **python teste1_los_generate.py** - loads the dataset file with the ranges acquired and runs the script to calculate the positions and store on another file.

2. **python teste1_los_ranges_analysis.py** - loads the result dataset with the distance obtained and generate an analysis on the error using the real position to determine the real distances. Generates histogram plots to represent the error.

3. **python teste1_los_plot_result.py** - loads the file with the results of estimated positions and determine the error comparin with the real position. It generates plots to help understanding the results.

For the next tests, the procedure is equal.

Note: this scripts must be executed on the folder were they are.

***

#### Movement tests:

In the case, for the dynamic tests, another dateset must be loaded - encoder acquisitions. To determine the error on thi case a linear regrassion was necessary to execute. This is because the equipment to acquire the tag data and the encoder data weren't syncronized. To solve that problem, an aproximation was necessary to elaborate.

An example to execute the dynamic analysis of the slow test:

1. **python slow_data_generate.py** - load the file containing the ranges obtained on the on the test and generates the file with the positions calculations.

2. **python slow_analysis.py** - runs the analysis of the position error during his deslocation. Plots are shown to demonstrate the results.

Note: this scripts must be executed on the folder were they are.

***

## Obtaining data from tag

We implemented a script to capture data from tag using the serial port. This script is used mainly just to acquire the data and store it for future processing.

<img>
