#!/usr/bin/env python

import pigpio
pi = pigpio.pi()

pi.set_mode(15, pigpio.OUTPUT)
pi.set_mode(18, pigpio.OUTPUT)  # gpio 17 as output

pi.write(15, 0)
pi.write(18, 0)
# pi.write(18, 1)
