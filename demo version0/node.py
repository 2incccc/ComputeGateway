import socket
import time
import threading
import random

# 模拟算力节点
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

