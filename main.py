from Application import Application

# if __name__ == '__main__':
#     print('PyCharm')
# 初始化
application = Application()
# 密钥协商
application.key_agreement()
# 生成数据
application.data_generator()
# 生成数据上传位置
all_group_in_client_data_index = application.generate_data_index(2, 3)
de_all_group_client_random_index = application.edgeManager.de_all_group_client_random_index

# 客户端上传数据
client_ru_all_group = application.client_generate_ru()
client_masking_data_all_group = application.client_upload_data(all_group_in_client_data_index,
                                                               de_all_group_client_random_index)
# print(client_masking_data_all_group)
# 边缘节点聚合客户端数据
application.edge_aggregation_client_data(client_masking_data_all_group)

# 云中心生成hash噪声
hash_noise_others_group = application.cloud_server_generate_hash_noise(client_ru_all_group)

# 边缘节点上传数据
edge_masking_data_all_group = application.edge_generate_edge_masking_data_all_group(hash_noise_others_group)

# 云中心聚合数据
edge_noise_index_all_group = application.edgeManager.edge_noise_index_all_group
anonymous_all_client_data = application.cloud_server_aggregation_edge_masking_data(edge_masking_data_all_group,
                                                                                   edge_noise_index_all_group)
# 云中心执行TD
td_result_anonymous_all_client_data = application.cloud_server_TD(anonymous_all_client_data)
print(td_result_anonymous_all_client_data)
# 对原始数据做TD,和匿名后云中心做TD进行比较
td_result_original_data = Application.original_data_TD(application.dataGenerator.all_client_data)
print(td_result_original_data)
