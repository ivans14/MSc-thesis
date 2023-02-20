import socket
import logging
# import rtde library
import sys
sys.path.append("RTDE_Python_Client_Library")
from .RTDE_Python_Client_Library.rtde import rtde as rtde
from .RTDE_Python_Client_Library.rtde import rtde_config as config
from typing import Any

class UR_Robot():
    def __init__(self, host: Any, port: int) -> None:
        self.host = host
        self.port = port
        self.connection = rtde.RTDE(self.host, self.port)
        self.connection.__conn_state = 0
    def connect(self):
        """initialize connection to robot"""
        # self.connection.connect()
        # if self.connection.__conn_state == 1:
        #     print("connected")
        # else: 
        #     print("unable to connect")
        print("not implemented")
    def check_connection(self) -> bool:
        """"check connection status"""
        if self.connection.__conn_state == 1:
            return True
        return False
    def move(self, input: list[float]):
        """from a 6D array, send command to robot to move to that setpoint"""
        self.connection.send(input)