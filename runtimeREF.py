import socket

SENSITIVITY = 2
HOSTNAME = socket.gethostname()
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
HOSTIP = s.getsockname()[0]
ACTIVEIP = s.getsockname()[0]
ISSERVER = False
fnDir = None
clients = []

def updateClients(arg):
    global clients
    if(arg["Task"] == 0):
        clients.append(arg["Addr"])
    elif(arg["Task"] == 1):
        clients.remove(arg["Addr"])
    elif(arg["Task"] == 2):
        clients = arg["Clients"]