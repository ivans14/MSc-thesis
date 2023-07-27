import numpy as np 

HOME_POSE = np.array([-0.15285, -0.25362, 0.33395, 2.404, 2.420, -2.432])

SYR_DECAP_POSE = np.array([-0.20697,-0.2745,0.21823,0.6,2.49,-2.46])
SYR_REGRIP_POSE = np.array([-0.21346,-0.2964,0.1872,1.673,0.877,-1.617])
SYR_DISPOSE_POSE = np.array([-0.20319,-0.37862,0.17385+0.07,2.147,0,-2.272])

SYR_POUR_POSE = np.array([-0.37073, 0.0649, 0.25+0.08, 2.069, -0.23,-2.147])

PEN_REGRIP_POSE = np.array([-0.19557,-0.42545,0.1398+0.05,0.937,2.51,-2.463])
PEN_DECAP_POSE = np.array([-0.2803, -0.37882, 0.2337-0.05, 2.346, 2.519, -2.359])

PEN_POUR_POSE = np.array([-0.375,-0.03357,0.1648+0.05,3.535,1.959,-1.934])
PEN_POUR_POSE2 = np.array([-0.40475,0.00046,0.2364+0.03,1.229,4.285,1.257])
PEN_POUR_POSE3 = np.array([-0.3639,-0.09756,0.22-0.03,0.892,-1.612,-1.616])
PEN_DISPOSE_POSE = np.array([-0.185,-0.345,0.134, 1.87,2.503,-2.525])

offset_moveL = np.array([0,0,-0.06,0,0,0])
initial_target_pen = np.array([-0.13313,-0.26955,0.09612-offset_moveL[2],0.007,-2.25,2.227])
initial_target_syringe = initial_target_pen.copy()
initial_target_syringe[2] = 0.1245-offset_moveL[2]
## status