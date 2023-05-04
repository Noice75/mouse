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
    clients = arg["Clients"]
