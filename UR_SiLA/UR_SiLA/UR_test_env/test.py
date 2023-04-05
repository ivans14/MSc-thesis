import time
import numpy as np
from UR_Arm import UR_Robot, SYR_POUR_POSE

Lmat = [[1, None, None, None, None, None], [None, None, None, None, None, None], 
        [None, None, None, None, None, None], [
    None, None, None, None, None, None], 
        [None, None, None, None, None, None], [None, None, None, None, None, None], 
        [None, None, None, None, None, None], [None, None, None, None, None, None],
          [None, None, None, None, None, None], [None, None, None, None, None, None], 
          [None, None, None, None, None, None], [None, None, None, None, None, None], 
          [None, None, None, None, None, None], [None, None, None, None, None, None], 
          [None, None, None, None, None, None]]

test = UR_Robot("192.168.0.30")
test.connect()
test.configure_robot_params(2,1,0,0,0,0)
test.go_home()
# test.reset_fingers()
test.Ltray_loop()