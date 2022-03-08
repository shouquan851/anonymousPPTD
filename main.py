import params
from AnonymousEdgePPTD import AnonymousEdgePPTD

# if __name__ == '__main__':
#     print('PyCharm')
# 初始化
anonymousEdgePPTD = AnonymousEdgePPTD()

# 密钥和随机种子协商
anonymousEdgePPTD.key_agreement()

# 生成数据
anonymousEdgePPTD.data_generator()

# 边缘节点之间协商数据上传位置
all_group_in_client_data_index = anonymousEdgePPTD.generate_data_index(params.select_index)  # 组内数据添加位置
de_all_group_client_data_index = anonymousEdgePPTD.edgeManager.de_all_group_client_data_index  # 整体数据添加位置

# 客户端上传数据
client_ru_all_group = anonymousEdgePPTD.client_generate_ru()  # 客户端生成ru
client_masking_data_all_group = anonymousEdgePPTD.client_upload_data(all_group_in_client_data_index,
                                                                     de_all_group_client_data_index)  # 生成要上传的数据

# 边缘节点聚合客户端数据
anonymousEdgePPTD.edge_aggregation_client_data(client_masking_data_all_group)

# 云中心生成hash噪声
hash_noise_others_group = anonymousEdgePPTD.cloud_server_generate_hash_noise(client_ru_all_group)

# 边缘节点添加云中心回馈的noise后上传数据,生成masking噪声并处理用户数据后上传
edge_masking_data_all_group = anonymousEdgePPTD.edge_generate_edge_masking_data_all_group(hash_noise_others_group, 2)

# 云中心聚合数据
anonymous_all_client_data = anonymousEdgePPTD.cloud_server_aggregation_edge_masking_data(edge_masking_data_all_group)

# 云中心执行TD
td_result_anonymous_all_client_data = anonymousEdgePPTD.cloud_server_TD(anonymous_all_client_data)
print(td_result_anonymous_all_client_data)

# 对原始数据做TD,和匿名后云中心做TD进行比较
td_result_original_data = anonymousEdgePPTD.original_data_TD(anonymousEdgePPTD.dataGenerator.all_client_data)
print(td_result_original_data)
