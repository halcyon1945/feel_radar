import serial
import binascii
import time
import numpy as np
import ctypes
import matplotlib.pyplot as plt
import threading


# global variable
graph_dist=[0]*101
distance = 0


class HeliosPoint(ctypes.Structure):
    # _pack_=1
    _fields_ = [('x', ctypes.c_uint16),
                ('y', ctypes.c_uint16),
                ('r', ctypes.c_uint8),
                ('g', ctypes.c_uint8),
                ('b', ctypes.c_uint8),
                ('i', ctypes.c_uint8)]


def main():
    #draw task 100ms
    global graph_dist 
    global distance
    while 1:
        plt.plot(np.arange(0., 10.1, 0.1),graph_dist)  
        plt.title("Distance[mm]")
        plt.xlabel("time[s]")
        plt.ylabel("Distance[mm]")
        plt.xlim((0.0, 10.1))
        plt.ylim((0.0, 11000))
        plt.draw()  
        plt.pause(0.1)  
        plt.cla() 
        
def thread_distance_array():
    #100ms task
    global graph_dist 
    global distance
    while 1:
        for num in range(1, 101):
            graph_dist[num-1] = graph_dist[num]
        graph_dist[100] = distance
        time.sleep(0.1)

def thread_radar_read():
    # no wait
    global distance
    distance_prev = distance
    ser = serial.Serial('/dev/serial0', 57600, bytesize=serial.EIGHTBITS,
                        parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=1.0)
    buf = ['0', '0', '0', '0', '0']
    while True:
        for num in range(4, 0, -1):
            buf[num] = buf[num - 1]
        buf[0] = ser.read()
        if buf[4] == b'\xff' and buf[3] == b'\xff' and buf[2] == b'\xff':
            distance = (int.from_bytes(buf[1], 'little') * 256 + int.from_bytes(buf[0], 'little')) * 10
            if round(distance / 100) != round(distance_prev / 100):
                print(time.strftime("%a %b %d %H:%M:%S %Y :", time.strptime(time.ctime())), distance, " mm")
            distance_prev = distance
    ser.close()


def thread_ls_draw():
    #300ms task
    global distance
    # Load and initialize library
    HeliosLib = ctypes.cdll.LoadLibrary("./libHeliosDacAPI.so")
    numDevices = HeliosLib.OpenDevices()
    print("Found ", numDevices, "Helios DACs")
    while True:
        show_ls(distance, numDevices, HeliosLib)
        time.sleep(0.3)
    HeliosLib.CloseDevices()

def show_ls(dist_y, numDevices, HeliosLib):
    # actual lenth per laser base lines
    act_y = np.array([300, 301, 303, 1200, 9000])
    las_y = np.array([0, 1023.75, 1023.75 * 2, 1023.75 * 3, 1023.75 * 4])

    frames = [0 for x in range(1)]
    frameType = HeliosPoint * 100
    inc100 = int(0xFFF) / 99
    scr_y = -1

    if dist_y < act_y[0] or dist_y > act_y[-1]:
        scr_y = -1
    else:
        scr_y = round(np.interp(dist_y, act_y, las_y))
        # print(dist_y,scr_y)

        frames[0] = frameType()
        for i in range(80):
            frames[0][i] = HeliosPoint(int(inc100 * i + inc100 * 20), int(scr_y), 0x0, 0xFF, 0x0, 0xFF)

        for j in range(numDevices):
            statusAttempts = 0
            # Make 512 attempts for DAC status to be ready. After that, just give up and try to write the frame anyway
            while (statusAttempts < 512 and HeliosLib.GetStatus(j) != 1):
                statusAttempts += 1
            HeliosLib.WriteFrame(j, int(30000), 1, ctypes.pointer(frames[0]), 80)  # Send the frame

    return

if __name__ == "__main__":
    t1 = threading.Thread(target=thread_radar_read)
    t2 = threading.Thread(target=thread_ls_draw)
    t3 = threading.Thread(target=thread_distance_array)
    
    # スレッドスタート
    t1.start()
    t2.start()
    t3.start()
    print('thread started')
    main()
