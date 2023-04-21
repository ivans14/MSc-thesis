import time
import numpy as np
from UR_Arm import UR_Robot, PEN_POUR_POSE, initial_target_pen, PEN_DECAP_POSE

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
test.configure_robot_params(0,0,1,1,0,0)
# PEN_POUR_POSE = np.array([-0.38417,-0.154,0.202,0.921,-1.679,-1.519])
# test.open_fingers()
test.go_home()
test.Ltray_loop()