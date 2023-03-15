from rtde_control import RTDEControlInterface as RTDEControl
from rtde_receive import RTDEReceiveInterface as RTDEReceive
from dashboard_client import DashboardClient
import numpy as np
import socket
import time

Ip = '192.168.0.30'
BUFFER_SIZE = 4096
dash = DashboardClient(hostname=Ip)
dash.connect()
dash.powerOn()
dash.brakeRelease()
setp1 = [-0.4104577419847799, -0.2626529489715343, 0.2972660465054066, 1.8552623321968715, 2.420037547531281, -0.014278932653435552]
setp2 =  [-0.2646567753143876, -0.43843427581831246, 0.2897307437164788, -1.54430191234484, -2.6607790325617, 0.17527592292018854]

con = RTDEControl(Ip)
rec = RTDEReceive(Ip)
pos_q = con.getInverseKinematics(setp1)
con.moveJ(pos_q)
dash.loadURP('ivan.urp')
dash.play()
print("gripping")
# dash.stop()

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect((Ip, 44221))
# print("connected to gripper")
# c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# c.connect((Ip, 29999))
# SelectPlayProgram('ivan.urp', Ip, 29999)

