# coding: utf-8
# sudo apt install python3-pyaudio
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import threading
import time
import math
assy=[0]
axis_x=[0]
CHUNK = int(44100/10)
RATE = 44100 # サンプリング周波数
resampling_interval = math.ceil(RATE/4096)
rms_re=[0]*4096

def main():
    global rms,axis_x,ndarray_base,rms_re
    rms_buf=0
    fig, ax = plt.subplots()

    time.sleep(3)  
    axis_x = np.linspace(0.0, resampling_interval/RATE,4096)
    line, = ax.plot(axis_x,rms_re,linewidth=2,color='red')
    plt.title("RMS[]")
    plt.xlabel("time[sec]")
    plt.ylabel("abs[]")
    #plt.xlim((0.0, CHUNK*10))
    plt.ylim((-32767, 32767))
    fig.canvas.draw()
    fig.show() 
    rms_max=0

    while 1:
        try:
            index=0
            for num in range(len(rms)):
                rms_buf=rms_buf + rms[num]
                if num % resampling_interval ==resampling_interval-1:
                   rms_re[index]=int(rms_buf / resampling_interval) 
                   index +=1
                   rms_buf=0
            line.set_ydata(rms_re)
            line.set_xdata(axis_x)
            ax.draw_artist(ax.patch)
            ax.draw_artist(line)
            fig.canvas.blit(ax.bbox)
            fig.canvas.flush_events() 
            time.sleep(0.5)     
        except KeyboardInterrupt:
            break
    return


    print('Stop Streaming')

def listen():
    global rms,axis_x
    rms0=[0]*CHUNK*10
    P = pyaudio.PyAudio()
    FLAG=0
    stream = P.open(format=pyaudio.paInt16, channels=1, rate=RATE, frames_per_buffer=CHUNK, input=True, output=False)

    while stream.is_active():
        try:
            input = stream.read(CHUNK, exception_on_overflow=False)
            ndarray = np.frombuffer(input, dtype='int16')
            for index in range(0,CHUNK*9):
                rms0[index]=rms0[index+CHUNK]
            rms0[CHUNK*9:CHUNK*10] = ndarray
            rms=rms0

        except KeyboardInterrupt:
            break

    stream.stop_stream()
    stream.close()
    P.terminate()

def thread_ls_draw():
    ##00ms task
    global rms_re
    # Load and initialize library
    HeliosLib = ctypes.cdll.LoadLibrary("./libHeliosDacAPI.so")
    numDevices = HeliosLib.OpenDevices()
    print("Found ", numDevices, "Helios DACs")
    while True:
        show_ls(rms_re, numDevices, HeliosLib)
        time.sleep(0.1)
    HeliosLib.CloseDevices()

def show_ls(dist_y, numDevices, HeliosLib):

    frames = [0 for x in range(1)]
    frameType = HeliosPoint * 4096
    frames[0] = frameType()
    for i in range(4096):
        frames[0][i] = HeliosPoint(int(i), int(rms_re[i]),0x0,0xFF,0x0,0xFF)

    for j in range(numDevices):
        statusAttempts = 0
        # Make 512 attempts for DAC status to be ready. After that, just give up and try to write the frame anyway
        while (statusAttempts < 512 and HeliosLib.GetStatus(j) != 1):
            statusAttempts += 1
        HeliosLib.WriteFrame(j, int(30000), 1, ctypes.pointer(frames[0]), 4096)  # Send the frame

    return


if __name__ == "__main__":
    t1 = threading.Thread(target=listen)
    t2 = threading.Thread(target=thread_ls_draw)
    
    # スレッドスタート
    t1.start()
    t2.start()
    print('thread started')
    main()