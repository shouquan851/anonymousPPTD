import copy
import random

import params
from utils.Encrypt import Encrypt


class EdgeManager:
    public_key_edge_list = list()
    private_key_edge_list = list()
    aes_key_list_all_edge = list()
    en_all_edge_client_data_index = list()
    de_one_group_client_data_index = list()
    all_group_in_client_data_index = list()

    def __init__(self):
        print("init EdgeManager")

    def generate_dh_key(self, edge_count):
        encrypt = Encrypt()
        public_key_list = list()
        private_key_list = list()
        for i in range(edge_count):
            private_key, public_key = encrypt.generate_dh_key()
            public_key_list.append(public_key)
            private_key_list.append(private_key)
        self.public_key_edge_list = public_key_list
        self.private_key_edge_list = private_key_list

    def generate_aes_key(self):
        encrypt = Encrypt()
        # 为所有边缘节点和其他所有边缘节点协商对称密钥
        aes_key_list_all_edge = list()
        for edge_index in range(len(self.private_key_edge_list)):
            # 逐个处理每个边缘节点
            aes_key_list_one_edge = list()
            for public_key in self.public_key_edge_list:
                # 生成对称密钥
                aes_key = encrypt.generate_aes_key(self.private_key_edge_list[edge_index],
                                                   self.public_key_edge_list[edge_index],
                                                   public_key)
                aes_key_list_one_edge.append(aes_key)
            aes_key_list_all_edge.append(aes_key_list_one_edge)
        self.aes_key_list_all_edge = aes_key_list_all_edge

    def generate_en_client_data_index(self):
        all_edge_client_data_index = list()
        # 所有边缘节点生成初始的未加密的数据添加位置向量
        for edge_index in range(params.edge_number):
            one_edge_client_data_index = list()
            for k in range(params.K):
                one_edge_client_data_index.append(k)
            random.shuffle(one_edge_client_data_index)
            # print(one_edge_client_data_index)
            all_edge_client_data_index.append(one_edge_client_data_index)
        # 为所有边缘节点加密身生成的数据添加位置
        for edge_index1 in range(len(all_edge_client_data_index)):
            en_one_edge_client_data_index = bytes()
            one_edge_client_data_index = all_edge_client_data_index[edge_index1]
            start_index = 0
            end_index = 0
            # 对序列切分，并使用和不同节点共享的密钥加密
            for edge_index2 in range(len(params.group_number_list)):
                end_index += params.group_number_list[edge_index2]
                temp_list = copy.copy(one_edge_client_data_index[start_index:end_index])
                temp = Encrypt.aes_list_encryptor(self.aes_key_list_all_edge[edge_index1][edge_index2], temp_list)
                en_one_edge_client_data_index += temp
                start_index = end_index
            self.en_all_edge_client_data_index.append(en_one_edge_client_data_index)

    def generate_de_group_client_data_index(self, edge_en_index, en_list):
        '''
        节点解密收到的加密数据位置
        :param edge_en_index: 加密向量的节点的索引
        :param edge_de_index: 该解密节点的索引
        :param en_list: 收到的加密数据位置
        :return:
        '''
        start_index = 0
        end_index = 0
        for edge_index in range(params.edge_number):
            end_index += params.group_number_list[edge_index]
            temp_list = copy.copy(en_list[start_index:end_index])
            self.de_one_group_client_data_index.append(
                Encrypt.aes_list_decryptor(self.aes_key_list_all_edge[edge_index][edge_en_index], temp_list))
            start_index = end_index

    def generate_in_group_client_data_index(self):
        '''
        各个边缘节点为组内用户分配组内数据添加位置
        :return:
        '''
        for edge_index in range(params.edge_number):
            one_group_in_group_client_data_index = list()
            for i in range(params.group_number_list[edge_index]):
                one_group_in_group_client_data_index.append(i)
            random.shuffle(one_group_in_group_client_data_index)
            self.all_group_in_client_data_index.append(one_group_in_group_client_data_index)


if __name__ == '__main__':
    # 测试一下协商数据添加位置的方式
    edgeManager = EdgeManager()
    edgeManager.generate_dh_key(params.edge_number)
    edgeManager.generate_aes_key()
    edgeManager.generate_en_client_data_index()
    print(edgeManager.en_all_edge_client_data_index)
    edgeManager.generate_de_group_client_data_index(7, edgeManager.en_all_edge_client_data_index[7])
    print(edgeManager.de_one_group_client_data_index)
