import socket

SENSITIVITY = 2
HOSTNAME = socket.gethostname()
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
HOSTIP = s.getsockname()[0]
ACTIVEIP = s.getsockname()[0]
ISSERVER = False
fnDir = None

def setActiveIP(arg):
    global ACTIVEIP
    ACTIVEIP = arg["ACTIVEIP"]
    print(ACTIVEIP)