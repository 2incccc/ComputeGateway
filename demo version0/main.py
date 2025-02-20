import time
import socket
import threading
import random
import socket

class ComputeGateway:
    def __init__(self, gateway_id, port):
        self.gateway_id = gateway_id
        self.port = port
        self.nodes = []  # 存储从算力节点接收到的资源信息
        self.aggregation_layer = []  # 聚合层（最优的算力节点）

    def start(self):
        # 创建一个socket监听客户端（算力节点）连接
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('localhost', self.port))
        server_socket.listen(5)
        print(f"Gateway {self.gateway_id} listening on port {self.port}")

        while True:
            client_socket, addr = server_socket.accept()
            print(f"Connected to node at {addr}")

            # 接收资源信息
            data = client_socket.recv(1024).decode()
            print(f"Received from node: {data}")
            self.nodes.append(data)  # 将节点资源信息存储在网关中

            # 计算聚合节点（选择最优节点）
            self.compute_aggregation_layer()
            
            # 关闭连接
            client_socket.close()

    # def compute_aggregation_layer(self):
    #     # 计算聚合节点（例如，选择资源最多的两个节点）
    #     if len(self.nodes) > 0:
    #         # 假设根据节点信息中的内存和CPU选择最优节点
    #         sorted_nodes = sorted(self.nodes, key=lambda x: (int(x.split('=')[1].split()[0]), int(x.split('=')[2].split()[0])), reverse=True)
    #         self.aggregation_layer = sorted_nodes[:2]  # 选择最优的两个节点
    #         print(f"Gateway {self.gateway_id} Aggregation Layer: {self.aggregation_layer}")
    #     else:
    #         self.aggregation_layer = []
        
# 启动网关
def start_gateway(gateway_id, port):
    gateway = ComputeGateway(gateway_id, port)
    gateway.start()


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


def compute_node(node_id, gateway_ip, gateway_port):
    # 创建一个socket连接到算力网关
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((gateway_ip, gateway_port))

    # 模拟算力资源信息
    cpu = random.randint(1, 8)  # 随机生成计算资源
    memory = random.randint(4, 32)  # 随机生成内存资源
    
    # 向算力网关发送资源信息
    message = f"Node {node_id} Resources: CPU={cpu} cores, Memory={memory} GB"
    sock.sendall(message.encode())

    print(f"Node {node_id} sent resources to gateway.")
    
    # 关闭连接
    time.sleep(2)
    sock.close()

# 启动多个算力节点线程
def start_nodes(gateway_ip, gateway_port, num_nodes=3):
    threads = []
    for i in range(num_nodes):
        t = threading.Thread(target=compute_node, args=(i, gateway_ip, gateway_port))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()


def main():
    gateway_port = 5000
    # 启动算力网关
    gateway_thread = threading.Thread(target=start_gateway, args=(1, gateway_port))
    gateway_thread.start()

    time.sleep(1)  # 等待网关启动完成

    # 启动多个算力节点
    start_nodes('localhost', gateway_port)

    # 启动用户请求
    start_user('localhost', gateway_port)

    gateway_thread.join()

if __name__ == '__main__':
    main()
