# feel_radar
Radar usage



make env memo
OpenCV2
```pip install opencv-python```

Raspi-config to ubuntu20
```
wget https://archive.raspberrypi.org/debian/pool/main/r/raspi-config/raspi-config_20200601_all.deb -P /tmp
sudo apt-get install libnewt0.52 whiptail parted triggerhappy lua5.1 alsa-utils -y
sudo apt-get install -fy
sudo dpkg -i /tmp/raspi-config_20200601_all.deb

cd /boot/
sudo ln -s ./firmware/config.txt config.txt
sudo ln -s ./firmware/cmdline.txt cmdline.txt
```
and check serial consol disable.
config.txt
```
#Bluetooth機能を切り替えて、Bluetoothモジュールとの接続をUART0からmini UARTを使用するように切り替えを行い、UART0（1番目のPL011）をPrimary UARTにします。
core_freq=250
enable_uart=1
dtoverlay=disable-bt
```

cmdline.txt
```
dwc_otg.lpm_enable=0 console=tty1 root=LABEL=writable rootfstype=ext4 elevator=deadline rootwait fixrtc quiet splash
```