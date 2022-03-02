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
    public_key_client_list, private_key_list = ClientManager.generate_dh_key(int(params.client_number))
    aes_key_list_all_client = ClientManager.generate_aes_key(public_key_client_list, private_key_list)
    # 边缘节点生成dh密钥，并相互生成aes密钥
    public_key_edge_list, private_key_list = EdgeManager.generate_dh_key(int(params.edge_number))
    aes_key_list_all_edge = EdgeManager.generate_aes_key(public_key_edge_list, private_key_list)
    # 云中心生成dh密钥，并和用户相互生成aes密钥
    cloudServer.generate_dh_key()
    cloudServer.generate_aes_key(public_key_client_list)


key_agreement()
for aes_key in cloudServer.aes_key_list_with_client:
    print(aes_key)
