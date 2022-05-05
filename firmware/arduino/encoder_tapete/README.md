# Encoder-tapete

## Overview

This a simple Arduino script used to count the pulses from the encoder attached to a linear conveyor actuator. With the pulses count, it is possible to estimat the  tag motion on the conveyor during the dynamic position tests. The Arduino used was an Arduino Uno Rev3 SMD and the encoder was the EC12E24204A8.

The pinout used to read the pulses was:

```
int encoder0PinA = 2; //GPIO pin 2 -> Encoder A
int encoder0PinB = 4; //GPIO pin 4 -> Encoder B
```

The script is just reading each pin input digital values, counting the pulses based edge-triggering, and printing the result on the serial port. Having this data available through the serial port, another program can be used to read the serial port and obtain the position estimate and the corresponding timestamp when that data was captured. 

The following image shows the connection between the Arduino and the encoder that were used:

<img title="" src="https://github.com/ipleiria-robotics/indoor_positioning_uwb/blob/main/img/encoder_arduino.jpg" alt="" data-align="inline">

***
