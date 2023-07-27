import time
import numpy as np
from UR_Arm import UR_Robot, PEN_POUR_POSE, initial_target_pen, PEN_DECAP_POSE
from Poses import *
from labware import *

test = UR_Robot("192.168.0.30")
# test.configure_decapping(156,0)
test.run_decapping(1,0)

# test.check_AND_moveL(PEN_DECAP_POSE)
# test.run_program(0,0,6,26,0,0)



