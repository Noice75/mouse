import socket
import select
import pickle
import runtimeREF
import threading
import time

port = 6969
clients = {}


def send(arg):
    for clientSock, clientAddress in clients.items():
        if clientAddress[0] == arg["IP"]:
            clientSock.sendall(pickle.dumps(arg))


def sendAll(arg):
    for clientSock, _ in clients.items():
        clientSock.sendall(pickle.dumps(arg))


def onClientConnect(clientSocket, clientAddr):
    global clients
    sendAll({"fn":53, "Task":0, "Addr":clientAddr[0]})
    runtimeREF.clients.append(clientAddr[0])
    clients[clientSocket] = clientAddr
    clientSocket.send(pickle.dumps({"fn":54,"ACTIVEIP":runtimeREF.ACTIVEIP, "Task":2, "Clients": runtimeREF.clients}))

def onClientDisconnect(sock):
    global clients
    disconnectedClientAddr = clients[sock][0]
    del clients[sock]
    if(disconnectedClientAddr == runtimeREF.ACTIVEIP):
        runtimeREF.ACTIVEIP = runtimeREF.HOSTIP
        sendAll({"fn":52,"ACTIVEIP":runtimeREF.ACTIVEIP})
        threading.Thread(target=runtimeREF.fnDir[50], args=({"ACTIVEIP":runtimeREF.ACTIVEIP},)).start()
    # remove client from list of clients if connection is closed
    sendAll({"fn":53, "Task":1, "Addr":disconnectedClientAddr})
    runtimeREF.clients.remove(disconnectedClientAddr)


def server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((runtimeREF.HOSTIP, port))
    s.listen(0)  # Set the maximum number of queued connections to infinity
    print(f"TCP Server listening on {runtimeREF.HOSTIP}:{port}")
    runtimeREF.ACTIVEIP = runtimeREF.HOSTIP
    runtimeREF.ISSERVER = True
    runtimeREF.clients.append(runtimeREF.HOSTIP)
    while True:
        # wait for incoming data on the socket
        read_sockets, _, _ = select.select([s] + list(clients.keys()), [], [])
        for sock in read_sockets:
            # if a new connection is made
            if sock == s:
                # accept the connection and add client to list of clients
                clientSocket, clientAddress = s.accept()
                onClientConnect(clientSocket=clientSocket, clientAddr=clientAddress)
                print(f"New client connected: {clientAddress}")

            # if existing client has sent data
            else:
                try:
                    data = sock.recv(1024)
                except ConnectionResetError:
                    onClientDisconnect(sock=sock)
                    print("Client disconnected")
                    continue
                if not data:
                    onClientDisconnect(sock=sock)
                    print("Client disconnected")
                    continue
                # unpickling after checks to prevent error `EOFError: Ran out of input`
                data = pickle.loads(data)
                if (data["IP"] != runtimeREF.HOSTIP and data["IP"] != None):
                    send(data)
                elif (data["IP"] == None):
                    sendAll(data)
                    if (data["fn"] >= 50):  # Threaded function needs to have key > 50
                        threading.Thread(
                            target=runtimeREF.fnDir[data["fn"]], args=(data,)).start()
                    else:
                        runtimeREF.fnDir[data["fn"]](data)
                elif (data["IP"] == runtimeREF.HOSTIP):
                    if (data["fn"] >= 50):  # Threaded function needs to have key > 50
                        threading.Thread(
                            target=runtimeREF.fnDir[data["fn"]], args=(data,)).start()
                    else:
                        runtimeREF.fnDir[data["fn"]](data)


if __name__ == "__main__":
    server()
    sendAll({"IP":"192.168.1.1"})
