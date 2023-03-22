from typing import Tuple
import numpy as np
import yaml
import time
from rtde_control import RTDEControlInterface as RTDEControl
from rtde_receive import RTDEReceiveInterface as RTDEReceive
from dashboard_client import DashboardClient
from labware import *

from UR_Arm_Abs import URRobotAbs

##useful poses

HOME_POSE = np.array([-0.4104577419847799, -0.2626529489715343, 0.2972660465054066, 
                        1.8552623321968715, 2.420037547531281, -0.014278932653435552])

SYR_DECAP_POSE = np.array([-0.4104577419847799, -0.2626529489715343, 0.2972660465054066, 
                        1.8552623321968715, 2.420037547531281, -0.014278932653435552])

PEN_DECAP_POSE = np.array([-0.4104577419847799, -0.2626529489715343, 0.2972660465054066, 
                        1.8552623321968715, 2.420037547531281, -0.014278932653435552])

## status

IDLE = 0
MOVING = 1
GRIPPING = 2
POURING = 3
DISCONNECTED = 4

class UR_Robot(URRobotAbs):
    def __init__(self, host: any, ) -> None:
        ##connection parameters
        self.TCP_IP = host

        self.home_pose = HOME_POSE
        self.status = DISCONNECTED
    
    def configure_robot_params(self, syr_samp: int, syr_batch: int, Lpen_samp: int,
                  Lpen_batch: int,Spen_samp: int, Spen_batch: int):
        self.LTray = LTray(syr_samp, syr_batch, Lpen_samp, Lpen_batch)
        self.STray = STray(Spen_samp, Spen_batch)
        self.OutTray = Out_tray(syr_batch, Lpen_samp, Lpen_batch)
        self.Lmat = self.LTray.create_matrix()
        self.Smat = self.STray.create_matrix()
        self.Outmat = self.OutTray.create_matrix()
        

    def connect(self):
        """connect to robot and initialize dashboard and receiver"""
        self.connection = RTDEControl(self.TCP_IP)
        self.receive = RTDEReceive(self.TCP_IP)
        self.dashboard = DashboardClient(hostname=self.TCP_IP)
        self.dashboard.connect()
        self.dashboard.powerOn()  
        self.dashboard.brakeRelease() 
        self.status = IDLE
        return self.connection.isConnected()
    
    def check_connection(self):
        return self.connection.isConnected()
    
    def robot_status(self):
        return self.status
    
    def check_AND_moveJ(self, pose: np.array, cartesian: bool = False):
        """ Check if pose if within safety limits and move in JointSpace. """
        # if cartesian:
        #     if self.rtde_c.isPoseWithinSafetyLimits(pose):
        #         pose = self.rtde_c.getInverseKinematics(pose)
        #     else:
        #         return False

        # if self.rtde_c.isJointsWithinSafetyLimits(pose):
        #     self.rtde_c.moveJ(pose, self.vel_q, self.acc_q)
        #     return True
        # else:
        #     return False
        print("movej to pose:",pose)

    def check_AND_moveL(self, pose: np.array, joint: bool = False):
        """ Check if pose if within safety limits and move in LinearSpace. """
        # if joint:
        #     if self.rtde_c.isJointsWithinSafetyLimits(pose):
        #         pose = self.rtde_c.getInverseKinematics(pose)
        #     else:
        #         return False 
           
        # if self.rtde_c.isPoseWithinSafetyLimits(pose):
        #     self.rtde_c.moveL(pose, self.vel_c, self.acc_c)
        #     return True
        # else:
        #     return False
        print("movel to pose:",pose)

    
    def go_home(self):
        """Move arm to home position"""
        self.check_AND_moveJ(self.home_pose, cartesian=True)

    def select_n_play(self, program: str):
        """laod and play program"""
        self.dashboard.loadURP(program)
        self.dashboard.play()
        print(f"[INFO]: Executing {program}. ")
        self.dashboard.stop()

    def grip_syringe(self):
        # program = "grip_syringe.urp"
        # self.select_n_play(program)
        print("gripping syringe")


    def grip_pen(self):
        # program = "grip_pen.urp"
        # self.select_n_play(program)   
        print("gripping pen")

    # def move_to_syr_index(self, row, col):
    #     pos = Ltray_poses[row,col]

    def move_to_decapper(self, object):
        if isinstance(object, Syringe):
            self.check_AND_moveJ(SYR_DECAP_POSE)
        else:
            self.check_AND_moveJ(PEN_DECAP_POSE)

    ##looping programs 

    def Ltray_loop(self):
        ##find actual values
        initial_target = np.array([1,1,0.2,0,0,0])
        targetJ = initial_target
        offset_moveL = np.array([0,-0.2,0,0,0,0])
        self.check_AND_moveJ(targetJ)
        for i in range(len(self.Lmat)):
            targetJ[0] = initial_target[0]
            targetJ[1] -= self.LTray.sep_y * i
            for j in range(len(self.Lmat[i])):
                if self.Lmat[i][j] is not None:
                    targetJ[0] += self.LTray.sep_x * j
                    self.check_AND_moveJ(targetJ)
                    self.check_AND_moveL(targetJ+offset_moveL)
                    self.grip_syringe() if isinstance(self.Lmat[i][j], Syringe) else self.grip_pen()
                else:
                    pass
                
    def Stray_loop(self):
        ##find actual values
        initial_target = np.array([0,1,0.2,0,0,0])
        targetJ = initial_target
        offset_moveL = np.array([0,-0.2,0,0,0,0])
        self.check_AND_moveJ(targetJ)
        for i in range(len(self.Lmat)):
            targetJ[0] = initial_target[0]
            targetJ[1] -= self.STray.sep_y * i
            for j in range(len(self.Smat[i])):
                if self.Smat[i][j] is not None:
                    targetJ[0] += self.STray.sep_x * j
                    self.check_AND_moveJ(targetJ)
                    self.check_AND_moveL(targetJ+offset_moveL)
                    self.grip_pen()
                else:
                    pass
        

test = UR_Robot("1", 2, 6, 2, 4, 3, 2, 2)
print(test.Lmat)
test.Ltray_loop()
print("starting stray")
test.Stray_loop()
