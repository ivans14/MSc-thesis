from __future__ import annotations
import socket
import sys
from typing import List, Dict, Tuple, Union
from abc import ABC, abstractmethod
from time import sleep
from dataclasses import dataclass


class RobotInterface(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def go_home(self):
        print("Time to go home.")
        pass

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def pick(self, handover: Tuple[int, int]):
        pass

    @abstractmethod
    def place(self, handover: Tuple[int, int]):
        pass

    @abstractmethod
    def move_to(self, pos: List[float]):
        pass

    @abstractmethod
    def grip_open(self):
        pass

    @abstractmethod
    def grip_close(self):
        pass


cm_to_units = 10


@dataclass
class Offset:
    dimension: int
    distance: float  # distance in cm


@dataclass
class Position:
    x: float
    y: float
    z: float
    yaw: float
    pitch: float
    roll: float
    offset: Offset

    def nest(self) -> List[float]:
        return [self.x, self.y, self.z, self.yaw, self.pitch, self.roll]

    def approach(self) -> List[float]:
        approach = self.nest()
        approach[self.offset.dimension-1] += self.offset.distance * cm_to_units
        return approach

    #def __str__(self):
    #    return ""

    @staticmethod
    def parse_string(s: str) -> Position:
        return Position(0, 0, 0, Offset(0, 0))


devices: Dict[int, Dict[int, int]] = {
    1: {1: 1},
    2: {1: 2, 2: 3, 3: 4},
    3: {1: 5},
    4: {1: 6, 2: 7, 3: 8, 4: 9, 5: 10, 6: 11, 7: 12, 8: 13, 9: 14, 10: 15, 11: 16, 12: 17, 13: 18, 14: 19}
}

# profile_number: Tuple (speed and speed2)
movement_profiles: Dict[int, Tuple] = {
    2: (50, 50),
    3: (20, 20),
    4: (5, 5)
}

positions: Dict[int, Position] = {
    1: Position(x=177.84, y=-262.598, z=12.952, yaw=-90.869, pitch=90, roll=180, offset=Offset(dimension=3, distance=5)),
    2: Position(x=298.867, y=-31.653, z=14.901, yaw=-1.02, pitch=90, roll=180, offset=Offset(dimension=3, distance=5)),
    3: Position(x=299.08, y=68.068, z=13.579, yaw=-0.773, pitch=90, roll=180, offset=Offset(dimension=3, distance=5)),
    4: Position(x=299.08, y=168.068, z=13.579, yaw=-0.773, pitch=90, roll=180, offset=Offset(dimension=3, distance=5)),
    5: Position(x=167.833, y=383.712, z=16.504, yaw=0.026, pitch=90, roll=-180, offset=Offset(dimension=3, distance=5)),
    8: Position(x=-133.642, y=214.806, z=381.896, yaw=179.439, pitch=90, roll=-180 ,offset=Offset(dimension=1, distance=15)),
    9: Position(x=-133.642, y=214.806, z=348.008, yaw=179.439, pitch=90, roll=-180 ,offset=Offset(dimension=1, distance=15)),
    10: Position(x=-133.642, y=214.806, z=314.120, yaw=179.439, pitch=90, roll=-180 ,offset=Offset(dimension=1, distance=15)),
    11: Position(x=-133.642, y=214.806, z=280.232, yaw=179.439, pitch=90, roll=-180 ,offset=Offset(dimension=1, distance=15)),
    12: Position(x=-133.642, y=214.806, z=246.345, yaw=179.439, pitch=90, roll=-180 ,offset=Offset(dimension=1, distance=15)),
    13: Position(x=-133.642, y=214.806, z=212.457, yaw=179.439, pitch=90, roll=-180 ,offset=Offset(dimension=1, distance=15)),
    14: Position(x=-133.642, y=214.806, z=178.569, yaw=179.439, pitch=90, roll=-180 ,offset=Offset(dimension=1, distance=15)),
    15: Position(x=-133.642, y=214.806, z=144.681, yaw=179.439, pitch=90, roll=-180 ,offset=Offset(dimension=1, distance=15)),
    16: Position(x=-133.642, y=214.806, z=110.794, yaw=179.439, pitch=90, roll=-180 ,offset=Offset(dimension=1, distance=15)),
    17: Position(x=-133.642, y=214.806, z=76.906, yaw=179.439, pitch=90, roll=-180 ,offset=Offset(dimension=1, distance=15)),
    18: Position(x=-133.642, y=214.806, z=43.018, yaw=179.439, pitch=90, roll=-180 ,offset=Offset(dimension=1, distance=15)),
    19: Position(x=-133.642, y=214.806, z=9.131, yaw=179.439, pitch=90, roll=-180 ,offset=Offset(dimension=1, distance=15)),
    # etc...
}


class PreciseInterface(RobotInterface):
    def grip_open(self):
        pass

    def grip_close(self):
        pass

    def move_to(self, pos: List[float]):
        pass

    BYTES_BUFFER = 128
    # Precise Flex Robot
    HOST = '192.168.0.17'
    PORT = 10100
    SLOW = 4
    NORMAL = 1
    RACK_OFFSET = .5  # cm

    def __init__(self):
        super(PreciseInterface, self).__init__()
        self.s = None
        for res in socket.getaddrinfo(self.HOST, self.PORT, socket.AF_UNSPEC, socket.SOCK_STREAM):
            af, socktype, proto, canonname, sa = res
            try:
                self.s = socket.socket(af, socktype, proto)
                print(self.s)
            except OSError as msg:
                self.s = None
                continue
            try:
                print(sa)
                self.s.connect(sa)
            except OSError as msg:
                print(msg)
                self.s.close()
                self.s = None
                continue
            break
        print('Socket connected')
        if self.s is None:
            print('Could not open socket')
            # sys.exit(1)
        self.connect()
        self.configure_movement_profiles()

    def __del__(self):
        self.s.shutdown(0), self.s.close()

    def send_command(self, cmd: str):
        self.s.send(str.encode(cmd))
        return self.receive_data()
    
    def receive_data(self):
        return self.s.recv(self.BYTES_BUFFER)

    @staticmethod
    def str_to_position(position_string: str) -> List:
        status, x, y, z, yaw, pitch, roll, _ = str.split(str(position_string), ' ')
        return [status, x, y, z, yaw, pitch, roll, _]

    @staticmethod
    def position_to_str(position: list) -> str:
        return ' '.join(i for i in position)

    def connect(self):
        self.send_command(cmd=f'open {self.HOST} {self.PORT}\n')
        self.send_command(cmd=f'attach 1\n')
        self.send_command(cmd='hp 1\n')
        print('Connected device successfully!')

    def configure_movement_profiles(self):
        for profile, params in movement_profiles.items():
            self.set_movement_profile(profile_index=profile,
                                      speed=params[0],
                                      speed_2=params[1])

    def pick(self, handover: Tuple[int, int]):
        print('picking ', handover)
        pos_index = handover[0]
        sub_pos_index = handover[1]
        position_number = devices[pos_index][sub_pos_index]
        position = positions[position_number]
        print(position_number)
        # movements
        print(position)
        print(position.approach())
        self.open_gripper()
        self.move_to_cartesian_position(self.NORMAL, position.approach())
        if pos_index == 4:
            # move a bit higher
            above_nest = position.nest()
            above_nest[2] += cm_to_units * self.RACK_OFFSET
            self.move_to_cartesian_position(self.SLOW, above_nest)
        self.move_to_cartesian_position(self.SLOW, position.nest())
        self.close_gripper()
        if pos_index == 4:
            # move a bit higher
            above_nest = position.nest()
            above_nest[2] += cm_to_units * self.RACK_OFFSET
            self.move_to_cartesian_position(self.SLOW, above_nest)
        self.move_to_cartesian_position(self.SLOW, position.approach())

    def place(self, handover: Tuple[int, int]):
        print('placing ', handover)
        pos_index = handover[0]
        sub_pos_index = handover[1]
        position_number = devices[pos_index][sub_pos_index]
        position = positions[position_number]
        print(position_number)
        # movements
        print(position)
        print(position.approach())
        self.move_to_cartesian_position(self.NORMAL, position.approach())
        if pos_index == 4:
            # move a bit higher
            above_nest = position.nest()
            above_nest[2] += cm_to_units * self.RACK_OFFSET
            self.move_to_cartesian_position(self.SLOW, above_nest)
        self.move_to_cartesian_position(self.SLOW, position.nest())
        self.open_gripper()
        if pos_index == 4:
            # move a bit higher
            above_nest = position.nest()
            above_nest[2] += cm_to_units * self.RACK_OFFSET
            self.move_to_cartesian_position(self.SLOW, above_nest)
        self.move_to_cartesian_position(self.SLOW, position.approach())

    def enter_free_mode(self):
        self.send_command(f'FreeMode 0\n')

    def exit_free_mode(self):
        self.send_command(f'FreeMode -1\n')

    # gripper commands
    def open_gripper(self):
        self.send_command(f"Gripper 1\n")

    def close_gripper(self):
        self.send_command(f"Gripper 2\n")
    # movement commands

    def go_home(self):
        self.send_command(f'Home\n')

    def move_to_station(self, station_index: int):
        self.send_command(f'Move {station_index}\n')

    def move_to_cartesian_position(self, profile: int, position_cartesian: list):
        position = ' '.join(str(i) for i in position_cartesian)
        self.send_command(f'MoveC {profile} {position}\n')

    def move_to_angle_position(self, profile: int, position_angle: list):
        position = ' '.join(str(i) for i in position_angle)
        self.send_command(f'MoveJ {profile} {position}\n')

    def save_current_position_as_cartesian(self, station_index: int):
        self.send_command(f'HereC {station_index}\n')

    def save_current_position_as_angle(self, station_index: int):
        self.send_command(f'HereJ {station_index}\n')

    def save_position_as_cartesian(self, station_index: int, position_cartesian: list) -> str:
        return self.send_command(f'locXyz {station_index} {position_cartesian}\n')

    def save_position_as_angle(self, station_index: int, position_angle: list) -> str:
        return self.send_command(f'locAngles {station_index} {position_angle}\n')

    def get_position_as_cartesian(self) -> str:
        return self.send_command(f'wherec\n')

    def get_position_as_angle(self) -> str:
        return self.send_command(f'wherej\n')

    def set_movement_profile(self, profile_index: int, speed: int=None, speed_2: int=None, accel: int=None,
                             decel: int=None, accel_ramp: int=None, decel_ramp: int=None, in_range: int=None,
                             straight: int=None):
        single_commands_list = ['Speed', 'Speed2', 'Accel', 'AccRamp', 'Decel', 'DecRamp', 'InRange', 'Straight']
        parameter_list = [speed, speed_2, accel, decel, accel_ramp, decel_ramp, in_range, straight]
        if None in parameter_list:
            # Set only the params that have been changed individually
            for i, param in enumerate(parameter_list):
                if param is not None:
                    self.send_command(f'{single_commands_list[i]} {profile_index} {param}\n')
            return
        else:
            # Set all params at once
            self.send_command(
                f'Profile {profile_index} {speed} {speed_2} {accel} {decel} {accel_ramp} {decel_ramp} {in_range} {straight}\n')


if __name__ == '__main__':
    # just for playing around
    # interface = PreciseInterface()
    pass
