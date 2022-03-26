# Encoder-tapete

## Overview

This a simple Arduino script used to count encoder pulses attached to a linear conveyor. With the pulses count it was possible to restore an approximate tag travel on the conveyor during the dynamic position tests. The Arduino used was a Arduino Uno Rev3 SMD and the encoder was the EC12E24204A8.

The pinout used to read the pulses were:

```
int encoder0PinA = 3; //GPIO pin 3 -> Encoder A
int encoder0PinB = 4; //GPIO pin 4 -> Encoder B
```

The simple functioning of this script is just reading the pinout values, count the pulses and printing it on the Serial Port. With this, another program can be used to read ther Serial Port and obtain the timestamp when they occur. 

The next image shows the connection between an example of Arduino and the encoder used:

<img title="" src="https://github.com/ipleiria-robotics/indoor_positioning_uwb/blob/main/img/encoder_arduino.jpg" alt="" data-align="inline">

***
