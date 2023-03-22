import socket
import time

Ip = '192.168.0.30'
BUFFER_SIZE = 4096
port = 29999

def SelectPlayProgram(
            ProgramName: str,
            Ip: str,
            port: int
    ) :
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect((Ip, port))
        data = s.recv(BUFFER_SIZE)
        print(f'Data received: {data}')
        # select program
        cmd = 'load ' + ProgramName + '\n'
        s.sendall(cmd.encode())
        data1 = s.recv(BUFFER_SIZE)
        print('load sent')
        print(ProgramName)
        print(f'Data received: {data1}')
        # play program
        cmd = 'play' + '\n'
        s.sendall(cmd.encode())
        data1 = s.recv(BUFFER_SIZE)
        print('play sent')
        print(f'Data received: {data1}')
        s.close()
        time.sleep(1)
        response = data1.decode("utf-8")
        print(response)

SelectPlayProgram('rtde_control_loop.urp', Ip, port)