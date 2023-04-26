import socket
import pickle

MCAST_GRP = '224.0.0.1'
MCAST_PORT = 5007
MULTICAST_TTL = 2
SENSITIVITY = 2
HOSTNAME = socket.gethostname()
HOSTIP = socket.gethostbyname(HOSTNAME)
activeIP = socket.gethostbyname(HOSTNAME)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)


def send(**kwargs):
    print(kwargs)
    sock.sendto(pickle.dumps((kwargs, HOSTNAME, HOSTIP)),
                (activeIP, MCAST_PORT))


def sendALL(**kwargs):
    sock.sendto(pickle.dumps((kwargs, HOSTNAME, HOSTIP)),
                (MCAST_GRP, MCAST_PORT))


def sendWithIP(**kwargs):
    sock.sendto(pickle.dumps((kwargs, HOSTNAME, HOSTIP)),
                (kwargs["IP"], MCAST_PORT))


if __name__ == "__main__":
    sendWithIP(fn=50, IP="192.168.1.101")
