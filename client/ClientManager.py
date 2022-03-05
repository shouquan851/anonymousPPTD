import time

import params
from utils.Encrypt import Encrypt


class ClientManager:
    public_key_client_list = list()
    private_key_client_list = list()
    aes_key_list_all_group = list()
    client_data_all_group = list()

    def __init__(self):
        print("init ClientManager")

    def generate_dh_key(self, client_count):
        encrypt = Encrypt()
        public_key_list = list()
        private_key_list = list()
        for i in range(client_count):
            private_key, public_key = encrypt.generate_dh_key()
            public_key_list.append(public_key)
            private_key_list.append(private_key)
        self.public_key_client_list = public_key_list
        self.private_key_client_list = private_key_list

    def generate_aes_key(self):
        encrypt = Encrypt()
        # 为每个组内的所有用户和其他所有用户协商对称密钥
        count = 0  # 已处理过的组的用户数量
        group_index = 1
        aes_key_list_all_group = list()
        for groupNumber in params.group_number_list:
            aes_key_list_all_client = list()
            for client_pri_index in range(groupNumber):
                # 逐个处理每个用户
                aes_key_list_one_client = list()
                for client_pub_index in range(groupNumber):
                    # 生成对称密钥
                    aes_key = encrypt.generate_aes_key(self.private_key_client_list[count + client_pri_index],
                                                       self.public_key_client_list[count + client_pri_index],
                                                       self.public_key_client_list[count + client_pub_index])
                    aes_key_list_one_client.append(aes_key)
                aes_key_list_all_client.append(aes_key_list_one_client)
            aes_key_list_all_group.append(aes_key_list_all_client)
            count += groupNumber
            print("第%d组处理完毕,已处理%d个用户" % (group_index, count))
        self.aes_key_list_all_group = aes_key_list_all_group

    def load_data(self, client_data):
        '''
        把生成的整个系统的用户数据切分给到各个组的用户中去
        :param client_data:整个系统的用户数据
        :return:
        '''
        count = 0
        for group_index in range(len(params.group_number_list)):
            client_data_one_group = list()
            for client_index_in_group in range(params.group_number_list[group_index]):
                client_data_one_group.append(client_data[count + client_index_in_group])
            self.client_data_all_group.append(client_data_one_group)
            count += params.group_number_list[group_index]

    def generate_update_data(self, add_noise_index_all_group):
        '''
        根据数据添加位置,生成处理过的数据
        :param add_noise_index_all_group:
        :return:
        '''
        if len(self.client_data_all_group) == 0:
            print("还未加载数据")
            return
        client_masking_data_all_group = list()
        # 逐个处理每个组
        for group_index in range(len(self.client_data_all_group)):
            client_masking_data_one_group = list()
            # 逐个处理组内每个用户的数据
            for client_index in range(len(self.client_data_all_group[group_index])):
                client_masking_data_one = list()
                # 逐个处理每个用户的每个任务
                for m in range(params.M):
                    client_masking_data_one_task = list()
                    # 逐个处理每个任务的数据
                    for data_index in range(len(self.client_data_all_group[group_index])):
                        # 当前位置是用户添加数据的位置,就添加数据,否则就只添加噪声000000
                        if data_index != add_noise_index_all_group[group_index][client_index]:
                            client_masking_data_one_task.append(10000000)
                        else:
                            client_masking_data_one_task.append(
                                10000000 + self.client_data_all_group[group_index][client_index][m])
                    # 把该任务处理后的数据添加进去
                    client_masking_data_one.append(client_masking_data_one_task)
                # 把单个用户的数据添加到组内
                client_masking_data_one_group.append(client_masking_data_one)
            # 把单组用户的数据添加到所有组的数据中
            client_masking_data_all_group.append(client_masking_data_one_group)
        return client_masking_data_all_group

# 打印密钥交换结果
# for aes_key_list_one_group in aes_key_list_all_group:
#     for aes_key_list_one_client in aes_key_list_one_group:
#         print(aes_key_list_one_client)

# encrypt = Encrypt()
# ct = Encrypt.aes_encryptor(aes_key_list_all_client[0][1], b"a" * 16)
# dt = Encrypt.aes_decryptor(aes_key_list_all_client[1][0], ct)
# print(dt)
