#!/usr/bin/env python
import RPi.GPIO as GPIO

import time

# pin 23 - light color
# pin 18 - brightness up
# pin 24 - brightness down
# pin 25 - power
#18 23 24 25

pins = [18, 23, 24, 25]

GPIO.setmode(GPIO.BCM)
for i in range(0,4):
	GPIO.setup(pins[i], GPIO.OUT)

GPIO.output(pins[3], GPIO.HIGH)
time.sleep(0.2)
GPIO.output(pins[3], GPIO.LOW)
time.sleep(0.5)
GPIO.cleanup()
