import os 
import glob 
import datetime 

os.system('modprobe w1-gpio') 
os.system('modprobe w1-therm') 

device1 = '28-000003ebcc16' 
device2 = '28-000004a0ce39'

base_dir = '/sys/bus/w1/devices/' 
device1_folder =base_dir + device1
device1_file = device1_folder + '/w1_slave' 
device2_folder = base_dir + device2
device2_file = device2_folder + '/w1_slave'

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
	temp_c_str = format(temp_c, '.1f')
    return temp_c_str


st = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
print('<li>Outdoor temperature: ' + read_temp(device1_file)+ ' C</li>')
print('<li>Indoor temperature: ' + read_temp(device2_file) + ' C</li>')
print('<li>last updated at: ' + st + '</li>')
