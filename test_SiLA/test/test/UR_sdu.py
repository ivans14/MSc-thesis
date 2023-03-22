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
home = [-0.15285, -0.25362, 0.33395, 2.404, 2.420, -2.432]
home_turned = [0.18865, -0.28095, 0.12454, 0.927, -1.365, 0.92]
setp3 = [0.13624, -0.32885, 0.17961, 0.37, 2.375, -2.338]
setp4 = [0.18865, -0.28095, 0.12454, 0.48, 2.377, -2.382]
setp5 = [0.1, 0, 0, 0, 0, 0]
setp1 = [-0.4104577419847799, -0.2626529489715343, 0.2972660465054066, 1.8552623321968715, 2.420037547531281, -0.014278932653435552]
setp2 =  [-0.2646567753143876, -0.43843427581831246, 0.2897307437164788, -1.54430191234484, -2.6607790325617, 0.17527592292018854]
turn_x = 0.3
con = RTDEControl(Ip)
rec = RTDEReceive(Ip)

print(rec.getActualTCPPose())
# con.moveL(home_turned, 0.1)
turn = np.pi/2
curr = con.getInverseKinematics(home_turned)
# curr[-1] += turn
# print(curr)
con.moveJ(curr)

# con.moveL(home_turned)
# print("new", con.getInverseKinematics(pos_turn[6:]))
# con.moveL(setp4, 0.1)
# pos_1 = con.getInverseKinematics(setp1)
# con.moveJ(pos_1, 0.5)
# pos_q = con.getInverseKinematics(setp4)
# con.moveL(setp3, 0.2)
# dash.loadURP('grip_syringe.urp')
# dash.play()
# print("gripping")
# time.sleep(3)
# dash.stop()
# dash.quit()
# print("moving to pos 2")
# con.reuploadScript()
# time.sleep(0.1)
# pos_2 = con.getInverseKinematics(setp2)
# con.moveJ(pos_2)


