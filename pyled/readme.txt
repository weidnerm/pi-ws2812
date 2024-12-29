led2812 python raspberry pi direct info
works on raspberry pi zero 2 w

python3 -m venv .venv
.venv/bin/pip3 install rpi_ws281x
.venv/bin/pip3 install adafruit-circuitpython-neopixel
.venv/bin/pip3 install --force-reinstall adafruit-blinka

sudo vi /boot/firmware/config.txt
	update to 
dtparam=audio=off

from
https://core-electronics.com.au/guides/raspberry-pi/fully-addressable-rgb-raspberry-pi/

