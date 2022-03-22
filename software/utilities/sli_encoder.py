"""
Script for capturing encoder pulses and get a timestamp from the arduino serial port
"""
import serial, time, io, datetime

port = "COM5" ## serial port to read data from
baud = 115200 ## baud rate for instrument

ser = serial.Serial(
    port = port,\
    baudrate = baud,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
    timeout=0)

print("Connected to: " + ser.portstr)

while True:
    data = ser.readline().decode()
    if data != '':
        f = open("encoder", "a")
        print(data)
        f.write(str(datetime.datetime.now().time()) + "," + data)
        f.close()

ser.close()