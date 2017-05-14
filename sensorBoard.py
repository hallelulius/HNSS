#!/usr/bin/env python

# reads sensor values from dallas ds1820b, DHT 11 and BMP085

import socket
import os
import datetime
import time
import DHT11 as DHT11
import pigpio
import Adafruit_BMP.BMP085 as BMP085

# ds1820b settings (temperature)
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

device1 = '28-011590a191ff'

base_dir = '/sys/bus/w1/devices/'
device1_folder = base_dir + device1
device1_file = device1_folder + '/w1_slave'

def read_temp_raw(device_file):
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines


def read_ds1820b():
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')

    device = '28-011590a191ff'

    base_dir = '/sys/bus/w1/devices/'
    device_folder = base_dir + device1
    device_file = device1_folder + '/w1_slave'
    
    lines = read_temp_raw(device_file)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw(device_file)
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
    return temp_c

def read_DHT11():
    pi = pigpio.pi()
    pin = 17
    sensor = DHT11.DHT11(pi, pin)
    response = sensor.next()
    sensor.close()
    return response

def read_BMP085():
    sensor = BMP085.BMP085()
    return [sensor.read_temperature(), sensor.read_pressure(), sensor.read_altitude(), sensor.read_sealevel_pressure()]


print(read_ds1820b())
print(read_DHT11())
print(read_BMP085())
  
