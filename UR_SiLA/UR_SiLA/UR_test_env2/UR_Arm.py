from typing import Tuple
import numpy as np
import yaml
import math
import time
from rtde_control import RTDEControlInterface as RTDEControl
from rtde_receive import RTDEReceiveInterface as RTDEReceive
from dashboard_client import DashboardClient
from labware import *
from Poses import *

from UR_Arm_Abs import URRobotAbs

##useful poses

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
        self.vel_c = 0.1
    
    def configure_robot_params(self, syr_samp: int, syr_batch: int, Lpen_samp: int,
                  Lpen_batch: int,Spen_samp: int, Spen_batch: int):
        if syr_samp < 0 or syr_samp > 6 or Lpen_samp <0 or Lpen_samp > 6:
            return False
        self.LTray = LTray(syr_samp, syr_batch, Lpen_samp, Lpen_batch)
        self.STray = STray(Spen_samp, Spen_batch)
        self.OutTray = Out_tray(syr_batch, Lpen_samp, Lpen_batch)
        self.Lmat = self.LTray.create_matrix()
        self.Smat = self.STray.create_matrix()
        self.Outmat = self.OutTray.create_matrix()
        print(self.Lmat)
        print(self.Smat)
        print(self.Outmat)
        return True
        

    def connect(self):
        """connect to robot and initialize dashboard and receiver"""
        self.connection = RTDEControl(self.TCP_IP)
        self.receive = RTDEReceive(self.TCP_IP)
        self.dashboard = DashboardClient(hostname=self.TCP_IP)
        self.dashboard.connect()
        self.dashboard.powerOn()  
        self.dashboard.brakeRelease() 
        self.status = IDLE
        return "connection succesfull" if self.connection.isConnected() else "connection failed"
    
    def check_connection(self):
        return self.connection.isConnected()
    
    def robot_status(self):
        return self.status
    
    def check_AND_moveJ(self, pose: np.array, cartesian: bool = True):
        """ Check if pose if within safety limits and move in JointSpace. """
        if cartesian:
            if self.connection.isPoseWithinSafetyLimits(pose):
                pose = self.connection.getInverseKinematics(pose)
            else:
                return False

        if self.connection.isJointsWithinSafetyLimits(pose):
            self.connection.moveJ(pose, 0.4)
            return True
        else:
            return False
        # print("movej to pose:",pose)

    def check_AND_moveL(self, pose: np.array, joint: bool = False, vel = 0.1):
        """ Check if pose if within safety limits and move in LinearSpace. """
        if joint:
            if self.connection.isJointsWithinSafetyLimits(pose):
                pose = self.connection.getInverseKinematics(pose)
            else:
                return False 
           
        if self.connection.isPoseWithinSafetyLimits(pose):
            print("moving", pose)
            self.connection.moveL(pose, vel)
            return True
        else:
            print("not safe")
            return False
        # print("movel to pose:",pose)


################## MOVING FUNCTIONS #########################################

    
    def go_home(self):
        """Move arm to home position"""
        self.check_AND_moveL(self.home_pose)

    ## PENDANT-BASED

    def select_n_play(self, program: str, execution_time: int):
        """laod and play program"""
        self.dashboard.loadURP(program)
        try:
            self.dashboard.play()
        except:
            print("error:trying again")
            time.sleep(1)
            self.dashboard.play()
        print(f"[INFO]: Executing {program}. ")
        time.sleep(execution_time)
        self.dashboard.stop()
        self.connection.reuploadScript()
        time.sleep(0.2)

    def grip_syringe(self, current_pos):
        print("gripping syringe")
        offset_z = [0,0,0.15,0,0,0]
        self.check_AND_moveL(current_pos+offset_z)

    def pour_syringe(self):
        program = "pour_syringe.urp"
        print("pouring syringe")
        self.select_n_play(program,10)   
        print("pouring syringe")

    def grip_pen(self, current_pos, time):
        program = "grip_pen.urp"
        self.select_n_play(program,time)   
        print("gripping pen")
        offset_z = [0,0,0.15,0,0,0]
        self.check_AND_moveL(current_pos+offset_z)
    
    def release_pen(self):
        program = "release_pen.urp"
        self.select_n_play(program,3) 


    def open_fingers(self):
        program = "open_fingers.urp"
        self.select_n_play(program,5) 
    
    def closed_fingers(self):
        program = "closed_fingers.urp"
        self.select_n_play(program,5) 

    ## DECAPPING

    def move_to_decapper(self, object):
        """move to decapper (for both syringes and pens)"""
        if isinstance(object, Syringe):
            self.check_AND_moveL(SYR_DECAP_POSE)
        else:
            self.check_AND_moveL(PEN_DECAP_POSE)

    def regrip_pen(self):
        self.check_AND_moveL(PEN_REGRIP_POSE,vel=0.07)
        move_down = [0,0,-0.02,0,0,0]
        self.check_AND_moveL(PEN_REGRIP_POSE+move_down,vel=0.07)
        self.release_pen()
        move_down[2] -= 0.035
        self.check_AND_moveL(PEN_REGRIP_POSE+move_down)
        current_pose = PEN_REGRIP_POSE+move_down
        self.grip_pen(current_pose,2)
        self.check_AND_moveL(PEN_REGRIP_POSE)

    def decap_syr(self):
        """decap syringe movement"""
        # find actual values
        current_pose = SYR_DECAP_POSE.copy()
        move_down = [-0.05,0,-0.0564,0,0,0]
        move_back = [0.048,0,0,0,0,0]
        move_right = [0,-0.008,0,0,0,0]
        self.check_AND_moveL(current_pose+move_down)
        current_pose += move_down
        print(current_pose)
        self.connection.moveL(current_pose+move_back,0.04)
        current_pose += move_back
        self.check_AND_moveL(current_pose+move_right)
        self.check_AND_moveL(SYR_DECAP_POSE + move_right)

    def decap_pen(self):
        current_pose = PEN_DECAP_POSE.copy()
        move_down = [0,0,-0.055,0,0,0]
        self.check_AND_moveL(current_pose+move_down)
        current_pose += move_down
        move_out = [0,0.1,0,0,0,0]
        self.check_AND_moveL(current_pose+move_out)
        current_pose += move_out
        move_up = [0,0,0.1,0,0,0]
        self.check_AND_moveL(current_pose+move_up)

    ## OUTPUT
    
    def move_to_output_syr(self, i):
        self.check_AND_moveL(SYR_POUR_POSE)
        row, column = divmod(i//3, 3)
        new_pos = SYR_POUR_POSE.copy() + [column*self.OutTray.sep_col, 
                                   row*self.OutTray.sep_row,0,0,0,0]
        self.check_AND_moveL(new_pos)
        new_pos += [0,0,-0.08,0,0,0]
        self.check_AND_moveL(new_pos)
        self.check_AND_moveL(new_pos + POUR_ANGLE)
    
    def move_to_output_pen(self, i):
        self.check_AND_moveL(PEN_POUR_POSE)
        row, column = divmod(i//3, 3)
        curr_pos = PEN_POUR_POSE.copy() + [column*self.OutTray.sep_col, 
                                   row*self.OutTray.sep_row,0,0,0,0]
        self.check_AND_moveL(curr_pos, vel=0.075)
        curr_pos += [0,0,-0.05,0,0,0]
        self.check_AND_moveL(curr_pos)
        self.release_pen()
        curr_pos += [0,0,0.08,0,0,0]
        self.check_AND_moveL(curr_pos)
        self.turn_wrist(90, curr_pos)
        self.closed_fingers()
        curr_pos = PEN_POUR_POSE2.copy() + [column*self.OutTray.sep_col, 
                                   row*self.OutTray.sep_row,0,0,0,0]
        self.check_AND_moveL(curr_pos+[0,0,0.05,0,0,0])
        self.check_AND_moveL(curr_pos)
        self.open_fingers()
        self.check_AND_moveL(curr_pos+[0,0,0.08,0,0,0])
        self.turn_wrist(90, curr_pos+[0,0,0.08,0,0,0])
        curr_pos = PEN_POUR_POSE3.copy() + [column*self.OutTray.sep_col, 
                                   row*self.OutTray.sep_row,0,0,0,0]
        self.check_AND_moveL(curr_pos)
        curr_pos += [0,0,-0.05,0,0,0]
        self.check_AND_moveL(curr_pos)
        self.grip_pen(curr_pos,9)
        self.check_AND_moveL(PEN_DISPOSE_POSE)
        self.release_pen()
    
    def dispose_syringe(self):
        self.check_AND_moveL(SYR_DECAP_POSE)
        current_pose = SYR_DECAP_POSE.copy()
        move_down = [-0.05,0,-0.09,0,0,0]
        move_right = [0,-0.01,0,0,0,0]
        move_back = [0.075,0,0,0,0,0]
        self.check_AND_moveL(current_pose+move_down)
        current_pose += move_down
        self.check_AND_moveL(current_pose+move_right)
        current_pose += move_right
        self.check_AND_moveL(current_pose+move_back)
        self.check_AND_moveL(SYR_DECAP_POSE + move_back)


    ##looping programs 
    def turn_wrist(self, deg: float, pos: list):
        """turn wrist for when the first pen appears"""
        turn = math.radians(deg)
        print("aaaa")
        curr = self.connection.getInverseKinematics(pos)
        curr[-1] += turn
        self.connection.moveJ(curr)
        time.sleep(0.5)
        return self.receive.getActualTCPPose()



    def syringe_loop(self, target_row:list, target_col: list, i: int ,j: int):
        # self.open_fingers()
        # self.check_AND_moveJ(target_row)
        # print(target_col)
        # self.check_AND_moveL(target_col+offset_moveL)
        # current_pos = target_col+offset_moveL
        # self.grip_syringe(current_pos) 
        self.move_to_decapper(self.Lmat[i][j])
        self.decap_syr()
        # self.move_to_output_syr(i)
        # self.pour_syringe()
        # self.check_AND_moveL(SYR_POUR_POSE)
        # self.open_fingers()
        # self.dispose_syringe()
        # self.go_home()

    def pen_loop(self, target_row:list, target_col: list, i: int ,j: int):
        self.closed_fingers()
        self.release_pen()
        # self.turn_wrist(180,HOME_POSE)
        self.check_AND_moveJ(target_row)
        self.check_AND_moveL(target_col)
        self.check_AND_moveL(target_col+offset_moveL_pen)
        current_pos = target_col+offset_moveL_pen
        # self.grip_pen(current_pos,2)
        # self.regrip_pen()
        # # # # self.move_to_decapper(self.Lmat[i][j])
        # # # # self.decap_pen()
        # self.turn_wrist(-180,PEN_REGRIP_POSE)
        # self.move_to_output_pen(i)


    def Ltray_loop(self):
        ##find actual values
        for i in range(len(self.Lmat)):
            for j in range(len(self.Lmat[i])):
                target_row = initial_target_syringe.copy() if isinstance(self.Lmat[i][j],Syringe) else initial_target_pen.copy()
                target_row[1] -= self.LTray.sep_y * i
                target_col = target_row.copy()
                time.sleep(0.1)
                if self.Lmat[i][j] is not None:
                    target_col[0] -= self.LTray.sep_x * j
                    if isinstance(self.Lmat[i][j], Syringe):
                        self.syringe_loop(target_row, target_col, i, j)
                    else:
                        self.pen_loop(target_row, target_col, i, j)
                    time.sleep(1)
                else:
                    pass
        return True
                
    def Stray_loop(self):
        ##find actual values
        initial_target = np.array([0,1,0.2,0,0,0])
        targetJ = initial_target
        offset_moveL = np.array([0,-0.2,0,0,0,0])
        self.check_AND_moveJ(targetJ)
        for i in range(len(self.Smat)):
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
        

# test = UR_Robot("1", 2, 6, 2, 4, 3, 2, 2)
# print(test.Lmat)
# test.Ltray_loop()
# print("starting stray")
# test.Stray_loop()
