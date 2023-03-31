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
SYR_DECAP_POSE = np.array([-0.2024, -0.35907, 0.1809, 0, -1.53, 0])


