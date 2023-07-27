from typing import Tuple
import numpy as np
import math
import time
from rtde_control import RTDEControlInterface as RTDEControl
from rtde_receive import RTDEReceiveInterface as RTDEReceive
from dashboard_client import DashboardClient
from rtde_io import RTDEIOInterface as RTDEIO
from labware import *
from Poses import *
from UR_Arm_Abs import URRobotAbs
# from .labware import *
# from .Poses import *
# from .UR_Arm_Abs import URRobotAbs
from datetime import datetime
import threading
from new_row import write_time

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
        self.current = "syr"
        self.connect()
    
    def configure_robot_params(self, syr_samp: int, syr_batch: int, Lpen_samp: int,
                  Lpen_batch: int,Spen_samp: int, Spen_batch: int):
        """IVSN: 19/05/23 Configure the parameters (number of batches and samples of each vial) for 
        the program, returning a boolean determining the validity of those parameters"""
        if syr_samp < 0 or syr_samp > 6 or Lpen_samp <0 or Lpen_samp > 6:
            return False
        self.Tray = Tray(syr_samp, syr_batch, Lpen_samp,
                  Lpen_batch,Spen_samp, Spen_batch)
        self.OutTray = Out_tray(syr_batch, Lpen_batch,Spen_batch)
        self.Lmat = self.Tray.create_matrix(False)
        self.Outmat = self.OutTray.create_matrix()
        print(self.Lmat)
        print(self.Outmat)
        return True
    
    def configure_decapping(self, LPen, SPen):
        if LPen + SPen > 12*13:
            return False
        self.Tray = Tray(0, 0, LPen, 0, SPen, 0)
        self.Lmat = self.Tray.create_matrix(True)
        print(self.Lmat)
        return True

        

    def connect(self):
        """IVSN: 19/05/23 Connect to robot and initialize dashboard and receiver"""
        # RTDEControl(self.TCP_IP).disconnect()
        # print(RTDEControl(self.TCP_IP).isConnected())

        self.connection = RTDEControl(self.TCP_IP)
        self.receive = RTDEReceive(self.TCP_IP)
        self.IO = RTDEIO(self.TCP_IP)
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
        """IVSN: 19/05/23 Check if pose if within safety limits and move in JointSpace. """
        if cartesian:
            if self.connection.isPoseWithinSafetyLimits(pose):
                pose = self.connection.getInverseKinematics(pose)
            else:
                return False

        if self.connection.isJointsWithinSafetyLimits(pose):
            self.connection.moveJ(pose, 3.14)
            return True
        else:
            return False
        # print("movej to pose:",pose)

    def check_AND_moveL(self, pose: np.array, joint: bool = False, vel = VEL):
        """IVSN: 19/05/23 Check if pose if within safety limits and move in LinearSpace. """
        if joint:
            if self.connection.isJointsWithinSafetyLimits(pose):
                pose = self.connection.getInverseKinematics(pose)
            else:
                return False 
           
        if self.connection.isPoseWithinSafetyLimits(pose):
            self.connection.moveL(pose, vel)
            return True
        else:
            print("not safe")
            return False
        # print("movel to pose:",pose)


############### FESTO #########################3
    def prepare_for_input_festo(self):
        print("prepare for input Festo")
        self.IO.setStandardDigitalOut(6,False)
        self.IO.setStandardDigitalOut(5,True)

    def prepare_for_output_festo(self):
        print("prepare for output Festo")
        self.IO.setStandardDigitalOut(5,False)
        self.IO.setStandardDigitalOut(6,True)
        # elif not self.receive.getDigitalOutputState(2) and InternalPosition == 1:
        #     self.IO.setStandardDigitalOut(2,True)


################## MOVING FUNCTIONS #########################################

    
    def go_home(self):
        """IVSN: 19/05/23 Move arm to home position"""
        self.check_AND_moveL(self.home_pose)

    def logic_row_col(self,i,j,only_decap):
        target_row = initial_target_syringe.copy() if isinstance(self.Lmat[i][j],Syringe) else initial_target_pen.copy()
        if only_decap and i>1:
            target_row = initial_target_pen2.copy()
            # curr = self.receive.getActualTCPPose()
            # self.turn_wrist(180,curr)
        if i % 2 == 1:
            target_row[0] += self.Tray.sep_x_double
        target_row[1] -= self.Tray.sep_y * (i//2)
        target_col = target_row.copy()
        time.sleep(0.1)
        target_col[0] += self.Tray.sep_x * j
        return target_row, target_col
    ## PENDANT-BASED

    def curr_syr(self,only_decap):
        if self.current == "syr":
            self.closed_fingers()
            self.release_pen()
        self.current = "Lpen"
        if not only_decap:
            threading.Thread(target = self.prepare_for_input_festo).start()


    def select_n_play(self, program: str, execution_time: int):
        """IVSN: 19/05/23 Laod and play program. 
        Args:
            program: .urp program to execute
            execution_time: Determines how long the main program 
            should wait for the execution, intending to save time
            """
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


    def pour_syringe(self,pour_pose):
        """IVSN: 19/05/23 Program to pour a PFS"""
        program = "pour_syringe.urp"
        print("pouring syringe")
        self.select_n_play(program,7)   
        print("pouring syringe")
        self.check_AND_moveL(pour_pose)
        self.open_fingers()

    def grip_pen(self, offset, current_pos, time):
        """IVSN: 19/05/23 Grip a Penfill cartridge
            Args:
                current_pos: 6-D array of robot's position
                time: execution time. Will be used for select_n_play function"""
        program = "grip_pen.urp"
        self.select_n_play(program,time)   
        print("gripping pen")
        offset_z = [0,0,offset,0,0,0]
        self.check_AND_moveL(current_pos+offset_z)
        return current_pos+offset_z
    
    def release_pen(self):
        """IVSN: 19/05/23 Release a pen"""
        program = "release_pen.urp"
        self.select_n_play(program,3) 

    def grip_syr(self, current_pos, time):
        """IVSN: 19/05/23 Grip a PFS
            Args:
                current_pos: 6-D array of robot's position
                time: execution time. Will be used for select_n_play function"""
        program = "grip_syr.urp"
        self.select_n_play(program,time)   
        print("gripping syr")
        offset_z = [0,0,0.15,0,0,0]
        self.check_AND_moveL(current_pos+offset_z)
    
    def release_syr(self):
        """IVSN: 19/05/23 Release a PFS"""
        program = "release_syr.urp"
        self.select_n_play(program,3) 

    def fix_syr(self):
        """IVSN: 19/05/23 fix a PFS"""
        program = "fix_syr.urp"
        self.select_n_play(program,5) 

    def unfix_syr(self):
        """IVSN: 19/05/23 unfix a PFS"""
        program = "unfix_syr.urp"
        self.select_n_play(program,3) 

    def open_fingers(self):
        """IVSN: 19/05/23 Open gripper's fingers"""
        program = "open_fingers.urp"
        self.select_n_play(program,5) 
    
    def closed_fingers(self):
        """IVSN: 19/05/23 Close gripper's fingers"""
        program = "closed_fingers.urp"
        self.select_n_play(program,5) 

    def turn_wrist(self, deg: float, pos: list):
        """IVSN: 19/05/23 Turn wrist function. Gets joint position and moves the last 
        joint according to arguments
        Args: 
            deg: number of degrees to turn
            pos: current position of the robot arm"""
        turn = math.radians(deg)
        curr = self.connection.getInverseKinematics(pos)
        curr[-1] += turn
        self.connection.moveJ(curr, 2)
        time.sleep(0.5)
        return self.receive.getActualTCPPose()

    ## GET LABWARE

    def get_labware(self,target_row,target_col,large=False,only_decap=False, i=0):
        if only_decap and i>1:
            if large:
                z = 0.15
            else:
                z = 0.13
            target_col_down = target_col.copy()
            target_col_down[2] = z
            # self.check_AND_moveJ(target_row)
            self.check_AND_moveL(target_col)
            self.check_AND_moveL(target_col_down)
            return target_col_down
        if not only_decap:
            self.check_AND_moveJ(target_row)
        self.check_AND_moveL(target_col)
        self.check_AND_moveL(target_col+offset_moveL)
        return target_col+offset_moveL

    ## DECAPPING

    def move_to_decapper(self, object):
        """IVSN: 19/05/23 move to decapper (for both syringes and pens)
        Args:
            object: Instance of object to be de-capped"""
        if isinstance(object, Syringe):
            self.check_AND_moveL(SYR_DECAP_POSE)
        else:
            self.check_AND_moveL(PEN_DECAP_POSE)
        threading.Thread(target=self.decapper_open).start()

    def regrip_pen(self,only_decap,large):
        """IVSN: 19/05/23 Regrip a Penfill cartridge to turn it upside down and place on output tray"""
        self.check_AND_moveL(PEN_REGRIP_POSE)
        move_down = [0,0,-0.04,0,0,0]
        move_down2 = [0,0,-0.0295,0,0,0]
        self.check_AND_moveL(PEN_REGRIP_POSE+move_down)
        self.release_syr()
        move_down[2] -= 0.035
        current_pose = PEN_REGRIP_POSE - move_down
        self.check_AND_moveL(current_pose)
        current_pose = self.turn_wrist(180,current_pose)
        if only_decap:
            self.check_AND_moveL(PEN_REGRIP_DECAP)
            if large:
                self.check_AND_moveL(PEN_REGRIP_DECAP+move_down2)
                current_pose = PEN_REGRIP_DECAP+move_down2
            else:
                current_pose = PEN_REGRIP_DECAP.copy()
                current_pose[2] = 0.2061
                self.check_AND_moveL(current_pose)
            current_pose = self.grip_pen(0.025,np.array(current_pose),3)
            return True
        current_pose_turned = current_pose
        current_pose_turned[2] = 0.093+0.03
        self.check_AND_moveL(current_pose_turned)
        current_pose = self.grip_pen(0.1,np.array(current_pose_turned),4)
        self.turn_wrist(-180,current_pose)

    def regrip_pen_inverse(self,large):
        """IVSN: 19/05/23 Regrip a Penfill cartridge to turn it upside down and place on output tray"""
        self.check_AND_moveL(PEN_REGRIP_DECAP)
        if not large:
            move_down = [0,0,-0.04,0,0,0]
            self.check_AND_moveL(PEN_REGRIP_DECAP+move_down)
        else:
            move_down = [0,0,-0.025,0,0,0]
            self.check_AND_moveL(PEN_REGRIP_DECAP+move_down)
        self.release_syr()
        self.check_AND_moveL(PEN_REGRIP_DECAP)
        current_pose = self.turn_wrist(-180,PEN_REGRIP_DECAP)
        self.check_AND_moveL(PEN_REGRIP_POSE)
        current_pose = PEN_REGRIP_POSE.copy()
        current_pose[2]=0.1663
        self.check_AND_moveL(current_pose)
        self.grip_pen(0.04,current_pose,3.25)


    def decap_syr(self):
        """IVSN: 19/05/23 Decap syringe movement"""
        # find actual values
        current_pose = SYR_DECAP_POSE.copy()
        move_down = [0,0,-0.1,0,0,0]
        move_up = [0,0,0.025,0,0,0]
        self.check_AND_moveL(current_pose+move_down,vel=0.05)
        current_pose += move_down
        time.sleep(0.2)
        self.check_AND_moveL(current_pose+move_up)
        self.unfix_syr()
        self.check_AND_moveL(SYR_DECAP_POSE)
        current_pose = self.turn_wrist(90,SYR_DECAP_POSE)
        current_pose[2] = SYR_REGRIP_POSE[2]
        self.check_AND_moveL(current_pose)
        self.check_AND_moveL(SYR_REGRIP_POSE,vel=0.05)
        self.check_AND_moveL(SYR_REGRIP_POSE+[i*3 for i in move_up])
        self.fix_syr()


    def turn_off_decapper(self):
        """IVSN: 19/05/23 Turns off de-capper's actuator, avoiding burnout"""
        self.IO.setStandardDigitalOut(0,True)
        time.sleep(2.5)
        self.IO.setStandardDigitalOut(1,True)
        time.sleep(0.1)

    def decapper_open(self):
        """IVSN: 19/05/23 Turns off de-capper's actuator, avoiding burnout"""
        self.IO.setStandardDigitalOut(1,False)
        self.IO.setStandardDigitalOut(0,True)

    def reset_decapper(self):
        self.IO.setStandardDigitalOut(1,False)
        time.sleep(0.1)
        self.IO.setStandardDigitalOut(0,False)
        time.sleep(2.5)
        self.IO.setStandardDigitalOut(0,True)
        time.sleep(2.5)
        self.IO.setStandardDigitalOut(1,True)
        time.sleep(0.1)
    
    def decap_pen(self, large:bool):
        """IVSN: 19/05/23 Decaps Penfill cartridge by using the actuator via Digital I/O"""
        current_pose = PEN_DECAP_POSE.copy()
        if large:
            z = 0.222
            current_pose[2] = z
            self.check_AND_moveL(current_pose)
        else:
            z = 0.2457
            current_pose[2] = z
            self.check_AND_moveL(current_pose)
        self.IO.setStandardDigitalOut(0,False)
        time.sleep(2)
        self.check_AND_moveL(PEN_DECAP_POSE)
        # avoid waiting for de-capper to turn off,move simultaneously
        threading.Thread(target = self.turn_off_decapper).start()

    ## OUTPUT
    
    def move_to_output_syr(self, i):
        """IVSN: 19/05/23 Pouring PFS into corresponding vial
        Args:
            i: batch number"""
        self.check_AND_moveL(SYR_POUR_POSE2)
        # calculation for the position of the corresponding output vial
        row, column = divmod(i, 3)
        new_pos = SYR_POUR_POSE2.copy() + [-column*self.OutTray.sep_col, 
                                    row*self.OutTray.sep_row,0,0,0,0]
        self.check_AND_moveL(new_pos)
        new_pos += [0,0,-0.08,0,0,0]
        self.check_AND_moveL(new_pos)
        return new_pos

    
    def move_to_output_pen(self, i):
        """IVSN: 19/05/23 Pouring Penfill cartridge into corresponding vial
        Args:
            i: batch number"""
        self.check_AND_moveL(PEN_POUR_POSE)
        # calculation for the position of the corresponding output vial
        row, column = divmod(i, 3)
        pour_pos = PEN_POUR_POSE.copy() + [-column*self.OutTray.sep_col, 
        row*self.OutTray.sep_row,0,0,0,0]
        self.check_AND_moveL(pour_pos)
        curr_pos = pour_pos.copy()
        curr_pos += [0,0,-0.05,0,0,0]
        self.check_AND_moveL(curr_pos)
        self.release_pen()
        self.pour_pen(curr_pos,row,column)
        return pour_pos
    
    def pour_pen(self,curr_pos,row,column):
        curr_pos += [0,0,0.08,0,0,0] 
        self.check_AND_moveL(curr_pos)
        curr_pos = self.turn_wrist(-90, curr_pos)
        # self.closed_fingers()
        curr_pos = PEN_POUR_POSE2.copy() + [-column*self.OutTray.sep_col, 
        row*self.OutTray.sep_row,0,0,0,0]
        self.check_AND_moveL(curr_pos+[0,0,0.05,0,0,0])
        self.check_AND_moveL(curr_pos-[0,0,0.07,0,0,0], vel= 0.05)
        time.sleep(0.5)
        # self.open_fingers()
        self.check_AND_moveL(curr_pos+[0,0,0.05,0,0,0])
        self.turn_wrist(90, curr_pos+[0,0,0.05,0,0,0])

    def dispose_pen(self, pour_pos):
        self.check_AND_moveL(pour_pos)
        curr_pos = pour_pos.copy()
        curr_pos += [0,0,-0.05,0,0,0]
        self.check_AND_moveL(curr_pos)
        self.grip_pen(0.15,curr_pos,3)
        self.check_AND_moveL(PEN_DISPOSE_POSE)
        self.release_pen()
    
    def move_to_input_pen(self, target_col, i, j, large,start_time):
            # self.check_AND_moveL(target_row)
            self.check_AND_moveL(target_col)
            if large:
                z = 0.15675
            else:
                z = 0.138
            if i < 2:
                z = 0.1          
            target_col_down = target_col.copy()
            target_col_down[2] = z
            self.check_AND_moveL(target_col_down)
            self.release_syr()
            write_time(int(large),i,j,start_time)
            self.check_AND_moveL(target_col)
            if (i==1 and j==5):
                self.turn_wrist(180,target_col)


    def dispose_syringe(self):
        """"IVSN: 19/05/23 Dispose of PFS by dropping it into built-in hole"""
        self.check_AND_moveL(SYR_DISPOSE_POSE)
        current_pose = SYR_DISPOSE_POSE.copy()
        move_down = [0,0,-0.07,0,0,0]
        move_back = [0.075,0,0,0,0,0]
        self.check_AND_moveL(current_pose+move_down)
        current_pose += move_down
        self.check_AND_moveL(current_pose+move_back,vel=0.1)
        self.check_AND_moveL(SYR_DISPOSE_POSE + move_back)


    ##looping programs 


    def syringe_loop(self, target_row:list, target_col: list, i: int ,j: int):
        """IVSN: 19/05/23 Looping function to process PFS
            Args:
                target_row: row position of the PFS in input tray
                target_col: column position of the PFS in input tray
                i: batch number
                j: sample number"""
        self.closed_fingers()
        self.release_syr()
        self.get_labware(target_row,target_col)
        start_time = datetime.now()
        self.grip_syr(target_col+offset_moveL,3)
        self.move_to_decapper(self.Lmat[i][j])
        self.decap_syr()
        pour_pose = self.move_to_output_syr(i)
        self.pour_syringe(pour_pose)
        self.dispose_syringe()
        write_time(2,i,j,start_time)

    def pen_loop(self, target_row:list, target_col: list, i: int ,j: int,large: bool, only_decap):
        """IVSN: 19/05/23 Looping function to process Penfills
            Args:
                target_row: row position of the Penfill in input tray
                target_col: column position of the Penfill in input tray
                i: batch number
                j: sample number"""
        current_pos = self.get_labware(target_row,target_col,large,only_decap,i)
        threading.Thread(target = self.reset_decapper).start()
        start_time = datetime.now()
        self.grip_pen(0.15,current_pos,3.5)
        if not only_decap:
            self.move_to_decapper(self.Lmat[i][j])
            self.decap_pen(large)
            self.regrip_pen(only_decap,large)
            pour_pos = self.move_to_output_pen(i)
            self.dispose_pen(pour_pos)
        else:
            if i>1:
                self.regrip_pen_inverse(large)
                self.move_to_decapper(self.Lmat[i][j])
                self.decap_pen(large)
                self.regrip_pen(only_decap,large)
                self.move_to_input_pen(target_col, i, j, large,start_time)
            else:
                self.move_to_decapper(self.Lmat[i][j])
                self.decap_pen(large)
                # self.regrip_pen(only_decap,large)
                self.move_to_input_pen(target_col, i, j, large,start_time)
            



    def tray_loop(self, only_decap):
        """IVSN: 19/05/23 Main function that calls the corresponding loop to process a single PFS or Penfill"""
        # if only_decap:
        for i in range(len(self.Lmat)):
            for j in range(len(self.Lmat[i])):
                if self.Lmat[i][j] is not None:
                    target_row, target_col = self.logic_row_col(i,j,only_decap)
                    if isinstance(self.Lmat[i][j], Syringe):
                        threading.Thread(target = self.prepare_for_output_festo).start()
                        self.syringe_loop(target_row, target_col, i, j)
                    elif isinstance(self.Lmat[i][j], LPen):
                        self.curr_syr(only_decap)
                        self.pen_loop(target_row, target_col, i, j,True, only_decap)
                    else:
                        self.curr_syr(only_decap)
                        self.pen_loop(target_row, target_col, i, j,False, only_decap)
                    time.sleep(1)
                else:
                    pass
        self.go_home()
        threading.Thread(target = self.prepare_for_output_festo).start()
        return True
                
    def run_program(self,SyrSamp, SyrBatch, LPenSamp, LPenBatch, SPenSamp, SPenBatch):
        """IVSN: 19/05/23 Runs the program according to parameters.
            Args:
                SyrSamp: number of samples for PFS
                SyrBatch: number of batches for PFS
                LPenSamp: number of samples for large Penfills
                LPenBatch: number of batches for large Penfills
                SPenSamp: number of samples for small Penfills
                SPenBatch: number of samples for small Penfills
                """
        # self.connect()
        response = self.configure_robot_params(SyrSamp, SyrBatch, LPenSamp, LPenBatch, SPenSamp, SPenBatch)
        if not response:
            return False
        self.go_home()
        self.tray_loop(only_decap = False)
        self.connection.disconnect()
        return True
    
    def run_decapping(self, LPen, Spen):
        # self.connect()
        response = self.configure_decapping(LPen, Spen)
        if not response:
            return False
        self.go_home()
        self.tray_loop(only_decap = True)
        # self.go_home()
        return True
