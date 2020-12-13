import serial
import binascii
import time
ser=serial.Serial('/dev/serial0',115200,timeout=0.5)
data_old=""

while 1 :
    data=ser.readline()
    if data_old != data:
        print(data)

    data_old = data
    time.sleep(0.3)

ser.close()