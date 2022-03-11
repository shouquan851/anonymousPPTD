import params
from AnonyMousePPTD.AnonyMousePPTD import AnonyMousePPTD
from AnonymousEdgePPTD import AnonymousEdgePPTD


def run_once():
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
    client_masking_data_all_group = anonymousEdgePPTD.client_upload_data(all_group_in_client_data_index,
                                                                         de_all_group_client_data_index)  # 生成要上传的数据

    data_miss_list_all_group = anonymousEdgePPTD.generate_data_miss_list(params.miss_rate)
    client_encrypt_ru_all_group = anonymousEdgePPTD.clientManager.client_encrypt_ru_all_group
    # 边缘节点聚合客户端数据
    anonymousEdgePPTD.edge_aggregation_client_data(client_masking_data_all_group, data_miss_list_all_group)
    # 云中心生成hash噪声
    hash_noise_others_group = anonymousEdgePPTD.cloud_server_generate_hash_noise(client_encrypt_ru_all_group,
                                                                                 data_miss_list_all_group)
    # 边缘节点添加云中心回馈的noise后上传数据,生成masking噪声并处理用户数据后上传
    edge_masking_data_all_group = anonymousEdgePPTD.edge_generate_edge_masking_data_all_group(hash_noise_others_group,
                                                                                              2)
    # 云中心聚合数据
    anonymous_all_client_data = anonymousEdgePPTD.cloud_server_aggregation_edge_masking_data(
        edge_masking_data_all_group)
    # 云中心执行TD
    td_result_anonymous_all_client_data = anonymousEdgePPTD.cloud_server_TD(anonymous_all_client_data)
    print("真值发现结果")
    print(td_result_anonymous_all_client_data)
    # 对原始数据做TD,和匿名后云中心做TD进行比较
    td_result_original_data = anonymousEdgePPTD.original_data_TD(anonymousEdgePPTD.dataGenerator.all_client_data)
    print("原始数据真值发现结果")
    print(td_result_original_data)

    # 执行对比方案
    print("************************************************************************")
    print("执行对比方案")
    # 初始化
    anonyMousePPTD = AnonyMousePPTD()
    # DR生成有各个用户的随机数种子，以及数据添加位置
    seed_list, all_data_index_list = anonyMousePPTD.DR_init()
    anonyMousePPTD.client_init(seed_list, all_data_index_list)
    all_client_masking_data = anonyMousePPTD.client_upload_data_(anonymousEdgePPTD.dataGenerator.all_client_data)
    anonymous_all_client_data = anonyMousePPTD.as_aggregation_masking_data(all_client_masking_data,data_miss_list_all_group)
    td_result_anonymous_all_client_data = anonyMousePPTD.as_td(anonymous_all_client_data)
    print("真值发现结果")
    print(td_result_anonymous_all_client_data)


def run_test():
    # 初始化本方案和对比方案
    anonymousEdgePPTD = AnonymousEdgePPTD()
    anonyMousePPTD = AnonyMousePPTD()
    # 本方案密钥和随机种子协商
    anonymousEdgePPTD.key_agreement()
    # 对比方案生成各个用户的随机数种子，以及数据添加位置
    seed_list, all_data_index_list = anonyMousePPTD.DR_init()
    anonyMousePPTD.client_init(seed_list, all_data_index_list)

    # 系统生成数据
    anonymousEdgePPTD.data_generator()

    # 边缘节点之间协商数据上传位置
    all_group_in_client_data_index = anonymousEdgePPTD.generate_data_index(params.select_index)  # 组内数据添加位置
    de_all_group_client_data_index = anonymousEdgePPTD.edgeManager.de_all_group_client_data_index  # 整体数据添加位置
    # 客户端上传数据
    client_masking_data_all_group = anonymousEdgePPTD.client_upload_data(all_group_in_client_data_index,
                                                                         de_all_group_client_data_index)  # 生成要上传的数据
    # 边缘节点聚合客户端数据
    anonymousEdgePPTD.edge_aggregation_client_data(client_masking_data_all_group)
    # 云中心生成hash噪声
    hash_noise_others_group = anonymousEdgePPTD.cloud_server_generate_hash_noise(client_ru_all_group)
    # 边缘节点添加云中心回馈的noise后上传数据,生成masking噪声并处理用户数据后上传
    edge_masking_data_all_group = anonymousEdgePPTD.edge_generate_edge_masking_data_all_group(hash_noise_others_group,
                                                                                              2)
    # 云中心聚合数据
    anonymous_all_client_data = anonymousEdgePPTD.cloud_server_aggregation_edge_masking_data(
        edge_masking_data_all_group)
    # 云中心执行TD
    td_result_anonymous_all_client_data = anonymousEdgePPTD.cloud_server_TD(anonymous_all_client_data)
    print("真值发现结果")
    print(td_result_anonymous_all_client_data)
    # 对原始数据做TD,和匿名后云中心做TD进行比较
    # td_result_original_data = anonymousEdgePPTD.original_data_TD(anonymousEdgePPTD.dataGenerator.all_client_data)
    # print(td_result_original_data)

    # 执行对比方案
    print("************************************************************************")
    print("执行对比方案")

    all_client_masking_data = anonyMousePPTD.client_upload_data_(anonymousEdgePPTD.dataGenerator.all_client_data)
    anonymous_all_client_data = anonyMousePPTD.as_aggregation_masking_data(all_client_masking_data)
    td_result_anonymous_all_client_data = anonyMousePPTD.as_td(anonymous_all_client_data)
    print("真值发现结果")
    print(td_result_anonymous_all_client_data)


run_once()
# run_test()
