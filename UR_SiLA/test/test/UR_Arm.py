from abc import ABC, abstractmethod
# import rtde library
from .RTDE_Python.rtde import rtde as rtde
from .RTDE_Python.rtde import rtde_config as config
from typing import Any


class RobotInterface(ABC):
    def __init__(self) -> None:
        pass
    @abstractmethod
    def connect(self):
        print("connecting")
    @abstractmethod
    def check_connection(self):
        print("checking connection")
    @abstractmethod
    def move(self, input: list[float]):
        pass
class UR_Robot(RobotInterface):
    def __init__(self, host: Any, port: int) -> None:
        super(UR_Robot, self).__init__()
        self.host = host
        self.port = port
        self.connection = rtde.RTDE(self.host, self.port)
        self.connection.__conn_state = 0
        self.count = 0
    def connect(self):
        """initialize connection to robot"""
        # self.connection.connect()
        # if self.connection.__conn_state == 1:
        #     print("connected")
        # else: 
        #     print("unable to connect")
        self.connection.__conn_state = 1
        print("connected to robot")
        return not not self.connection.__conn_state
    def check_connection(self) -> bool:
        """check connection status"""
        self.count += 1
        print(self.count)
        if self.count ==15:
            self.connection.__conn_state = not self.connection.__conn_state
        if self.connection.__conn_state == 1:
            return True
        return False
    def move(self, input: list[float]):
        """from a 6D array, send command to robot to move to that setpoint"""
        print(f"moving to position {input}")
        # self.connection.send(input)