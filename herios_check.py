# -*- coding: utf-8 -*-
"""
Example for using Helios DAC libraries in python (using C library with ctypes)

NB: If you haven't set up udev rules you need to use sudo to run the program for it to detect the DAC.
"""

import ctypes

#Define point structure
class HeliosPoint(ctypes.Structure):
    #_pack_=1
    _fields_ = [('x', ctypes.c_uint16),
                ('y', ctypes.c_uint16),
                ('r', ctypes.c_uint8),
                ('g', ctypes.c_uint8),
                ('b', ctypes.c_uint8),
                ('i', ctypes.c_uint8)]

#Load and initialize library
HeliosLib = ctypes.cdll.LoadLibrary("./libHeliosDacAPI.so")
numDevices = HeliosLib.OpenDevices()
print("Found ", numDevices, "Helios DACs")

#Create sample frames
frames = [0 for x in range(5)]
frameType = HeliosPoint * 1000
x = 0
y = 0
inc100=int(0xFFF)/99
inc5=int(0xFFF)/4

print(inc100)
print(inc5)

for j in range(5):
    frames[j] = frameType()
    for i in range(100):
        frames[j][i] = HeliosPoint(round(inc100 * i), round(j * inc5),0x0,0xFF,0x0,0xFF)

#Play frames on DAC
while 1:
    for i in range(5):
        for j in range(numDevices):
            statusAttempts = 0
            # Make 512 attempts for DAC status to be ready. After that, just give up and try to write the frame anyway
            while (statusAttempts < 5120 and HeliosLib.GetStatus(j) != 1):
                statusAttempts += 1
            HeliosLib.WriteFrame(j, int(50000), 0, ctypes.pointer(frames[i]), 100)   #Send the frame

HeliosLib.CloseDevices()
