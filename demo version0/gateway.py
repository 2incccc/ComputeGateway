import socket
import threading
import random

# 模拟算力网关
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

    def compute_aggregation_layer(self):
        # 计算聚合节点（例如，选择资源最多的两个节点）
        if len(self.nodes) > 0:
            # 假设根据节点信息中的内存和CPU选择最优节点
            sorted_nodes = sorted(self.nodes, key=lambda x: (int(x.split('=')[1].split()[0]), int(x.split('=')[2].split()[0])), reverse=True)
            self.aggregation_layer = sorted_nodes[:2]  # 选择最优的两个节点
            print(f"Gateway {self.gateway_id} Aggregation Layer: {self.aggregation_layer}")
        else:
            self.aggregation_layer = []
        
# 启动网关
def start_gateway(gateway_id, port):
    gateway = ComputeGateway(gateway_id, port)
    gateway.start()

