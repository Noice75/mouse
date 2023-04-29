import socket
import threading
import pickle
import runtimeREF

TCP_PORT = 6969
ip_range = '.'.join(runtimeREF.HOSTIP.split('.')[0:3]) + '.'
connection = None
threads = []


def send(arg):
    connection.send(arg)


def connect(ip_address):
    global connection
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect((ip_address, 6969))
        connection = s
        connection.settimeout(None)
        print(f"Server at {ip_address}:505")
    except:
        s.close()
        pass


def getServer():
    for i in range(1, 256):
        ip_address = ip_range + str(i)
        thread = threading.Thread(target=connect, args=(ip_address,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    if (connection == None):
        return False
    return True


if __name__ == "__main__":
    if (getServer()):
        while True:
            try:
                data = connection.recv(1024)
            except ConnectionResetError:
                print("disconnected")
                break
            if not data:
                print("disconnected")
                break
            # unpickling after checks to prevent error `EOFError: Ran out of input`
            data = pickle.loads(data)
            print(data)
