import socket
import select
import pickle
import runtimeREF
import threading

port = 6969
clients = {}


def send(arg):
    for client_sock, client_address in clients.items():
        if client_address[0] == arg["IP"]:
            client_sock.sendall(arg)


def sendAll(arg):
    for client_sock in clients.items():
        client_sock.sendall(arg)


def onClientConnect(clientSocket):
    clientSocket.sendall(pickle.dumps({"fn":4,"ACTIVEIP":runtimeREF.ACTIVEIP}))


def server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((runtimeREF.HOSTIP, port))
    s.listen(0)  # Set the maximum number of queued connections to infinity
    print(f"Server listening on {runtimeREF.HOSTIP}:{port}")
    runtimeREF.ISSERVER = True
    while True:
        # wait for incoming data on the socket
        read_sockets, _, _ = select.select([s] + list(clients.keys()), [], [])
        for sock in read_sockets:
            # if a new connection is made
            if sock == s:
                # accept the connection and add client to list of clients
                clientSocket, clientAddress = s.accept()
                clients[clientSocket] = clientAddress
                onClientConnect(clientSocket=clientSocket)
                print(f"New client connected: {clientAddress}")

            # if existing client has sent data
            else:
                try:
                    data = sock.recv(1024)
                except ConnectionResetError:
                    del clients[sock]
                    print("Client disconnected")
                    continue
                if not data:
                    # remove client from list of clients if connection is closed
                    del clients[sock]
                    print("Client disconnected")
                    # send data back to the client that sent it
                    # sock.sendall(data)
                    continue
                # unpickling after checks to prevent error `EOFError: Ran out of input`
                data = pickle.loads(data)
                print(f"Received data from client: {data}")
                if (data["IP"] != runtimeREF.HOSTIP and data["IP"] != None):
                    send(data)
                elif (data["IP"] == None):
                    sendAll(data)
                elif (data["IP"] == runtimeREF.HOSTIP):
                    if (data["fn"] >= 50):  # Threaded function needs to have key > 50
                        threading.Thread(
                            target=runtimeREF.fnDir[data["fn"]], args=(data,)).start()
                    else:
                        runtimeREF.fnDir[data["fn"]](data)


if __name__ == "__main__":
    server()
