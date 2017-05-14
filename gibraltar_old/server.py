#!/usr/bin/env python

import socket
import os
import datetime
import time
import pigpio
import arduinoCom as ac

# for accesing GPIO without root
pi = pigpio.pi()

# for temperature
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

device1 = '28-000003ebcc16'
device2 = '28-000004a0ce39'

base_dir = '/sys/bus/w1/devices/'
device1_folder = base_dir + device1
device1_file = device1_folder + '/w1_slave'
device2_folder = base_dir + device2
device2_file = device2_folder + '/w1_slave'


# temperature functions
def read_temp_raw(device_file):
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines


def read_temp(device_file):
    lines = read_temp_raw(device_file)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw(device_file)
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
    return temp_c


# like lamp functions
def blink_lamp():
    pi.set_mode(15, pigpio.OUTPUT)  # gpio 15 as output uses BCM standard
    pi.set_mode(18, pigpio.OUTPUT)  # gpio 18 as output
    pi.write(15, 0)
    pi.write(18, 0)
    time.sleep(3)
    pi.write(15, 1)
    pi.write(18, 1)


def lamp_on():
    pi.set_mode(15, pigpio.OUTPUT)
    pi.set_mode(18, pigpio.OUTPUT)
    pi.write(15, 0)
    pi.write(18, 0)


def lamp_off():
    pi.set_mode(15, pigpio.OUTPUT)
    pi.set_mode(18, pigpio.OUTPUT)
    pi.write(15, 1)
    pi.write(18, 1)


# response from the server
def response(data):
    if data == 'time':
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if data == 'indoor':
        return str(read_temp(device2_file))
    if data == 'outdoor':
        return str(read_temp(device1_file))
    if data == 'lamp_on':
        return 'lamp is on'
    if data == 'lamp_off':
        return 'lamp is off'
    if data == 'blink':
        return 'lamp is lit'
    if data == 'sensor_help':
        return ac.sendResponse(0)
    if data == 'sensor_all':
	return ac.sendResponse("1 2 3 4 5 6")
    if data == '1':
        return ac.sendResponse(1)
    if data == '2':
        return ac.sendResponse(2)
    if data == '3':
        return ac.sendResponse(3)
    if data == '4':
        return ac.sendResponse(4)
    if data == '5':
        return ac.sendResponse(5)
    if data == '6':
        return ac.sendResponse(6)
    if data == '7':
        return 'use \'SLPvalue\' instead'
    if data[0:3] == 'SLP':  # fix for automatic SLP updates
        ac.sendResponse(7)
        time.sleep(4)  # wait for arduino
        return ac.sendResponse(data[3:])
    elif data == 'help':
        return ('I can send you: \n' +
                'current time (time)\n' +
                'indoor temperature (indoor) \n' +
                'outdoor temperature (outdoor) \n' + 
		'sensor data (sensor_all) \n' +
                'I can also: \n'
                'light a lamp (blink),(lamp_on),(lamp_off) \n' +
                'for more try (sensor_help)')
    else:
        return (data + ' not found in command list, try \'help\'')


# function to change GPIOs on the pi
def action(data):
    if data == 'blink':
        blink_lamp()
    elif data == 'lamp_on':
        lamp_on()
    elif data == 'lamp_off':
        lamp_off()


# for server
TCP_IP = '192.168.42.2'
TCP_PORT = 5005
BUFFER_SIZE = 64  # Normally 1024, but we want fast response


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((TCP_IP, TCP_PORT))
s.listen(10)

while 1:
    conn, addr = s.accept()
    print('Connection address:', addr)
    while 1:
        data = conn.recv(BUFFER_SIZE)
        if not data:
            break
        print("received data:", data)
        res = response(data)
        print("response :", res)
        action(data)
        conn.send(res.rstrip())
    conn.close()
