import socket
import threading

TCP_PORT = 505
MESSAGE = "UwU"
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip_address = s.getsockname()[0]
ip_range = '.'.join(ip_address.split('.')[0:3]) + '.'
connection = None
threads = []


def connect(ip_address):
    global connection
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect((ip_address, 505))
        s.send(MESSAGE.encode())
        if (s.recv(1024).decode() == MESSAGE):
            connection = s
            print(f"Server at {ip_address}:505")
        else:
            s.close()
    except:
        pass


for i in range(1, 256):
    ip_address = ip_range + str(i)
    thread = threading.Thread(target=connect, args=(ip_address,))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()
