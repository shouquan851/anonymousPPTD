import params
from utils.TD_CRH import TD_CRH


class AS:
    anonymous_all_client_data = list()

    def __init__(self):
        pass

    def aggregation_masking_data_all_client(self, all_client_masking_data, data_miss_list_all_group):
        """
        中心服务器聚合用户数据
        :param all_client_masking_data:
        :return:
        """
        data_miss_list = list()
        count = 0
        for edge_index in range(len(data_miss_list_all_group)):
            for miss_index in data_miss_list_all_group[edge_index]:
                data_miss_list.append(count + miss_index)
            count += params.group_number_list[edge_index]

        for k in range(params.K):
            anonymous_one_client_data = list()
            for m in range(params.M):
                temp = 0
                for j in range(params.K):
                    if j not in data_miss_list:
                        temp += all_client_masking_data[j][m][k]
                anonymous_one_client_data.append(temp)
            self.anonymous_all_client_data.append(anonymous_one_client_data)

    def detection_extreme_data(self, data_section):
        extreme_data_list = list()
        for k in range(len(self.anonymous_all_client_data)):
            for m in range(params.M):
                if self.anonymous_all_client_data[k][m] == 0:
                    extreme_data_list.append(self.anonymous_all_client_data[k])
                    break
                if params.extreme_detection_flag_:
                    if self.anonymous_all_client_data[k][m] < data_section[m][0] or data_section[m][1] < \
                            self.anonymous_all_client_data[k][m]:
                        extreme_data_list.append(self.anonymous_all_client_data[k])
                        break
        for extreme_data in extreme_data_list:
            self.anonymous_all_client_data.remove(extreme_data)

    def td_in_anonymous_data(self, anonymous_all_client_data):
        """
        对匿名数据执行真值发现
        :param anonymous_all_client_data:
        :return:
        """

        td_CRH = TD_CRH(anonymous_all_client_data, len(anonymous_all_client_data), len(anonymous_all_client_data[0]))
        td_CRH.TD(params.count)
        self.td_result = td_CRH.xm_i[params.count]
