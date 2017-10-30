#!/usr/bin/python
import time
import Adafruit_CharLCD as LCD
import os
import glob
import sys

#Pi pin configuration:
lcd_rs        = 25  
lcd_en        = 24
lcd_d4        = 23
lcd_d5        = 17
lcd_d6        = 21
lcd_d7        = 22
lcd_backlight = 4

# Specify 16x2 LCD
lcd_columns = 16
lcd_rows    = 2

# Initialize the LCD using the pins above.
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
							lcd_columns, lcd_rows, lcd_backlight)
#temperature sensor setup
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
max_min_file = '/home/pi/max_min'
 
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

def read_max_and_min():
	with open(max_min_file) as f:
		floats = map(float,f)
	return floats
def write_max_and_min(floats):
	with open(max_min_file, "w") as f:
		f.write("\n".join(map("{0:.1f}".format, floats)))
	

floats = read_max_and_min()
min_temp = min(floats)
min_temp_str = str(min_temp)
max_temp = max(floats)
max_temp_str = str(max_temp)
current_temp = read_temp()
current_temp_str = str(current_temp)
current_temp = read_temp()
if current_temp < min_temp:
	min_temp = current_temp
if current_temp > max_temp:
	max_temp = current_temp
current_temp_str = str(current_temp)
min_temp_str = format(min_temp, '.1f')
max_temp_str = format(max_temp, '.1f')
lcd.clear()
#lcd.message('Current ' + current_temp_str + 'C\nMin/Max ' + min_temp_str + 'C')
#time.sleep(5)
lcd.clear()
lcd.message('Current ' + current_temp_str + 'C\nM+- ' + max_temp_str + 'C/' + min_temp_str + 'C')
write_max_and_min((min_temp, max_temp))	

