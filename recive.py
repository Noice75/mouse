import socket
import struct
import pickle
import keyboard
import mouse
import listners
import threading

MCAST_GRP = '224.0.0.1'
MCAST_PORT = 5007
IS_ALL_GROUPS = True

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
if IS_ALL_GROUPS:
    # on this port, receives ALL multicast groups
    sock.bind(('', MCAST_PORT))
else:
    # on this port, listen ONLY to MCAST_GRP
    sock.bind((MCAST_GRP, MCAST_PORT))
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)

sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

# Defined functions
fnDir = {
    0: keyboard.keyboardInput,
    1: mouse.move,
    2: mouse.clickMouseButton,
    3: mouse.scroll,
    50: listners.active,
}

while True:
    data = pickle.loads(sock.recv(1024))
    if (data[0]["fn"] >= 50):
        threading.Thread(
            target=fnDir[data[0]["fn"]], args=(data[0],)).start()
    else:
        fnDir[data[0]["fn"]](data[0])
