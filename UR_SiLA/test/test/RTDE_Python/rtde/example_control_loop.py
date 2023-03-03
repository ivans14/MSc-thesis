

import logging
import sys

import rtde_2 as rtde
import rtde_config as rtde_config


# logging.basicConfig(level=logging.INFO)

ROBOT_HOST = "192.168.0.30"
ROBOT_PORT = 30004
config_filename = "control_loop_configuration.xml"

keep_running = True

logging.getLogger().setLevel(logging.INFO)

conf = rtde_config.ConfigFile(config_filename)
state_names, state_types = conf.get_recipe("state")
setp_names, setp_types = conf.get_recipe("setp")
watchdog_names, watchdog_types = conf.get_recipe("watchdog")

con = rtde.RTDE(ROBOT_HOST, ROBOT_PORT)
con.connect()

print("connected")

# get controller version
con.get_controller_version()

# setup recipes
con.send_output_setup(state_names, state_types)
setp = con.send_input_setup(setp_names, setp_types)
watchdog = con.send_input_setup(watchdog_names, watchdog_types)

# Setpoints to move the robot to
setp1 = [-0.4104577419847799, -0.2626529489715343, 0.2972660465054066, 1.8552623321968715, 2.420037547531281, -0.014278932653435552]
setp2 =  [-0.2646567753143876, -0.43843427581831246, 0.2897307437164788, -1.54430191234484, -2.6607790325617, 0.17527592292018854]

setpoints = [setp1,setp2]

setp.input_double_register_0 = 0
setp.input_double_register_1 = 0
setp.input_double_register_2 = 0
setp.input_double_register_3 = 0
setp.input_double_register_4 = 0
setp.input_double_register_5 = 0

# The function "rtde_set_watchdog" in the "rtde_control_loop.urp" creates a 1 Hz watchdog
watchdog.input_int_register_0 = 0


def setp_to_list(sp):
    sp_list = []
    for i in range(0, 6):
        sp_list.append(sp.__dict__["input_double_register_%i" % i])
    return sp_list


def list_to_setp(sp, list):
    for i in range(0, 6):
        sp.__dict__["input_double_register_%i" % i] = list[i]
    return sp


# start data synchronization
if not con.send_start():
    sys.exit()

# control loop
move_completed = True
state = con.receive()
print("inital pose",state.actual_TCP_pose)
i = 0
while keep_running:
    # receive the current state
    state = con.receive()

    if state is None:
        break

    # do something...
    # print(state.output_int_register_0==0,not not  move_completed,
    #       not move_completed and state.output_int_register_0 == 0)
    if move_completed and state.output_int_register_0 == 1:
        print(i)
        move_completed = False
        new_setp = setpoints[i]
        list_to_setp(setp, new_setp)
        print("New pose = " + str(new_setp))
        # send new setpoint
        con.send(setp)
        watchdog.input_int_register_0 = 1
        i = 1 if i==0 else 0
    elif not move_completed and state.output_int_register_0 == 0:
        print("Move to confirmed pose = " + str(state.target_TCP_pose))
        move_completed = True
        watchdog.input_int_register_0 = 0

    # print("e")
    # kick watchdog
    con.send(watchdog)

con.send_pause()

con.disconnect()
