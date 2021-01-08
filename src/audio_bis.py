# coding: utf-8
# sudo apt install python3-pyaudio
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import threading
import time


def main():
    global assy
    fig, ax = plt.subplots()
    line, = ax.plot(np.arange(0, 1024,1),np.arange(0, 1024,1) ,linewidth=2,color='red')

    plt.title("Distance[mm]")
    plt.xlabel("time[s]")
    plt.ylabel("Distance[mm]")
    plt.xlim((0.0, 1024))
    plt.ylim((-327, 327))
    fig.canvas.draw()
    fig.show() 
    while 1:
        try:
            line.set_ydata(assy)
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
    global assy
    CHUNK = 1024
    RATE = 44100 # サンプリング周波数
    P = pyaudio.PyAudio()
    stream = P.open(format=pyaudio.paInt16, channels=1, rate=RATE, frames_per_buffer=CHUNK, input=True, output=True)
    
    while stream.is_active():
        try:
            input = stream.read(CHUNK, exception_on_overflow=False)
            # bufferからndarrayに変換
            ndarray = np.frombuffer(input, dtype='int16')

            ''' 高速フーリエ変換をして時間領域から周波数領域にする場合は下1行を追加する '''
            f = np.fft.fft(ndarray)

            # ndarrayからリストに変換
            # Pythonネイティブのint型にして扱いやすくする
            assy = [np.asscalar(i) for i in ndarray]
            assy = f
            # 試しに0番目に入っているものを表示してみる


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