import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip_address = s.getsockname()[0]
port = 505
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((ip_address, port))
s.listen(5)

print(f"Server listening on {ip_address}:{port}")
clients = []
while True:
    conn, addr = s.accept()
    print(f"Connection from {addr[0]}:{addr[1]}")
    if (conn.recv(1024).decode() != "UwU"):
        print("Connection REFUSED... Closing")
        conn.close()
        continue
    message = "UwU"
    conn.sendall(message.encode())
    clients.append(conn)
