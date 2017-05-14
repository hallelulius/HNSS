#!/usr/bin/env python

import socket
import datetime
import time
import sensorBoard
import pickle


# response from the server
def response(data):
    if data == 'time':
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    elif data == 'sensors':
        return dict(
	    ds1820b=sensorBoard.read_ds1820b(),
            DHT11=sensorBoard.read_DHT11(),
            BMP085=sensorBoard.read_BMP085()
            )
    elif data == 'help':
        return ('I can send you: \n' +
                'current time (time)\n' +
                'sensor values (sensors)')
    else:
        return (data + ' not found in command list, try \'help\'')

# server settings
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
        conn.send(pickle.dumps(res))
    conn.close()
