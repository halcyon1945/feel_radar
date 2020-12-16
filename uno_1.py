import serial
import binascii
import time
ser = serial.Serial('/dev/serial0', 57600, bytesize=serial.EIGHTBITS,
                    parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=1.0)
data_old = ""

while 1:
    data = ser.readline()
#    if data_old != data:
    print(time.strftime("%a %b %d %H:%M:%S %Y", time.strptime(time.ctime())),data, "\n")

    data_old = data
    time.sleep(0.3)

ser.close()
