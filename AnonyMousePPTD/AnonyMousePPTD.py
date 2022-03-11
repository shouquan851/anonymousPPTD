from AnonyMousePPTD.AS import AS
from AnonyMousePPTD.ClientManage import ClientManage
from AnonyMousePPTD.DR import DR
from data_generator.DataGenerator import DataGenerator


class AnonyMousePPTD:
    DR = None
    client_manager = None
    AS = None
    dataGenerator = None

    def __init__(self):
        self.DR = DR()
        self.client_manager = ClientManage()
        self.AS = AS()
        self.dataGenerator = DataGenerator()
        print("init AnonyMousePPTD")

    def DR_init(self):
        self.DR.generate_seed()
        self.DR.generate_data_index()
        return self.DR.seed_list, self.DR.all_data_index_list

    def client_init(self, seed_list, all_data_index_list):
        self.client_manager.load_seed_and_data_index(seed_list, all_data_index_list)

    def data_generator_init(self):
        # 生成整个系统的用户数据
        self.dataGenerator.generate_base_data(10, 0, 100, 99)
        # 打印basedata
        print("basedata")
        print(self.dataGenerator.base_data)

    def client_upload_data(self):
        self.data_generator_init()
        self.client_manager.load_data(self.dataGenerator.generate_client_data())
        self.client_manager.generate_noise(2)
        # self.client_manager.verify_noise_data()
        self.client_manager.generate_masking_data()
        return self.client_manager.all_client_masking_data

    def client_upload_data_(self, all_client_data):
        self.client_manager.load_data(all_client_data)
        self.client_manager.generate_noise(2)
        # self.client_manager.verify_noise_data()
        self.client_manager.generate_masking_data()
        return self.client_manager.all_client_masking_data

    def as_aggregation_masking_data(self, all_client_masking_data, data_miss_list_all_group):
        self.AS.aggregation_masking_data_all_client(all_client_masking_data, data_miss_list_all_group)
        return self.AS.anonymous_all_client_data

    def as_td(self, anonymous_all_client_data):
        self.AS.td_in_anonymous_data(anonymous_all_client_data)
        return self.AS.td_result
