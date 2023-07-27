from abc import ABC, abstractmethod
import os
# import rtde library
from typing import Any
from pathlib import Path

class URRobotAbs(ABC):
    def __init__(self) -> None:
        pass
    
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def check_connection(self):
        pass

    @abstractmethod
    def go_home(self):
        pass

    @abstractmethod
    def grip_syr(self):
        pass

    @abstractmethod
    def grip_pen(self):
        pass
    
    @abstractmethod
    def select_n_play(self):
        pass
    