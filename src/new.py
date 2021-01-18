# coding: utf-8
# sudo apt install python3-pyaudio
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import threading
import time
assy=[0]
axis_x=[0]
CHUNK = 44100
RATE = 44100 # サンプリング周波数


def main():
    global rms,axis_x,ndarray_base
    fig, ax = plt.subplots()

    time.sleep(3)  
    axis_x = np.linspace(0.0, 1/RATE,CHUNK*10)
    line, = ax.plot(axis_x,rms,linewidth=2,color='red')
    plt.title("RMS[]")
    plt.xlabel("Tempo[Hz]")
    plt.ylabel("abs[]")
    #plt.xlim((0.0, CHUNK*10))
    #plt.ylim((-100, 100))
    fig.canvas.draw()
    fig.show() 
    while 1:
        try:
            line.set_ydata(rms)
            line.set_xdata(axis_x)
            ax.draw_artist(ax.patch)
            ax.draw_artist(line)
            fig.canvas.blit(ax.bbox)
            fig.canvas.flush_events() 
            time.sleep(0.1)     
        except KeyboardInterrupt:
            break
    return


    print('Stop Streaming')

def listen():
    global rms,axis_x
    rms=[0]*CHUNK*10
    P = pyaudio.PyAudio()
    FLAG=0
    stream = P.open(format=pyaudio.paInt16, channels=1, rate=RATE, frames_per_buffer=CHUNK, input=True, output=False)

    while stream.is_active():
        try:
            input = stream.read(CHUNK, exception_on_overflow=False)
            ndarray = np.frombuffer(input, dtype='int16')
            # bufferからndarrayに変換
            ''' 高速フーリエ変換をして時間領域から周波数領域にする場合は下1行を追加する '''
            # ndarrayからリストに変換
            # Pythonネイティブのint型にして扱いやすくする
            #assy = [np.asscalar(i) for i in ndarray]
            #assy = f

            for index in range(0,CHUNK*9):
                rms[index]=rms[index+CHUNK]
            rms[CHUNK*9:CHUNK*10] = ndarray

            
            ''' 音声を出力する場合はstreamのoutputをTrueにして下2行を追加する '''
            #output = np.array(assy, dtype='int16').tobytes()
            #stream.write(output)
        except KeyboardInterrupt:
            break

    stream.stop_stream()
    stream.close()
    P.terminate()




if __name__ == "__main__":
    t1 = threading.Thread(target=listen)
    
    # スレッドスタート
    t1.start()
    print('thread started')
    main()