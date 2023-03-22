# -*- coding: utf-8 -*-
"""
Created on Wed Jun  1 13:42:59 2022

@author: lscimmi

Program: TCS_test: here some tests related to TCS control mode for PreciseFlex robots
         are performed.
"""

import socket
import struct
import time

IP_robot = "10.1.10.203"
PORT_robot = 10100
bytes_buffer = 128

tcs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

tcs.connect((IP_robot, PORT_robot))

st = "open 10.1.10.203 10100" + "\n" #verify if \r\n could also work
tcs.send(st.encode())

data = tcs.recv(bytes_buffer)
print(data)
# data_double = struct.unpack("<I",data[0:7])
# print(data_double)

time.sleep(5)

st = "attach 1" + "\n" #verify if \r\n could also work
tcs.send(st.encode())
data = tcs.recv(bytes_buffer)
print(data)
# data = tcs.recv(bytes_buffer)
# data_double = struct.unpack(...)
# print(data_double)
# data_single = struct.unpack(...)
# print(data_single)

time.sleep(5)

st = "MoveOneAxis 5 120 1" + "\n" #verify if \r\n could also work
tcs.send(st.encode())
data = tcs.recv(bytes_buffer)
print(data)

time.sleep(5)

st = "MoveOneAxis 5 80 1" + "\n" #verify if \r\n could also work
tcs.send(st.encode())
data = tcs.recv(bytes_buffer)
print(data)

time.sleep(5)

# st = "profile 2 25 0 10 10 0.5 0.5 10 0" + "\n" #verify if \r\n could also work
# tcs.send(st.encode())
# data = tcs.recv(bytes_buffer)
# print(data)

# time.sleep(5)

st = "LoadFile /flash/projects/Tcp_cmd_server_pa/Tcs.gpo" + "\n" #verify if \r\n could also work
tcs.send(st.encode())
data = tcs.recv(bytes_buffer)
print(data)

time.sleep(5)

st = "profile 2" + "\n" #verify if \r\n could also work
tcs.send(st.encode())
data = tcs.recv(bytes_buffer)
print(data)

time.sleep(5)

st = "MoveOneAxis 3 240 2" + "\n" #verify if \r\n could also work
tcs.send(st.encode())
data = tcs.recv(bytes_buffer)
print(data)

time.sleep(5)

st = "wherej" + "\n" #find the way to unpack the data and see them properly
tcs.send(st.encode())
data = tcs.recv(bytes_buffer)
print(data)
# data_double = struct.unpack(...)
# print(data_double)

time.sleep(5)

# st = "StoreFile /flash/projects/Tcp_cmd_server_pa/Tcs.gpo" + "\n" #verify if \r\n could also work
# tcs.send(st.encode())
# data = tcs.recv(bytes_buffer)
# print(data)

# time.sleep(5)

st = "mode 1" + "\n" #verify if \r\n could also work
tcs.send(st.encode())
data = tcs.recv(bytes_buffer)
print(data)

time.sleep(5)

st = "wherej" + "\n" #find the way to unpack the data and see them properly
tcs.send(st.encode())
data = tcs.recv(bytes_buffer)
print(data)
# data_double = struct.unpack(...)
# print(data_double)

time.sleep(15)

tcs.close()

