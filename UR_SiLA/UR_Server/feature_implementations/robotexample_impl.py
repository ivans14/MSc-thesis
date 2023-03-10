# Generated by sila2.code_generator; sila2.__version__: 0.7.3
from __future__ import annotations

from typing import TYPE_CHECKING
from numpy.random import random
import time

from demo_server.hardware_interface import RobotInterface
from sila2.server import MetadataDict

from ..generated.robotexample import GoToHomePosition_Responses, RobotExampleBase

if TYPE_CHECKING:
    from ..server import Server


class RobotExampleImpl(RobotExampleBase):
    def __init__(self, parent_server: Server, hardware_interface: RobotInterface) -> None:
        self.interface = hardware_interface
        super().__init__(parent_server=parent_server)

    def get_BatteryState(self, *, metadata: MetadataDict) -> float:
        return random()

    def GoToHomePosition(self, *, metadata: MetadataDict) -> GoToHomePosition_Responses:
        print("Going home")
        self.interface.go_home()
        time.sleep(2)
        print("I'm home")
