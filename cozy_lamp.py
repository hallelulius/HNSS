#!/usr/bin/env python
import RPi.GPIO as GPIO

import time

# pin 18 - brightness up
# pin 23 - light color
# pin 24 - brightness down
#pin 25 - power
#18 23 24 25

pins = [18, 23, 24, 25, 7, 8]

GPIO.setmode(GPIO.BCM)
for i in range(0,6):
	GPIO.setup(pins[i], GPIO.OUT)

GPIO.output(pins[4], GPIO.HIGH)
GPIO.output(pins[5], GPIO.LOW)
while True:
	time.sleep(0.2)
	GPIO.output(pins[2], GPIO.HIGH)
      	time.sleep(0.2)
     	GPIO.output(pins[2], GPIO.LOW)
      	time.sleep(0.5)
      	GPIO.output(pins[3], GPIO.HIGH)
      	time.sleep(0.2)
      	GPIO.output(pins[3], GPIO.LOW)
      	time.sleep(0.5)
GPIO.cleanup()
