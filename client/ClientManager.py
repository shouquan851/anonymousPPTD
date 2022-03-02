from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

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
        # print(private_key_list)
        # print(public_key_list)
        return public_key_list, private_key_list

    @staticmethod
    def generate_aes_key(public_key_list, private_key_list):
        encrypt = Encrypt()
        # 为每个组内的所有用户和其他所有用户协商对称密钥
        count = 0 # 已处理过的组的用户数量
        aes_key_list_all_group = list()
        for groupNumber in params.group_number_list:
            aes_key_list_all_client = list()
            for client_pri_index in range(groupNumber):
                # 逐个处理每个用户
                aes_key_list_one_client = list()
                for client_pub_index in range(groupNumber):
                    # 生成对称密钥
                    aes_key = encrypt.generate_aes_key(private_key_list[count + client_pri_index], public_key_list[count + client_pri_index],
                                                       public_key_list[count + client_pub_index])
                    aes_key_list_one_client.append(aes_key)
                aes_key_list_all_client.append(aes_key_list_one_client)
            count += groupNumber
            aes_key_list_all_client.append(aes_key_list_one_client)
        aes_key_list_all_group.append(aes_key_list_all_client)
        return aes_key_list_all_group


public_key_list, private_key_list = ClientManager.generate_dh_key(int(params.client_number))
aes_key_list_all_group = ClientManager.generate_aes_key(public_key_list, private_key_list)
print(aes_key_list_all_group)
# encrypt = Encrypt()
# ct = Encrypt.aes_encryptor(aes_key_list_all_client[0][1], b"a" * 16)
# dt = Encrypt.aes_decryptor(aes_key_list_all_client[1][0], ct)
# print(dt)
