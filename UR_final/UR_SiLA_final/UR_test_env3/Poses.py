import numpy as np 

HOME_POSE = np.array([-0.15285, -0.25362, 0.33395, 2.404, 2.420, -2.432])

SYR_DECAP_POSE = np.array([-0.20919,-0.2706,0.21823,0.653,2.423,-2.5])
SYR_REGRIP_POSE = np.array([-0.21346,-0.2964,0.1872-0.01285,1.673,0.877,-1.617])
SYR_DISPOSE_POSE = np.array([-0.20319,-0.37862,0.17385+0.07,2.147,0,-2.272])

SYR_POUR_POSE2 = np.array([-0.32458, -0.09941, 0.25+0.08-0.02515, 2.069, -0.23,-2.147])

PEN_REGRIP_POSE = np.array([-0.246,-0.3991,0.1398+0.05+0.03,0.307,2.363,-2.319])
PEN_DECAP_POSE = np.array([-0.27913, -0.37877, 0.2337-0.044, 2.346, 2.519, -2.359])
PEN_REGRIP_DECAP = np.array([-0.2226,-0.45367,0.25324,1.515,-0.565,-0.558])
PEN_REGRIP_DECAP2 = np.array([-0.228,-0.45495,0.25324,1.515,-0.565,-0.558])

PEN_POUR_POSE = np.array([-0.32916,-0.03357-0.16856+0.00958,0.1648+0.05,3.535,1.959,-1.934])
PEN_POUR_POSE2 = np.array([-0.363,-0.17,0.2364+0.03,1.229,4.285,1.257])
PEN_POUR_POSE3 = np.array([-0.3639,-0.09756,0.22-0.03,0.892,-1.612,-1.616])
PEN_DISPOSE_POSE = np.array([-0.185,-0.345,0.134, 1.87,2.503,-2.525])

offset_moveL = np.array([0,0,-0.08,0,0,0])
initial_target_pen = np.array([-0.15462,-0.2658,0.09165-offset_moveL[2],0.007,-2.25,2.227])
initial_target_pen2 = np.array([-0.1562,-0.3055,0.24171,1.593,0.017,0.027])
initial_target_syringe = initial_target_pen.copy()
initial_target_syringe[2] = 0.1092-offset_moveL[2]
## status

VEL = 3