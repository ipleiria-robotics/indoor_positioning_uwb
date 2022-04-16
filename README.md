# Indoor Localization System - UWB

## Overview

This repository describes the development and testing of an indoor positioning system based on UWB.

For this work, the **MDEK1001 Development-kit**, containing 12 DWM1001 modules/development boards, were acquired. Considering the limitations that the original firmware that comes with all the devices, it was necessary to developed our own firmware version. We adapted the simple version from the Decawave's “Getting Started” repository and using the **SEGGER embedded Studio for ARM 5.70a** we developed our own firmware version. We developed two versions, one for the devices working as anchors and the other for the devices working as tag.

At the same time, we developed Python 3 scripts to communicate with the localization device to store and post-analysing the resultant data. Using this scripts, it is possible to analyse the different test elaborated.

To obtain the ground-truth position values, we used a theodolite, so it is possible to obtain the positioning of error.

***

## Requirements

##### Software tools requirements

To use this repository, there are some requirements. First, it is necessary to install all the software used on the development.

- Installation of the IDE Segger to compile and program the devices DWM1001. To setting up the environment, follow instructions from original Decawave's repository ([dwm1001-examples](https://github.com/Decawave/dwm1001-examples)). There you can see the adicional packages to install to compile the projects. It is important to refer that, after the IDE installation and after all the Decawave's instructions, some corrections may occur. At the same time, we recommend being careful with the size folder path where the project will be downloaded.

- Installation of Python 3.7.5 and install the packages require to run the scripts. More information on the software module presented on this repository.

If there is a necessity to use the same code developed, the Arduino IDE must be installed to program the Arduino device.

##### Another used tools (Groud-truth):

For the measurement of the ground-truth data to compare with the distances and positions estiamted another equipments were used.

- Theodelite to obtain the coordinates in cartesian axis format from the anchors and the tag.

- Laser distance meter to measure the real distances between two devices.

- An encoder used to obtain the pulses on relative to the conveyor we used to execute the dynamic tests.

**Note:** We used this equipment but the user is free to use any other types of equipment to obtain the real values of distances and positions.

More explanations can be found on each folder on the repository container.

***

## Respository Description

This repository is divided on two main folders. The firmware folder where all the firmware developed is allocated wit the correspondent guide lines. On the software folder exist all the Python scripts developed to be used on capturing and analysing data. In each folder there are guidelines explaining how to install and to execute them.

##### Description of  the elaborated tests

Here we show a representation of the installation and respectives coordinates used.

<img title="" src="https://github.com/ipleiria-robotics/indoor_positioning_uwb/blob/main/img/sala_info.jpg" alt="">

We used this anchors disposition because we wanted to have Line-of-sight most of the comunications/positions and we have a limit on the height (3 meters). Aditional, we wanted the tag to be located inside off the area defined from the anchors. To test the localization was decided to elaborate 2 types of tests, statics and dynamics. This way it is possible to tet both situations with different difficulties. The static test was elaborated testing LOS or NLOS situations and the dynamic test were executed with different velocities on a linear conveyor moved by a DC motor.

Using the instrumentation described before we obtained the real positions of each anchor.

##### Static Tests

The static tests were divided on three situations:

1. Teste 1 - Static test with all 8 anchors with LOS situation to the tag.

2. Teste 2 - Static test in the same previous position but with the anchor 5 on NLOS situation. As the next figure shows, we used a metalic board on the ceil near the anchor 5.

3. Teste 3 - Static test on a position were exists many NLOS commucations between anchors and tag.

<img title="Optional title" src="https://github.com/ipleiria-robotics/indoor_positioning_uwb/blob/main/img/static.png" alt="Alt text">

##### Dynamic Tests

For the dynamic test, were executed using two different velocities on the conveyor. One with a slow velocity and another with fast velocity. To execute the correspondent python scripts to generate positions and then analysis:

1. Slow - Test with a low velocity

2. Fast - Test with a high velocity

<img title="" src="https://github.com/ipleiria-robotics/indoor_positioning_uwb/blob/main/img/movimento1.jpg" alt="">

For this test an aditional data is needed, a dataset with the real movement executed by the tag so it is possible to analyse the error. For that, the usage of an encoder to determine the increments of the linear conveyor.
