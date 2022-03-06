import params
from utils.Encrypt import Encrypt
from utils.TD_CRH import TD_CRH


class CloudServer:
    private_server_key = None
    public_server_key = None
    aes_key_list_with_client = None
    anonymous_all_client_data = list()
    td_result = list()

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
                anonymous_one_client_data.append(temp)
            self.anonymous_all_client_data.append(anonymous_one_client_data)

    def td_in_anonymous_data(self, anonymous_all_client_data):
        td_CRH = TD_CRH(anonymous_all_client_data, params.K, params.M)
        td_CRH.TD(params.count)
        self.td_result = td_CRH.xm_i[params.count]
