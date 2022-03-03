import time

import params
from client.ClientManager import ClientManager
from cloud_server.CloudServer import CloudServer
from data_generator.DataGenerator import DataGenerator
from edge_server.EdgeManager import EdgeManager

# if __name__ == '__main__':
#     print('PyCharm')

clientManager = ClientManager()
edgeManager = EdgeManager()
cloudServer = CloudServer()
dataGenerator = DataGenerator()


def key_agreement():
    # 用户生成dh密钥，并相互生成aes密钥
    # start = round(time.time()*1000)# 返回当前时间戳 ms级别
    start = time.perf_counter()  # 返回性能计数器的值（以小数秒为单位）作为浮点数
    clientManager.generate_dh_key(int(params.client_number))
    end = time.perf_counter()
    print("为所有用户生成DH密钥用时%d" % (end - start))
    start = time.perf_counter()
    clientManager.generate_aes_key()
    end = time.perf_counter()
    print("为所有用户协商对称密钥用时%d" % (end - start))
    # 边缘节点生成dh密钥，并相互生成aes密钥
    start = time.perf_counter()
    edgeManager.generate_dh_key(int(params.edge_number))
    end = time.perf_counter()
    print("为所有边缘节点生成DH密钥用时%d" % (end - start))
    start = time.perf_counter()
    edgeManager.generate_aes_key()
    end = time.perf_counter()
    print("为所有边缘节点生成协商对称密钥用时%d" % (end - start))
    # 云中心生成dh密钥，并和用户相互生成aes密钥
    cloudServer.generate_dh_key()
    start = time.perf_counter()
    cloudServer.generate_aes_key(clientManager.public_key_client_list)
    end = time.perf_counter()
    print("为所有用户和云中心协商对称密钥用时%d" % (end - start))


# key_agreement()
# print(clientManager.aes_key_list_all_group)
# print(edgeManager.aes_key_list_all_edge)

# 生成整个系统的用户数据
dataGenerator.generate_base_data(10, 0, 100, 80)
client_data = dataGenerator.generate_client_data()
for client_data_one in client_data:
    print(client_data_one)
# 将用户数据加载到clientManager中
clientManager.load_data(client_data)
index = 1
# 打印用户数据
for client_data_one_group in clientManager.client_data_all_group:
    print("第%d组" % index)
    index += 1
    for client_data_one in client_data_one_group:
        print(client_data_one)
