import params
from utils.Encrypt import Encrypt


class EdgeManager:
    public_key_edge_list = list()
    private_key_edge_list = list()
    aes_key_list_all_edge = list()

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
                aes_key = encrypt.generate_aes_key(self.private_key_edge_list[edge_index], self.public_key_edge_list[edge_index],
                                                   public_key)
                aes_key_list_one_edge.append(aes_key)
            aes_key_list_all_edge.append(aes_key_list_one_edge)
        self.aes_key_list_all_edge = aes_key_list_all_edge

# if __name__ == '__main__':
#     print('PyCharm')
# public_key_list, private_key_list = EdgeManager.generate_dh_key(int(params.edge_number))
# aes_key_list_all_edge = EdgeManager.generate_aes_key(public_key_list, private_key_list)
# for aes_key_list_one_edge in aes_key_list_all_edge:
#     print(aes_key_list_one_edge)

# encrypt = Encrypt()
# ct = Encrypt.aes_encryptor(aes_key_list_all_edge[0][1], b"a" * 16)
# dt = Encrypt.aes_decryptor(aes_key_list_all_edge[1][0], ct)
# print(dt)
