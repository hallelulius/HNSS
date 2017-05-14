#!/usr/bin/python

import serial
import time
import sys

def sendResponse(i):
	ser = serial.Serial('/dev/ttyACM0', 115200)
	ser.flush()
	time.sleep(0.2)
	ser.write(str(i))
	time.sleep(4)  # wait for arduino
	bytesToRead = ser.inWaiting()
	response = ser.read(bytesToRead)
	return str(response.rstrip())
