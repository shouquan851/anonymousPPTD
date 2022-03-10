import params
from utils.TD_CRH import TD_CRH


class AS:
    anonymous_all_client_data = list()

    def __init__(self):
        print("init AS")

    def aggregation_masking_data_all_client(self, all_client_masking_data):
        """
        中心服务器聚合用户数据
        :param all_client_masking_data:
        :return:
        """
        for k in range(params.K):
            anonymous_one_client_data = list()
            for m in range(params.M):
                temp = 0
                for j in range(params.K):
                    temp += all_client_masking_data[j][m][k]
                anonymous_one_client_data.append(temp)
            self.anonymous_all_client_data.append(anonymous_one_client_data)

    def td_in_anonymous_data(self, anonymous_all_client_data):
        """
        对匿名数据执行真值发现
        :param anonymous_all_client_data:
        :return:
        """
        td_CRH = TD_CRH(anonymous_all_client_data, params.K, params.M)
        td_CRH.TD(params.count)
        self.td_result = td_CRH.xm_i[params.count]
