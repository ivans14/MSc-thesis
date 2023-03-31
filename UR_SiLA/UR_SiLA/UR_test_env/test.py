import time
import numpy as np
from UR_Arm import UR_Robot

Lmat = [[1, None, None, None, None, None], [None, None, None, None, None, None], 
        [None, None, None, None, None, None], [None, None, None, None, None, None], 
        [None, None, None, None, None, None], [None, None, None, None, None, None], 
        [None, None, None, None, None, None], [None, None, None, None, None, None],
          [None, None, None, None, None, None], [None, None, None, None, None, None], 
          [None, None, None, None, None, None], [None, None, None, None, None, None], 
          [None, None, None, None, None, None], [None, None, None, None, None, None], 
          [None, None, None, None, None, None]]

test = UR_Robot("192.168.0.30")
test.connect()
test.configure_robot_params(1,2,0,0,0,0)
# test.check_AND_moveL([-0.14811, -0.372, 0.2420+0.06, 0.176, -1.518, 0.108])
# test.check_AND_moveL([-0.14811-0.05, -0.372, 0.2420, 0.176, -1.518, 0.108])
# test.check_AND_moveL([-0.14811, -0.372, 0.2420, 0.176, -1.518, 0.108])
# test.check_AND_moveL([-0.14811, -0.38, 0.2420, 0.176, -1.518, 0.108])
# time.sleep(2)
# test.check_AND_moveL([-0.14811, -0.38, 0.2420+0.06, 0.176, -1.518, 0.108])
test.go_home()
test.Ltray_loop()