import matplotlib as mpl
import serial, time
import numpy as np
baudrate = 115200
port = serial.Serial('COM19', baudrate)
while True:
    line = port.readline().decode('UTF-8')
    data = line.split(',')
    if len(data) == 16:
        czas = data[1]
        yaw = float(data[4])
        pitch = float(data[5])
        roll = float(data[6])
        print("Czas: ", czas, " Yaw: ", yaw, " Pitch: ", pitch, " Roll: ", roll)
    else:
        print("Error in reading Serial. Trying again...")
    time.sleep(0.025)
