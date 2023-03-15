from typing import Tuple
import numpy as np
import yaml
import time
from rtde_control import RTDEControlInterface as RTDEControl
from rtde_receive import RTDEReceiveInterface as RTDEReceive
from dashboard_client import DashboardClient

from UR_Arm_Abs import URRobotAbs

class UR_Robot(URRobotAbs):
    def __init__(self) -> None:
        