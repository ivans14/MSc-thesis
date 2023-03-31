# Generated by sila2.code_generator; sila2.__version__: 0.10.1

from typing import Optional, Any
from uuid import UUID

from sila2.server import SilaServer

from .feature_implementations.connectioncontroller_impl import ConnectionControllerImpl
from .feature_implementations.robotexample_impl import RobotExampleImpl
from .generated.connectioncontroller import ConnectionControllerFeature
from .generated.robotexample import RobotExampleFeature

# import hardware interface class
from .UR_Arm import UR_Robot

class Server(SilaServer):
    def __init__(self, server_uuid: Optional[UUID] = None):
        # TODO: fill in your server information
        super().__init__(
            server_name="UR_Robot",
            server_type="Device",
            server_version="0.1",
            server_description="Implementation of UR Robot Arm",
            server_vendor_url="https://gitlab.com/SiLA2/sila_python",
            server_uuid=server_uuid,
        )

        host : Any = "192.168.0.30"
        port : int = 30004
        self.robot_interface = UR_Robot(host = host, port = port)
        
        self.connectioncontroller = ConnectionControllerImpl(self)
        self.set_feature_implementation(ConnectionControllerFeature, self.connectioncontroller)

        self.robotexample = RobotExampleImpl(self)
        self.set_feature_implementation(RobotExampleFeature, self.robotexample)