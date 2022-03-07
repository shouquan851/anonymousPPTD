import copy

import params
from utils.Encrypt import Encrypt
from utils.TD_CRH import TD_CRH


class CloudServer:
    private_server_key = None
    public_server_key = None
    aes_key_list_with_client = None
    anonymous_all_client_data = list()
    td_result = list()
    hash_noise_all_group = list()
    hash_noise_others_group = list()
    hash_noise_index = list()

    def __init__(self):
        print("init CloudServer")

    def generate_dh_key(self):
        encrypt = Encrypt()
        self.private_server_key, self.public_server_key = encrypt.generate_dh_key()

    def generate_aes_key(self, public_key_client_list):
        aes_key_list_with_client = list()
        encrypt = Encrypt()
        for public_key_client in public_key_client_list:
            aes_key_list_with_client.append(
                encrypt.generate_aes_key(self.private_server_key, self.public_server_key, public_key_client))
        self.aes_key_list_with_client = aes_key_list_with_client

    def generate_hash_noise_all_group(self, client_ru_all_group):
        '''
        云中心生成hash噪声
        :param de_all_group_client_random_index:
        :param client_ru_all_group:
        :return:
        '''
        for edge_index in range(params.edge_number):
            hash_noise_one_group = list()
            for m in range(params.M):
                hash_noise_one_group_one_task = list()
                for k in range(params.K):
                    noise = 0
                    for edge_index2 in range(params.edge_number):
                        if edge_index != edge_index2:
                            for client_index in range(params.group_number_list[edge_index2]):
                                temp = client_ru_all_group[edge_index2][client_index] + k + m
                                noise += Encrypt.hash_random(temp)
                    hash_noise_one_group_one_task.append(noise)
                hash_noise_one_group.append(hash_noise_one_group_one_task)
            self.hash_noise_others_group.append(hash_noise_one_group)
        for m in range(params.M):
            hash_noise_all_group_one_task = list()
            for k in range(params.K):
                noise = 0
                for edge_index in range(params.edge_number):
                    for client_index in range(params.group_number_list[edge_index]):
                        temp = client_ru_all_group[edge_index][client_index] + k + m
                        noise += Encrypt.hash_random(temp)
                hash_noise_all_group_one_task.append(noise)
            self.hash_noise_all_group.append(hash_noise_all_group_one_task)

    def aggregate_edge_noise_index_all_group(self, edge_noise_index_all_group):
        for k in range(params.client_number):
            self.hash_noise_index.append(0)
        for k in range(params.client_number):
            for edge_index in range(params.edge_number):
                self.hash_noise_index[k] += edge_noise_index_all_group[edge_index][k]

    def aggregation_edge_masking_data_all_group(self, edge_masking_data_all_group):
        '''
        中心服务器聚合用户数据
        :param edge_masking_data_all_group:
        :return:
        '''
        for k in range(params.K):
            anonymous_one_client_data = list()
            for m in range(params.M):
                temp = 0
                for edge_index in range(params.edge_number):
                    temp += edge_masking_data_all_group[edge_index][m][k]
                temp -= self.hash_noise_all_group[m][self.hash_noise_index[k]]
                anonymous_one_client_data.append(temp)
            self.anonymous_all_client_data.append(anonymous_one_client_data)


    def td_in_anonymous_data(self, anonymous_all_client_data):
        td_CRH = TD_CRH(anonymous_all_client_data, params.K, params.M)
        td_CRH.TD(params.count)
        self.td_result = td_CRH.xm_i[params.count]
