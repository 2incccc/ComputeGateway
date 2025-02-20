import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = 'localhost'
port = 12345

server_socket.bind((host, port))

server_socket.listen(5)
print("Gateway listening on port 12345")

conn, addr = server_socket.accept()
print(f"Connected to node at {addr}")

data = conn.recv(1024).decode()
print(f"Received from node: {data}")

response = "I have 4 CPU and 8 GB memory"
conn.sendall(response.encode())

conn.close()