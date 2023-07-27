from typing import Tuple
import numpy as np
import math
import time
from rtde_control import RTDEControlInterface as RTDEControl
from rtde_receive import RTDEReceiveInterface as RTDEReceive
from dashboard_client import DashboardClient
from rtde_io import RTDEIOInterface as RTDEIO
from .labware import *
from .Poses import *
import threading

from .UR_Arm_Abs import URRobotAbs
from sila2.server import MetadataDict, ObservableCommandInstance
from queue import Queue

##useful poses

IDLE = 0
MOVING = 1
GRIPPING = 2
POURING = 3
DISCONNECTED = 4

class UR_Robot(URRobotAbs):
    def __init__(self, host: any, labware_transfer_Festo, labware_transfer_site_UR, labware_transfer_man_UR) \
    -> None:
        ##connection parameters
        self.TCP_IP = host
        self.FestoController = labware_transfer_Festo
        self.ManControllerUR = labware_transfer_man_UR
        self.SiteControllerUR = labware_transfer_site_UR
        self.home_pose = HOME_POSE
        self.status = DISCONNECTED
        self.vel_c = 0.1
    
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
            self.connection.moveJ(pose, 0.4)
            return True
        else:
            return False
        # print("movej to pose:",pose)

    def check_AND_moveL(self, pose: np.array, joint: bool = False, vel = 0.1):
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


################## MOVING FUNCTIONS #########################################

    
    def go_home(self):
        """IVSN: 19/05/23 Move arm to home position"""
        self.check_AND_moveL(self.home_pose)

    ## PENDANT-BASED

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


    def pour_syringe(self):
        """IVSN: 19/05/23 Program to pour a PFS"""
        program = "pour_syringe.urp"
        print("pouring syringe")
        self.select_n_play(program,10)   
        print("pouring syringe")

    def grip_pen(self, current_pos, time):
        """IVSN: 19/05/23 Grip a Penfill cartridge
            Args:
                current_pos: 6-D array of robot's position
                time: execution time. Will be used for select_n_play function"""
        program = "grip_pen.urp"
        self.select_n_play(program,time)   
        print("gripping pen")
        offset_z = [0,0,0.15,0,0,0]
        print("wtf")
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

    def open_fingers(self):
        """IVSN: 19/05/23 Open gripper's fingers"""
        program = "open_fingers.urp"
        self.select_n_play(program,5) 
    
    def closed_fingers(self):
        """IVSN: 19/05/23 Close gripper's fingers"""
        program = "closed_fingers.urp"
        self.select_n_play(program,5) 

    ## DECAPPING

    def move_to_decapper(self, object):
        """IVSN: 19/05/23 move to decapper (for both syringes and pens)
        Args:
            object: Instance of object to be de-capped"""
        if isinstance(object, Syringe):
            self.check_AND_moveL(SYR_DECAP_POSE)
        else:
            self.check_AND_moveL(PEN_DECAP_POSE)

    def regrip_pen(self):
        """IVSN: 19/05/23 Regrip a Penfill cartridge to turn it upside down and place on output tray"""
        self.check_AND_moveL(PEN_REGRIP_POSE,vel=0.07)
        move_down = [0,0,-0.04,0,0,0]
        self.check_AND_moveL(PEN_REGRIP_POSE+move_down,vel=0.07)
        self.release_pen()
        move_down[2] -= 0.035
        current_pose = PEN_REGRIP_POSE - move_down
        self.check_AND_moveL(current_pose)
        current_pose = self.turn_wrist(180,current_pose)
        current_pose_turned = current_pose
        current_pose_turned[2] = 0.093
        self.check_AND_moveL(current_pose_turned)
        current_pose = self.grip_pen(np.array(current_pose_turned),3)
        self.turn_wrist(-180,current_pose)

    def decap_syr(self):
        """IVSN: 19/05/23 Decap syringe movement"""
        # find actual values
        current_pose = SYR_DECAP_POSE.copy()
        move_down = [0,0,-0.1,0,0,0]
        move_up = [0,0,0.025,0,0,0]
        self.check_AND_moveL(current_pose+move_down)
        current_pose += move_down
        time.sleep(0.2)
        self.check_AND_moveL(current_pose+move_up)
        self.open_fingers()
        self.check_AND_moveL(SYR_DECAP_POSE)
        current_pose = self.turn_wrist(90,SYR_DECAP_POSE)
        current_pose[2] = SYR_REGRIP_POSE[2]
        self.check_AND_moveL(current_pose)
        self.check_AND_moveL(SYR_REGRIP_POSE)
        self.check_AND_moveL(SYR_REGRIP_POSE+[i*3 for i in move_up])


    def turn_off_decapper(self):
        """IVSN: 19/05/23 Turns of de-capper's actuator, avoiding burnout"""
        self.IO.setStandardDigitalOut(0,True)
        time.sleep(2.5)
        self.IO.setStandardDigitalOut(1,True)
        time.sleep(0.1)

    def decap_pen(self, large:bool):
        """IVSN: 19/05/23 Decaps Penfill cartridge by using the actuator via Digital I/O"""
        current_pose = PEN_DECAP_POSE.copy()
        self.IO.setStandardDigitalOut(1,False)
        self.IO.setStandardDigitalOut(0,True)
        time.sleep(2.5)
        move_up = [0,0,0.05,0,0,0]
        move_up_small = [0,0,0.05,0,0,0]
        if large:
            self.check_AND_moveL(current_pose+move_up)
        else:
            print("small")
        #     self.check_AND_moveL(current_pose+move_up_small)
        # self.IO.setStandardDigitalOut(0,False)
        # time.sleep(2.5)
        # self.check_AND_moveL(PEN_DECAP_POSE)
        # # avoid waiting for de-capper to turn off,move simultaneously
        # threading.Thread(target = self.turn_off_decapper).start()

    ## OUTPUT
    
    def move_to_output_syr(self, i):
        """IVSN: 19/05/23 Pouring PFS into corresponding vial
        Args:
            i: batch number"""
        self.check_AND_moveL(SYR_POUR_POSE)
        # calculation for the position of the corresponding output vial
        row, column = divmod(i, 3)
        new_pos = SYR_POUR_POSE.copy() + [row*self.OutTray.sep_row, 
                                   column*self.OutTray.sep_col,0,0,0,0]
        self.check_AND_moveL(new_pos)
        new_pos += [0,0,-0.08,0,0,0]
        self.check_AND_moveL(new_pos)

    
    def move_to_output_pen(self, i):
        """IVSN: 19/05/23 Pouring Penfill cartridge into corresponding vial
        Args:
            i: batch number"""
        self.check_AND_moveL(PEN_POUR_POSE)
        # calculation for the position of the corresponding output vial
        row, column = divmod(i, 3)
        pour_pos = PEN_POUR_POSE.copy() + [row*self.OutTray.sep_row, 
                                   column*self.OutTray.sep_col,0,0,0,0]
        self.check_AND_moveL(pour_pos, vel=0.075)
        curr_pos = pour_pos.copy()
        curr_pos += [0,0,-0.05,0,0,0]
        self.check_AND_moveL(curr_pos)

        # Put Labware
        # self.release_pen()

        # Pour
        # curr_pos += [0,0,0.08,0,0,0] 
        # self.check_AND_moveL(curr_pos)
        # curr_pos = self.turn_wrist(-90, curr_pos)
        # self.closed_fingers()
        # curr_pos = PEN_POUR_POSE2.copy() + [row*self.OutTray.sep_row, 
        #                            column*self.OutTray.sep_col,0,0,0,0]
        # self.check_AND_moveL(curr_pos+[0,0,0.05,0,0,0])
        # self.check_AND_moveL(curr_pos-[0,0,0.03,0,0,0])
        # self.open_fingers()
        # self.check_AND_moveL(curr_pos+[0,0,0.08,0,0,0])
        # self.turn_wrist(90, curr_pos+[0,0,0.08,0,0,0])

        # Get Labware
        # self.check_AND_moveL(pour_pos)
        # curr_pos = pour_pos.copy()
        # curr_pos += [0,0,-0.05,0,0,0]
        # self.check_AND_moveL(curr_pos)
        # self.grip_pen(curr_pos,9)
        # self.check_AND_moveL(PEN_DISPOSE_POSE)
        # self.release_pen()

    def pour_pen(self, i):
        row, column = divmod(i, 3)
        curr_pos = self.receive.getActualTCPPose()
        curr_pos += [0,0,0.08,0,0,0] 
        self.check_AND_moveL(curr_pos)
        curr_pos = self.turn_wrist(-90, curr_pos)
        self.closed_fingers()
        curr_pos = PEN_POUR_POSE2.copy() + [row*self.OutTray.sep_row, 
                                   column*self.OutTray.sep_col,0,0,0,0]
        self.check_AND_moveL(curr_pos+[0,0,0.05,0,0,0])
        self.check_AND_moveL(curr_pos-[0,0,0.03,0,0,0])
        self.open_fingers()
        self.check_AND_moveL(curr_pos+[0,0,0.08,0,0,0])
        self.turn_wrist(90, curr_pos+[0,0,0.08,0,0,0])


    def pick_output_pen(self, i):
        row, column = divmod(i, 3)
        pour_pos = PEN_POUR_POSE.copy() + [row*self.OutTray.sep_row, 
        column*self.OutTray.sep_col,0,0,0,0]
        curr_pos = pour_pos.copy()
        curr_pos += [0,0,-0.05,0,0,0]
        self.check_AND_moveL(curr_pos)
        # self.grip_pen(curr_pos,9)
    
    def dispose_pen(self):
        self.check_AND_moveL(PEN_DISPOSE_POSE)
        self.release_pen()


    def dispose_syringe(self):
        """"IVSN: 19/05/23 Dispose of PFS by dropping it into built-in hole"""
        self.check_AND_moveL(SYR_DISPOSE_POSE)
        current_pose = SYR_DISPOSE_POSE.copy()
        move_down = [0,0,-0.07,0,0,0]
        move_back = [0.075,0,0,0,0,0]
        self.check_AND_moveL(current_pose+move_down)
        current_pose += move_down
        self.check_AND_moveL(current_pose+move_back)
        self.check_AND_moveL(SYR_DISPOSE_POSE + move_back)


    ##looping programs 
    def turn_wrist(self, deg: float, pos: list):
        """IVSN: 19/05/23 Turn wrist function. Gets joint position and moves the last 
        joint according to arguments
        Args: 
            deg: number of degrees to turn
            pos: current position of the robot arm"""
        turn = math.radians(deg)
        curr = self.connection.getInverseKinematics(pos)
        curr[-1] += turn
        self.connection.moveJ(curr)
        time.sleep(0.5)
        return self.receive.getActualTCPPose()



    def syringe_loop(self, target_row:list, target_col: list, i: int ,j: int):
        """IVSN: 19/05/23 Looping function to process PFS
            Args:
                target_row: row position of the PFS in input tray
                target_col: column position of the PFS in input tray
                i: batch number
                j: sample number"""
        self.closed_fingers()
        self.release_syr()
        self.check_AND_moveJ(target_row)
        print(target_col)
        self.check_AND_moveL(target_col+offset_moveL)
        self.grip_syr(target_col+offset_moveL,3)
        self.move_to_decapper(self.Lmat[i][j])
        self.decap_syr()
        threading.Thread(target = self.prepare_for_output_festo).start()
        self.move_to_output_syr(i)
        self.pour_syringe()
        self.check_AND_moveL(SYR_POUR_POSE)
        self.open_fingers()
        self.dispose_syringe()
        self.go_home()

    def pen_loop(self, target_row:list, target_col: list, i: int ,j: int,large: bool, only_decap):
        """IVSN: 19/05/23 Looping function to process Penfills
            Args:
                target_row: row position of the Penfill in input tray
                target_col: column position of the Penfill in input tray
                i: batch number
                j: sample number"""
        self.closed_fingers()
        self.release_pen()
        self.release_pen()
        self.check_AND_moveJ(target_row)
        self.check_AND_moveL(target_col)
        self.check_AND_moveL(target_col+offset_moveL)
        current_pos = target_col+offset_moveL
        self.grip_pen(current_pos,3)
        self.move_to_decapper(self.Lmat[i][j])
        self.decap_pen(large)
        if not only_decap:
            self.regrip_pen()

            self.prepare_for_ManOutput_UR_wrapper(("support tray",i+1),1,"Large Penfill" if large else "Small Penfill",\
                   "Lpen" if large else "SPenfill")
            thread = threading.Thread(
            target=self.prepare_for_Input_Festo_wrapper,
            args=(("support tray extended", i), 1, "Large Penfill" if large else "Small Penfill",\
                   "Lpen" if large else "SPenfill")
            )
            thread.start()

            self.putLabware_ManUR_wrapper(("support tray",i+1),1,"Large Penfill" if large else "Small Penfill",\
                   "Lpen" if large else "SPenfill")
            
            self.pour_pen(i)

            self.prepare_for_ManInput_UR_wrapper(("support tray",i+1),1,"Large Penfill" if large else "Small Penfill",\
                   "Lpen" if large else "SPenfill")
            thread = threading.Thread(
            target=self.prepare_for_Output_Festo_wrapper,
            args=(("support tray extended", i), 1, "Large Penfill" if large else "Small Penfill",\
                   "Lpen" if large else "SPenfill")
            )
            thread.start()
            self.getLabware_ManUR_wrapper(("support tray",i+1),1,"Large Penfill" if large else "Small Penfill",\
                   "Lpen" if large else "SPenfill")
            self.dispose_pen()

            # self.move_to_output_pen(i)
        else:
            self.check_AND_moveL(target_col)
            self.check_AND_moveL(target_col+offset_moveL)
            self.release_pen()



    def tray_loop(self, only_decap):
        """IVSN: 19/05/23 Main function that calls the corresponding loop to process a single PFS or Penfill"""
        for i in range(len(self.Lmat)):
            for j in range(len(self.Lmat[i])):
                target_row = initial_target_syringe.copy() if isinstance(self.Lmat[i][j],Syringe) else initial_target_pen.copy()
                if i % 2 == 1:
                    target_row[0] += self.Tray.sep_x_double
                target_row[1] -= self.Tray.sep_y * (i//2)
                target_col = target_row.copy()
                time.sleep(0.1)
                if self.Lmat[i][j] is not None:
                    target_col[0] += self.Tray.sep_x * j
                    if isinstance(self.Lmat[i][j], Syringe):
                        self.syringe_loop(target_row, target_col, i, j)
                    elif isinstance(self.Lmat[i][j], LPen):
                        self.pen_loop(target_row, target_col, i, j,True, only_decap)
                    else:
                        self.pen_loop(target_row, target_col, i, j,False, only_decap)
                    time.sleep(1)
                else:
                    pass
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
        response = self.configure_robot_params(SyrSamp, SyrBatch, LPenSamp, LPenBatch, SPenSamp, SPenBatch)
        if not response:
            return False
        self.prepare_for_Input_Festo_wrapper(("position",1),1,"large", "L")
        # self.prepare_for_ManOutput_UR_wrapper(("support tray",1),1)
        # self.go_home()
        # self.tray_loop(only_decap = False)
        return True
    
    def run_decapping(self, LPen, Spen):
        response = self.configure_decapping(LPen, Spen)
        if not response:
            return False
        self.go_home()
        self.tray_loop(only_decap = True)
        return True


    def prepare_for_input_festo(self):
        print("prepare for input Festo")
        # if not self.receive.getDigitalOutputState(2):
        #     self.IO.setStandardDigitalOut(2,True)
        return "True"

    def prepare_for_output_festo(self, InternalPosition):
        print("prepare for output Festo")
        if self.receive.getDigitalOutputState(2) and InternalPosition == 2:
            self.IO.setStandardDigitalOut(2,False)
        elif not self.receive.getDigitalOutputState(2) and InternalPosition == 1:
            self.IO.setStandardDigitalOut(2,True)
        return True
    
    def prepare_for_Input_Festo_wrapper(self, position, internal_position, labware_type, labware_unique_id):
        self.FestoController.PrepareForInput(position, internal_position, labware_type, labware_unique_id, \
                                             metadata=[], instance=ObservableCommandInstance(Queue()))

    def prepare_for_Output_Festo_wrapper(self, position, internal_position, labware_type, labware_unique_id):
        self.FestoController.PrepareForOutput(position, internal_position, labware_type, labware_unique_id)

    def prepare_for_input_UR(self, HandoverPosition):
        print("prepare for input UR")
        self.pick_output_pen(HandoverPosition)

    def prepare_for_output_UR(self, HandoverPosition):
        print("prepare for output UR")
        self.move_to_output_pen(HandoverPosition)

    def putLabwareUR(self):
        print("put labware UR")
        self.release_pen()
        return True
    
    def getLabwareUR(self, HandoverPosition):
        print("get labware UR")
        row, column = divmod(HandoverPosition, 3)
        pour_pos = PEN_POUR_POSE.copy() + [row*self.OutTray.sep_row, 
        column*self.OutTray.sep_col,0,0,0,0]
        self.grip_pen(pour_pos)
        return True
    
    def prepare_for_ManInput_UR_wrapper(self, position, internal_position, labware_type, labware_unique_id):
        self.ManControllerUR.PrepareForInput(position, internal_position, labware_type, labware_unique_id)

    def prepare_for_ManOutput_UR_wrapper(self, position, internal_position):
        self.ManControllerUR.PrepareForOutput(position, internal_position)

    def putLabware_ManUR_wrapper(self, position, internal_position):
        self.ManControllerUR.PutLabware(position, internal_position)

    def getLabware_ManUR_wrapper(self,position, internal_position):
        self.ManControllerUR.GetLabware(position, internal_position)
