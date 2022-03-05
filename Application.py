import time

import params
from client.ClientManager import ClientManager
from cloud_server.CloudServer import CloudServer
from data_generator.DataGenerator import DataGenerator
from edge_server.EdgeManager import EdgeManager


class Application:
    clientManager = None
    edgeManager = None
    cloudServer = None
    dataGenerator = None

    def __init__(self):
        self.clientManager = ClientManager()
        self.edgeManager = EdgeManager()
        self.cloudServer = CloudServer()
        self.dataGenerator = DataGenerator()
        print("init Application")

    def key_agreement(self):
        # 用户生成dh密钥，并相互生成aes密钥
        # start = round(time.time()*1000)# 返回当前时间戳 ms级别
        start = time.perf_counter()  # 返回性能计数器的值（以小数秒为单位）作为浮点数
        self.clientManager.generate_dh_key(int(params.client_number))
        end = time.perf_counter()
        print("为所有用户生成DH密钥用时%d" % (end - start))
        start = time.perf_counter()
        self.clientManager.generate_aes_key()
        end = time.perf_counter()
        print("为所有用户协商对称密钥用时%d" % (end - start))
        # 边缘节点生成dh密钥，并相互生成aes密钥
        start = time.perf_counter()
        self.edgeManager.generate_dh_key(int(params.edge_number))
        end = time.perf_counter()
        print("为所有边缘节点生成DH密钥用时%d" % (end - start))
        start = time.perf_counter()
        self.edgeManager.generate_aes_key()
        end = time.perf_counter()
        print("为所有边缘节点生成协商对称密钥用时%d" % (end - start))
        # 云中心生成dh密钥，并和用户相互生成aes密钥
        self.cloudServer.generate_dh_key()
        start = time.perf_counter()
        self.cloudServer.generate_aes_key(self.clientManager.public_key_client_list)
        end = time.perf_counter()
        print("为所有用户和云中心协商对称密钥用时%d" % (end - start))

    def data_generator(self):
        # 生成整个系统的用户数据
        self.dataGenerator.generate_base_data(10, 0, 100, 80)
        client_data = self.dataGenerator.generate_client_data()
        for client_data_one in client_data:
            print(client_data_one)
        # 将用户数据加载到clientManager中
        self.clientManager.load_data(client_data)
        index = 1
        # 打印用户数据
        for client_data_one_group in self.clientManager.client_data_all_group:
            print("第%d组" % index)
            index += 1
            for client_data_one in client_data_one_group:
                print(client_data_one)

    def generate_data_index(self, edge_index):
        '''
        边缘节点协商数据添加位置
        :param edge_index: 云中心选的边缘服务器
        :return:
        '''
        self.edgeManager.generate_en_client_data_index()
        self.edgeManager.generate_de_group_client_data_index(edge_index,
                                                             self.edgeManager.en_all_edge_client_data_index[edge_index])
        print(self.edgeManager.de_one_group_client_data_index)
        # 各个边缘节点生成组内用户数据添加位置
        self.edgeManager.generate_in_group_client_data_index()
        print(self.edgeManager.all_group_in_client_data_index)
        return self.edgeManager.all_group_in_client_data_index

    def client_upload_data(self, all_group_in_client_data_index):
        # 根据数据添加位置处理用户数据
        return self.clientManager.generate_update_data(all_group_in_client_data_index)
