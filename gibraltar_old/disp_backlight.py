#!/usr/bin/env python
import time
import sys 
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
switch_pin = 8
GPIO.setup(GREEN_LED, GPIO.OUT)

args = str(sys.argv[1])
print(args)
if args == 'off':
	GPIO.output(switch_pin, False)
if args =='on':
	GPIO.output(switch_pin, True)
