
import numpy as np 

HOME_POSE = np.array([-0.15285, -0.25362, 0.33395, 2.404, 2.420, -2.432])

SYR_DECAP_POSE = np.array([-0.14887, -0.37347, 0.2420+0.060-0.042, 0.176, -1.518, 0.108])

SYR_POUR_POSE = np.array([-0.36664, -0.0155, 0.3, 0.176, -1.518, 0.108])
SYR_POUR_POSE2 = np.array([-0.36664, -0.004, 0.22, 0.545, 4.711, -0.48])
POUR_ANGLE = [0.002, 0.0148, 0, 0.369, 6.22, -0.588]
# POUR_ANGLE = [0, 0.0151, 0, 0.369, 6.22, -0.588]
z_pour_syr= 0.222

PEN_REGRIP_POSE = np.array([-0.1908,-0.42013,0.16933,1.507,-0.561,-0.562])
PEN_DECAP_POSE = np.array([-0.2445, -0.37042, 0.21331, 2.377, 2.420, -2.382])

PEN_POUR_POSE = np.array([-0.36618,-0.09874,0.22-0.03,3.535,1.959,-1.934])
PEN_POUR_POSE2 = np.array([-0.40217,-0.06214,0.215,2.404,-0.76,-2.435])
PEN_POUR_POSE3 = np.array([-0.3639,-0.09756,0.22-0.03,0.892,-1.612,-1.616])
PEN_DISPOSE_POSE = np.array([-0.177,-0.345,0.134, 1.314, -1, -0.982])

offset_moveL = np.array([0,-0.01744,0,0,0,0])
offset_moveL_pen = np.array([0,0,-0.04,0,0,0])
initial_target_syringe = [-0.0378, -0.26686, 0.1587, 1.19, -1.212, 1.244]
initial_target_pen = [-0.0444, -0.25718,0.0991+0.03,0.007,-2.25,2.227]
## status