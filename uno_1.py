import serial
import binascii
import time
ser = serial.Serial('/dev/serial0', 57600, bytesize=serial.EIGHTBITS,
                    parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=1.0)
buf=['0','0','0','0','0']

while 1:
    for num in range(4,0,-1):
        buf[num]=buf[num-1]
    buf[0] = ser.read()
    if buf[4] == b'\xff' and buf[3] == b'\xff' and buf[2] == b'\xff':
        distance = int.from_bytes(buf[1],'little')*256+int.from_bytes(buf[0],'little')
        print(time.strftime("%a %b %d %H:%M:%S %Y", time.strptime(time.ctime())),int.from_bytes(buf[1],'little'),int.from_bytes(buf[0],'little'),distance, "\n")

ser.close()
