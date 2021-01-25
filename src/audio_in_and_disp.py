# coding: utf-8
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import threading
import time
import math
import ctypes

# Tune-setting
input_interval = 1/10  # sec
draw_length = 1.0  # sec
audio_sampling_rate = 44100  # Hz
max_draw_points = 4096  # limited by ILDA

# pre-calc
# buffer size for one time
CHUNK = math.ceil(audio_sampling_rate * input_interval)
draw_cycle = math.ceil(draw_length / input_interval)  # ten times for disp
draw_cycle_window = math.ceil(max_draw_points / draw_cycle) # 409 points for each window
local_resampling_window = math.ceil(CHUNK / draw_cycle_window)

# init global val
draw_axis_x_for_matplot = [0]*max_draw_points
draw_y_value = [0]*4096
input_raw_y_value = [0]*CHUNK*draw_cycle

# this func has two thread and 1 main .
# main thread is for matplot
# listen thread is for scanning audio
# thread_ls_draw is for lazer output



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
    global draw_axis_x_for_matplot
    fig, ax = plt.subplots()
    time.sleep(3)
    draw_axis_x_for_matplot = np.linspace(0.0,draw_length, max_draw_points )
    line, = ax.plot(draw_axis_x_for_matplot, draw_y_value, linewidth=2, color='red')
    plt.title("audio wave draw")
    plt.xlabel("time[sec]")
    plt.ylabel("volume[abs level]")
    # plt.xlim((0.0, CHUNK*10))
    plt.ylim((-32767, 32767))
    fig.canvas.draw()
    fig.show()

    while 1:
        try:
            line.set_ydata(draw_y_value)
            line.set_xdata(draw_axis_x_for_matplot)
            ax.draw_artist(ax.patch)
            ax.draw_artist(line)
            fig.canvas.blit(ax.bbox)
            fig.canvas.flush_events()
            time.sleep(0.1)
        except KeyboardInterrupt:
            print('Stop Streaming')
            break
    return


def listen_callback(in_data, frame_count, time_info, status):
    global input_raw_y_value
    # input buffering
    input_raw_y_value_temp = input_raw_y_value
    input = in_data
    ndarray = np.frombuffer(input, dtype='int16')
    # move window
    for index in range(0, int(CHUNK*(draw_cycle - 1))):
        input_raw_y_value_temp[index] = input_raw_y_value[index+CHUNK]

    # update latest data
    input_raw_y_value_temp[CHUNK*(draw_cycle - 1):(CHUNK*draw_cycle)]=ndarray
    # rewrite global value
    input_raw_y_value_temp=input_raw_y_value

    return(None, pyaudio.paContinue)

def listen():
    global input_raw_y_value
    # input audio setting
    P = pyaudio.PyAudio()
    stream = P.open(format=pyaudio.paInt16, channels=1, rate=audio_sampling_rate,
                    frames_per_buffer=CHUNK, input=True, output=False,stream_callback=listen_callback)
    while stream.is_active():
        try:
            time.sleep(0.1)
        except KeyboardInterrupt:
            stream.stop_stream()
            stream.close()
            P.terminate()
            break
    return

def thread_ls_draw():
    # 00ms task
    global draw_y_value
    # Load and initialize library
    HeliosLib=ctypes.cdll.LoadLibrary("./libHeliosDacAPI.so")
    numDevices=HeliosLib.OpenDevices()
    print("Found ", numDevices, "Helios DACs")
    while True:
        try:
            # resampling
            index=0
            local_resample_buf=0
            for num in range(len(input_raw_y_value)):
                local_resample_buf=local_resample_buf + input_raw_y_value[num]
                if num % local_resampling_window == local_resampling_window-1:
                    # calc average
                    draw_y_value[index]=math.ceil(local_resample_buf / local_resampling_window)
                    index += 1
                    local_resample_buf=0
            
            #show_ls(draw_y_value, numDevices, HeliosLib)
            #time.sleep(0.05)
        except KeyboardInterrupt:
            HeliosLib.CloseDevices()
            break
    return

def show_ls(input_y, numDevices, HeliosLib):

    frames=[0 for x in range(1)]
    frameType=HeliosPoint * max_draw_points
    frames[0]=frameType()
    for i in range(max_draw_points):
        frames[0][i]=HeliosPoint(int(i), int(input_y[i]), 0x0, 0xFF, 0x0, 0xFF)

    for j in range(numDevices):
        statusAttempts=0
        # Make 512 attempts for DAC status to be ready. After that, just give up and try to write the frame anyway
        while (statusAttempts < 512 and HeliosLib.GetStatus(j) != 1):
            statusAttempts += 1
        HeliosLib.WriteFrame(j, int(30000), 1, ctypes.pointer(
            frames[0]), max_draw_points)  # Send the frame

    return


if __name__ == "__main__":
    t1=threading.Thread(target = listen)
    t2=threading.Thread(target = thread_ls_draw)

    # スレッドスタート
    t1.start()
    t2.start()
    print('thread started')
    main()
