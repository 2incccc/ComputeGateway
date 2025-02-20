import socket
import threading

# 模拟用户请求
def user_request(gateway_ip, gateway_port, request):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((gateway_ip, gateway_port))

    # 发送资源请求
    sock.sendall(request.encode())
    print(f"User sent request: {request}")

    # 等待算力网关返回资源分配结果
    data = sock.recv(1024).decode()
    print(f"User received response: {data}")

    sock.close()

# 启动用户请求
def start_user(gateway_ip, gateway_port, request="I need 4 CPU and 8 GB memory"):
    user_thread = threading.Thread(target=user_request, args=(gateway_ip, gateway_port, request))
    user_thread.start()
    user_thread.join()

