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

initial_target_syringe = [-0.0378, -0.26686, 0.1587, 1.19, -1.212, 1.244]
PEN_POUR_POSE = np.array([-0.3638,-0.09661,0.22-0.03,0.843,-1.622,-1.579])
HOME_POSE = np.array([-0.15285, -0.25362, 0.33395, 2.404, 2.420, -2.432])
initial_target_pen = [-0.04657, -0.25915,0.0991,1.5295,0.013,0.061]
test = UR_Robot("192.168.0.30")
test.connect()
test.configure_robot_params(0,0,1,1,0,0)
# test.go_home()
# test.turn_wrist(180,[-0.15285, -0.25362, 0.33395, 2.404, 2.420, -2.432])
# test.check_AND_moveL(PEN_POUR_POSE)
# test.check_AND_moveL(initial_target_pen)
# PEN_POUR_POSE = np.array([-0.38417,-0.154,0.202,0.921,-1.679,-1.519])
# test.open_fingers()
test.go_home()
test.Ltray_loop()