# Echo client program
import socket
import sys

HOST = '192.168.0.17'    # The remote host
# Precise Flex Robot
PORT = 10100

# UR Robot
DashboardServer = 29999             # The same port as used by the server
PrimaryClient = 30001
SecondaryClient = 30002  # Robot state and version messages
PrimaryClientReadOnly = 30011  # Robot state messages

s = None
for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        s = socket.socket(af, socktype, proto)
    except OSError as msg:
        s = None
        continue
    try:
        s.connect(sa)
    except OSError as msg:
        s.close()
        s = None
        continue
    break
print('Socket connected')
if s is None:
    print('could not open socket')
    sys.exit(1)
try:
    with s:
        s.sendall(b'hp')
        msg = s.recv(1024)
        while msg:
            print('Received:' + msg.decode())
            msg = s.recv(1024)

        # disconnect the client
        s.close()
    print('Received', repr(msg))
except KeyboardInterrupt:
    pass