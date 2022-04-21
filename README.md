# Indoor Localization System - UWB

## Overview

This repository describes the development and testing of an indoor positioning system based on UWB.

For this work, the **MDEK1001 Development-kit**, containing 12 DWM1001 modules/development boards, was acquired. Considering the limitations of the original firmware included with the devices, we adapted the firmware from the Decawave's “Getting Started” repository and, using the **SEGGER embedded Studio for ARM 5.70a**, we developed our [own firmware](https://github.com/ipleiria-robotics/indoor_positioning_uwb/tree/main/firmware/). We developed two versions, one for the devices working as anchors (reference points) and another for the device working as tag (device to be located). These devices are used only to obtain the distance measurements between the tag and the rest of the anchors. The position estimation, it is not executed on the tag.

At the same time, [we developed Python 3 scripts](https://github.com/ipleiria-robotics/indoor_positioning_uwb/tree/main/software#-indoor-localization-system---uwb---software-folder) to communicate with the tag via serial port to store the distance estimations on a csv file for post-analysis. 

After the dataset with the measurements stored, it is possible to preform the post-analysis. This post-analysis includes the position estimation with the dataset loaded and error analysis (plots, statistics).

***

## Requirements

#### Software tools requirements

To use the software made available in this repository, there are some requirements. First, one has to install all the needed development software:

- Install the IDE Segger to compile and program the DWM1001 devices. To set up the environment, follow the instructions from the original Decawave's repository ([dwm1001-examples](https://github.com/Decawave/dwm1001-examples)). There you can see the adicional packages to install to be able to compile the projects. At the same time, we recommend being careful with the folder path size where the project will be hosted. Avoid white spaces and long names on folders.

- Install Python 3 (version used 3.7.5) and the packages required to run the scripts. More information about the need packages on the [software](https://github.com/ipleiria-robotics/indoor_positioning_uwb/tree/main/software#-indoor-localization-system---uwb---software-folder) folder on this repository.

Note: In our case, we used the Arduino IDE to develop a sketch to capture an encoder pulses using an Arduino UNO R3. This is relative to a dynamic test elaborated.

#### Other used tools (Ground-truth):

For the measurement of the ground-truth data for comparison with the estimated distances and positions, third-party equipment was used:

- A theodelite, to obtain the coordinates of the anchors and the tag in world coordinates.

- Laser distance meter to measure the real distances between two devices.

- An encoder used to obtain the pulses and measure the traveling distance in a linear conveyor (for dynamic tests).

**Note:** We used this equipment but the user is free to use any other types of equipment to obtain the real distances and positions values for ground-truth evaluationn and error assessment.

More explanations can be found on each folder within this repository.

***

## Respository Description

This repository is divided in two main folders. The firmware folder is where all the firmware developed is stored. On the software folder you will find all the Python scripts that were developed for capturing and analysing data. In each folder there are guidelines explaining how to install the needed software and how to execute it.

#### Description of  the elaborated tests

Here we show a representation of the installation and respectives coordinates used.

<img title="" src="https://github.com/ipleiria-robotics/indoor_positioning_uwb/blob/main/img/sala_info.jpg" alt="">

We used this anchors placement because we wanted to have Line-of-Sight in a reasonable part of the lab, and because we have a limit on the height (3 meters). Aditionally, we wanted the tag to be located inside the area defined from the anchors. To test the localization estimation, 2 types of tests were specified: statics and dynamic. This approach allowed testing both situations with different difficulties. The static test was elaborated testing LOS or NLOS situations, and the dynamic test were executed with different velocities on a linear conveyor, moved by a DC motor. Using the theodolite mentioned before, we obtained the real position of each anchor.

#### [Static Tests](https://github.com/ipleiria-robotics/indoor_positioning_uwb/tree/main/software/static_test)

The static tests were divided in three situations:

1. Teste 1 - Static test with all 8 anchors in LOS situation to the tag.

2. Teste 2 - Static test in the same position has "Teste 1", but with the anchor 5 on a NLOS situation. As the next figure shows, we used a metalic board on the ceiling near the anchor 5 to force the NLOS situation.

3. Teste 3 - Static test on a position were many NLOS communications exist between anchors and tag.

<img title="Optional title" src="https://github.com/ipleiria-robotics/indoor_positioning_uwb/blob/main/img/static.png" alt="Alt text">

#### [Dynamic Tests](https://github.com/ipleiria-robotics/indoor_positioning_uwb/tree/main/software/movement_test)

The dynamic tests were executed using two different velocities on a linear conveyor, one with a slow velocity and another with a faster velocity. In order to properly evaluate the performance of this test, additional data was needed, namely a dataset with the real motion carried out by the tag. For that purpose, we used an encoder, attached to the motor controlling the conveyor motion.  An Arduino Uno R3 was used to read the pulses and together with Python script [sli_encoder.py](https://github.com/ipleiria-robotics/indoor_positioning_uwb/tree/main/software/utilities) running on a PC. During this test, the tag device was connected to a Raspberry Pi 3 to run the previous Python scripts presented.

All the data acquired was post-analysed to obtain the position estimated and error analysis. To execute the corresponding python scripts to generate positions and then analyse the results:

1. Slow - Test with a low velocity

2. Fast - Test with a high velocity

<img title="" src="https://github.com/ipleiria-robotics/indoor_positioning_uwb/blob/main/img/movimento1.jpg" alt="">
