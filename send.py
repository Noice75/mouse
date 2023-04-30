import socket
import pickle
import runtimeREF
import server
import client

MCAST_GRP = '224.0.0.1'
MCAST_PORT = 5007
MULTICAST_TTL = 2
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)


def send(**kwargs): #udp
    print(kwargs)
    sock.sendto(pickle.dumps(kwargs),
                (runtimeREF.ACTIVEIP, MCAST_PORT))
    
def udpSendALL(**kwargs): # Not supported by all routers! Thats why tcp sendAll is used
    sock.sendto(pickle.dumps(kwargs),
                (MCAST_GRP, MCAST_PORT))


def sendWithIP(**kwargs): #udp
    sock.sendto(pickle.dumps(kwargs),
                (kwargs["IP"], MCAST_PORT))
    
def sendALL(**kwargs): #tcp
    if(runtimeREF.ISSERVER):
        server.sendAll(kwargs)
        return
    kwargs["IP"] = None #When IP = None, Server Sends data to all clients
    client.send(kwargs)

def tcpSend(**kwargs): #tcp
    if(runtimeREF.ISSERVER):
        server.send(kwargs)
        return
    client.send(kwargs)



if __name__ == "__main__":
    pass
