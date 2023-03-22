import time
import numpy as np
from UR_Arm import UR_Robot

Lmat = [[1, 1, 1, None, None, None], [2, 2, None, None, None, None], 
        [None, None, None, None, None, None], [None, None, None, None, None, None], 
        [None, None, None, None, None, None], [None, None, None, None, None, None], 
        [None, None, None, None, None, None], [None, None, None, None, None, None],
          [None, None, None, None, None, None], [None, None, None, None, None, None], 
          [None, None, None, None, None, None], [None, None, None, None, None, None], 
          [None, None, None, None, None, None], [None, None, None, None, None, None], 
          [None, None, None, None, None, None]]

test = UR_Robot("192.168.0.30")
test.connect()
test.configure_robot_params(2,1,2,1,1,1)
test.go_home()
test.Ltray_loop()