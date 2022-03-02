import params
from utils.Encrypt import Encrypt


class EdgeManager:
    def __init__(self):
        print("init EdgeManager")

    @staticmethod
    def generate_dh_key(edge_count):
        encrypt = Encrypt()
        public_key_list = list()
        private_key_list = list()
        for i in range(edge_count):
            private_key, public_key = encrypt.generate_dh_key()
            public_key_list.append(public_key)
            private_key_list.append(private_key)
        # print(private_key_list)
        # print(public_key_list)
        return public_key_list, private_key_list

    @staticmethod
    def generate_aes_key(public_key_list, private_key_list):
        encrypt = Encrypt()
        # 为所有边缘节点和其他所有边缘节点协商对称密钥
        aes_key_list_all_edge = list()
        for edge_index in range(len(private_key_list)):
            # 逐个处理每个边缘节点
            aes_key_list_one_edge = list()
            for public_key in public_key_list:
                # 生成对称密钥
                aes_key = encrypt.generate_aes_key(private_key_list[edge_index], public_key_list[edge_index],
                                                   public_key)
                aes_key_list_one_edge.append(aes_key)
            aes_key_list_all_edge.append(aes_key_list_one_edge)
        return aes_key_list_all_edge


# if __name__ == '__main__':
#     print('PyCharm')
# public_key_list, private_key_list = EdgeManager.generate_dh_key(int(params.edgeNumber))
# aes_key_list_all_edge = EdgeManager.generate_aes_key(public_key_list, private_key_list)

# encrypt = Encrypt()
# ct = Encrypt.aes_encryptor(aes_key_list_all_edge[0][1], b"a" * 16)
# dt = Encrypt.aes_decryptor(aes_key_list_all_edge[1][0], ct)
# print(dt)
