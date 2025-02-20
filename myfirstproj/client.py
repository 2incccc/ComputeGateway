import socket


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = 'localhost'
port = 12345
client_socket.connect((host, port))

message = "I need 4 CPU and 8 GB memory"
client_socket.send(message.encode())

response = client_socket.recv(1024).decode()
print(f"Received response from server: {response}")

client_socket.close()

