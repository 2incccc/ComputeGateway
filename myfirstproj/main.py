import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = 'localhost'
port = 12345

server_socket.bind((host, port))

server_socket.listen(5)
print("Gateway listening on port 12345")

client_socket.connect((host, port))

conn, addr = server_socket.accept()
print(f"Connected to client at {addr}")

client_socket.send("I need 4 CPU and 8 GB memory".encode()) 



data = conn.recv(1024).decode()
print(f"Received from client: {data}")


conn.close()
client_socket.close()