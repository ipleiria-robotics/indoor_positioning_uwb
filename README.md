# indoor_positioning_uwb

## Overview

Development and testing of an indoor positioning system based on UWB. 

The **MDEK1001 Development-kit**, containing 12 DWM1001 modules/development boards were used. We adapted the examples from the Decawave's repository to program an "anchor" version and a "tag" version. The **SEGGER embedded Studio for ARM 5.70a** was the IDE used to develop firmware.

For the data analysing tools Python scripts were developed and using common packages.

Another scripts were developed to help depending on the type of tests elaborated. More description in the follow.

***

## Software tools requirements

The requirements for the usage of this repository software:

- Installation of the IDE Segger to compile and program the devices DWM1001. To setting up the environment follow instructions from original Decawave's repository ([dwm1001-examples](https://github.com/Decawave/dwm1001-examples)). There you can see theadicional packages to install to compile the projects. It is important to fefer that, after the IDE installation, following the Decawave instructions, some options may need some corrections (if some change occour) and the user must be carefull with the size and format of the folderpath from where the project is running.

- Installation of Python 3.7.5 and install the packages require to run the scripts.

**Note:** during ours test we used Arduino IDE to count pulses from an encoder attached to a linear conveyor. The script used is store on the Firwamre folder too.

***

## Another used tools (Groud-truth):

For the measurement of the ground-truth data to compare with the distances and positions estiamted another equipments were used.

- Theodelite to obtain the coordinates in cartesian axis format from the anchors and the tag.

- Laser distance meter to measure the real distances between two devices.

- An encoder used to obtain the pulses on relative to the conveyor we used to execute the dynamic tests.

**Note:** We used this equipment but the user is free to use any other types of equipment to obtain the real values of distances and positions.

More explanations can be found on each folder on the repository container.

***

## Respository Description

In this repository exists the firmware used on the different devices and the different scripts in Python wich we used.

We used Python scripts to obtain the data, reading the serial port from the tag, and to store on a csv format the data acquired. 

Later, to calculate the position using the ranges, we used the Iterative Least-square to determine a 3D position.

All the analyses were made using Python too.

We uploaded some dataset with data referring to 3 different examples of a static position test and 2 examples with different velocities on a dynamic test.

That data can be consulted on the dataset folder.

A file containing the 8 anchors installed for our test is uploaded too. This is a important point that it must be studied. The installation of the anchor must be done using the concepts like Dillution of Precision (GDOP) and respecting some manufactor conditions too. 

## Description of  the elaborated tests

Here we show a representation of the installation and respectives coordinates used.

<img title="" src="https://github.com/ipleiria-robotics/indoor_positioning_uwb/blob/main/img/sala_info.jpg" alt="">

We used this anchors disposition because we wanted to have Line-of-sight most of the comunications/positions and we have a limit on the height (3 meters). Aditional, we wanted the tag to be located inside off the area defined from the anchors. To test the localization was decided to elaborate 2 types of tests, statics and dynamics. This way it is possible to tet both situations with different difficulties. The static test was elaborated testing LOS or NLOS situations and the dynamic test were executed with different velocities on a linear conveyor moved by a DC motor.

Using the instrumentation described before we obtained the real positions of each anchor.

#### Static Tests

The static tests were divided on three situations:

1. Teste 1 - Static test with all 8 anchors with LOS situation to the tag.

2. Teste 2 - Static test in the same previous position but with the anchor 5 on NLOS situation. As the next figure shows, we used a metalic board on the ceil near the anchor 5.

3. Teste 3 - Static test on a position were exists many NLOS commucations between anchors and tag.

<img title="Optional title" src="https://github.com/ipleiria-robotics/indoor_positioning_uwb/blob/main/img/static.png" alt="Alt text">

#### Dynamic Tests

For the dynamic test, were executed using two different velocities on the conveyor. One with a slow velocity and another with fast velocity. To execute the correspondent python scripts to generate positions and then analysis:

1. Slow - Test with a low velocity

2. Fast - Test with a high velocity

<img title="" src="https://github.com/ipleiria-robotics/indoor_positioning_uwb/blob/main/img/movimento1.jpg" alt="">

#### Devices firmware usage

For all tests, we used the UWB configuration of 128 preamble, with 6.81Mbps, channel 5 and prf of 64MHz. We used the same tag for all the elaborated tests and the anchors were on the same position on every tests. On the Firmware folder are described more information about the usage of the firmware used on the anchors an tag and to use them. The development were based on the Decawave's simple examples repository. So we made a Fork from their repository and created two branches, one for the anchors firmware and another for the tag firmware.

#### Python Scripts usage

The usage of the Python scripts were basically to read and store the data from the tag and then too run a post-processing data to compute the localization and errors analysis. On the Software folder more information can be found.
