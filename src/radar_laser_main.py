import serial
import binascii
import time
import numpy as np
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


def main():
    ser = serial.Serial('/dev/serial0', 57600, bytesize=serial.EIGHTBITS,
                        parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=1.0)
    buf=['0','0','0','0','0']
    distance=0
    
    #Load and initialize library
    HeliosLib = ctypes.cdll.LoadLibrary("./libHeliosDacAPI.so")
    numDevices = HeliosLib.OpenDevices()
    print("Found ", numDevices, "Helios DACs")
    
    while 1:
        for num in range(4,0,-1):
            buf[num]=buf[num-1]
        buf[0] = ser.read()
        if buf[4] == b'\xff' and buf[3] == b'\xff' and buf[2] == b'\xff':
            distance = (int.from_bytes(buf[1],'little')*256+int.from_bytes(buf[0],'little'))*10
            #print(time.strftime("%a %b %d %H:%M:%S %Y", time.strptime(time.ctime())),int.from_bytes(buf[1],'little'),int.from_bytes(buf[0],'little'),distance, "\n")
            print(time.strftime("%a %b %d %H:%M:%S %Y :", time.strptime(time.ctime())),distance," mm")
        show_l(distance,numDevices,HeliosLib)
    
    ser.close()
    HeliosLib.CloseDevices()




def show_l(dist_y,numDevices,HeliosLib):
    # actual lenth per laser base lines 
    act_y=np.array([500 ,1000    ,2000      ,6000      ,10000])
    las_y=np.array([  0 ,1023.75 ,1023.75*2 ,1023.75*3 ,1023.75*4])

    frames = [0 for x in range(1)]
    frameType = HeliosPoint * 1000
    inc100=int(0xFFF)/99
    scr_y = -1

    if dist_y < act_y[0] or dist_y > act_y[-1]:
        scr_y = -1
    else:
        scr_y = round(  np.interp(dist_y,act_y,las_y))
        #print(dist_y)

        frames[0] = frameType()
        for i in range(100):
            frames[0][i] = HeliosPoint(int(inc100 * i), int(scr_y),0x0,0xFF,0x0,0xFF)

        for j in range(numDevices):
            statusAttempts = 0
            # Make 512 attempts for DAC status to be ready. After that, just give up and try to write the frame anyway
            while (statusAttempts < 512 and HeliosLib.GetStatus(j) != 1):
                statusAttempts += 1
            HeliosLib.WriteFrame(j, int(50000), 0, ctypes.pointer(frames[0]), 100)   #Send the frame

    return




if __name__ == "__main__":
    main()

