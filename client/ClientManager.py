import time

import params
from utils.Encrypt import Encrypt


class ClientManager:
    def __init__(self):
        print("init ClientManager")

    @staticmethod
    def generate_dh_key(client_count):
        encrypt = Encrypt()
        public_key_list = list()
        private_key_list = list()
        for i in range(client_count):
            private_key, public_key = encrypt.generate_dh_key()
            public_key_list.append(public_key)
            private_key_list.append(private_key)
        return public_key_list, private_key_list

    @staticmethod
    def generate_aes_key(public_key_list, private_key_list):
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
                    aes_key = encrypt.generate_aes_key(private_key_list[count + client_pri_index],
                                                       public_key_list[count + client_pri_index],
                                                       public_key_list[count + client_pub_index])
                    aes_key_list_one_client.append(aes_key)
                aes_key_list_all_client.append(aes_key_list_one_client)
            aes_key_list_all_group.append(aes_key_list_all_client)
            count += groupNumber
            print("第%d组处理完毕,已处理%d个用户" % (group_index, count))
        return aes_key_list_all_group


start = time.perf_counter()
public_key_list, private_key_list = ClientManager.generate_dh_key(int(params.client_number))
end = time.perf_counter()
print("为所有用户生成密钥用时%d" % (end - start))

start = time.perf_counter()
aes_key_list_all_group = ClientManager.generate_aes_key(public_key_list, private_key_list)
end = time.perf_counter()
print("为所有用户交换密钥用时%d" % (end - start))

# 打印密钥交换结果
# for aes_key_list_one_group in aes_key_list_all_group:
#     for aes_key_list_one_client in aes_key_list_one_group:
#         print(aes_key_list_one_client)

# encrypt = Encrypt()
# ct = Encrypt.aes_encryptor(aes_key_list_all_client[0][1], b"a" * 16)
# dt = Encrypt.aes_decryptor(aes_key_list_all_client[1][0], ct)
# print(dt)
