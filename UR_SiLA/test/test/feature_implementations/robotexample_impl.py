# Generated by sila2.code_generator; sila2.__version__: 0.10.1
from __future__ import annotations

from typing import TYPE_CHECKING

from sila2.server import MetadataDict

from ..generated.robotexample import GoToHomePosition_Responses, RobotExampleBase

if TYPE_CHECKING:
    from ..server import Server


class RobotExampleImpl(RobotExampleBase):
    def __init__(self, parent_server: Server) -> None:
        super().__init__(parent_server=parent_server)

    def get_BatteryState(self, *, metadata: MetadataDict) -> float:
        raise NotImplementedError  # TODO

    def GoToHomePosition(self, *, metadata: MetadataDict) -> GoToHomePosition_Responses:
        print("a")
        self.parent_server.robot_interface.move()
