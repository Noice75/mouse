import socket
import struct
import pickle
import runtimeREF
import listners
import threading
import server
import client
import mouse
import keyboard
import clipboard

MCAST_GRP = '224.0.0.1'
MCAST_PORT = 5007

# Socket Setup
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', MCAST_PORT))
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

# Defined functions
runtimeREF.fnDir = {
    0: keyboard.keyboardInput,
    1: mouse.move,
    2: mouse.clickMouseButton,
    3: mouse.scroll,
    4: listners.setActiveIP,
    5: runtimeREF.updateClients,
    50: listners.active,
    51: clipboard.setClipboard,
}
fnDir = runtimeREF.fnDir
def clientConnListner():
    while True:
        try:
            data = client.connection.recv(1024)
        except ConnectionResetError:
            print("Server disconnected")
            break
        if not data:
            print("Server disconnected")
            break
        # unpickling after checks to prevent error `EOFError: Ran out of input`
        data = pickle.loads(data)
        print(data)
        if (data["fn"] >= 50):  # Threaded function needs to have key > 50
            threading.Thread(
                target=fnDir[data["fn"]], args=(data,)).start()
        else:
            fnDir[data["fn"]](data)


if (client.getServer()):
    threading.Thread(target=clientConnListner).start()
else:
    server = threading.Thread(target=server.server)
    server.start()
    listners.activeThreads["server"] = server
    threading.Thread(target=listners.active,args=({"ACTIVEIP":runtimeREF.ACTIVEIP},)).start()

while True:
    data = pickle.loads(sock.recv(1024))
    print(data)
    if (data["fn"] >= 50):  # Threaded function needs to have key > 50
        threading.Thread(
            target=fnDir[data["fn"]], args=(data,)).start()
    else:
        fnDir[data["fn"]](data)