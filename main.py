import params
from AnonyMousePPTD.AnonyMousePPTD import AnonyMousePPTD
from AnonymousEdgePPTD import AnonymousEdgePPTD
from utils.TestUtils import TestUtils


def run_once():
    # 初始化
    anonymousEdgePPTD = AnonymousEdgePPTD()
    # 密钥和随机种子协商
    anonymousEdgePPTD.key_agreement()
    # 生成数据
    anonymousEdgePPTD.data_generator()

    # 添加极端值
    anonymousEdgePPTD.generate_extreme_data_index(params.K, params.M, params.extreme_client_rate,
                                                  params.extreme_task_rate)
    anonymousEdgePPTD.add_extreme_data()

    # 边缘节点之间协商数据上传位置
    all_group_in_client_data_index = anonymousEdgePPTD.generate_data_index(params.select_index)  # 组内数据添加位置
    de_all_group_client_data_index = anonymousEdgePPTD.edgeManager.de_all_group_client_data_index  # 整体数据添加位置

    # 客户端加载数据
    anonymousEdgePPTD.client_load_data(anonymousEdgePPTD.all_client_data)
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
        edge_masking_data_all_group, anonymousEdgePPTD.data_section)

    print("***********************************************************************")
    print("开始进行真值发现")
    # 对原始数据做TD
    td_result_original_data = anonymousEdgePPTD.original_data_TD(anonymousEdgePPTD.origin_client_data)
    print("原始数据真值发现结果")
    print(td_result_original_data)
    print("直接TD的RMSE = %f" % (TestUtils.get_RMSE(td_result_original_data, anonymousEdgePPTD.base_data_list)))

    # 对有离群值数据做TD
    td_result_original_data = anonymousEdgePPTD.original_data_TD(anonymousEdgePPTD.all_client_data)
    print("有离群值数据直接真值发现结果")
    print(td_result_original_data)
    print("直接TD的RMSE = %f" % (TestUtils.get_RMSE(td_result_original_data, anonymousEdgePPTD.base_data_list)))

    # 云中心执行TD
    print("************************************************************************")
    print("云中心TD")
    td_result_anonymous_all_client_data = anonymousEdgePPTD.cloud_server_TD(anonymous_all_client_data)
    print("真值发现结果")
    print(td_result_anonymous_all_client_data)
    print("本方案RMSE = %f" % (TestUtils.get_RMSE(td_result_anonymous_all_client_data, anonymousEdgePPTD.base_data_list)))

    # 执行对比方案
    print("************************************************************************")
    print("执行对比方案")
    # 初始化
    anonyMousePPTD = AnonyMousePPTD()
    # DR生成有各个用户的随机数种子，以及数据添加位置
    seed_list, all_data_index_list = anonyMousePPTD.DR_init()
    anonyMousePPTD.client_init(seed_list, all_data_index_list)
    all_client_masking_data = anonyMousePPTD.client_upload_data_(anonymousEdgePPTD.all_client_data)
    anonymous_all_client_data = anonyMousePPTD.as_aggregation_masking_data(all_client_masking_data,
                                                                           data_miss_list_all_group,
                                                                           anonymousEdgePPTD.data_section)
    td_result_anonymous_all_client_data = anonyMousePPTD.as_td(anonymous_all_client_data)
    print("真值发现结果")
    print(td_result_anonymous_all_client_data)
    print("对比方案RMSE = %f" % (TestUtils.get_RMSE(td_result_anonymous_all_client_data, anonymousEdgePPTD.base_data_list)))

    print("****************************************************************")
    print("本方案运行时间")
    print("one client_time = %f" % (anonymousEdgePPTD.clientManager.all_client_time / params.client_number))
    print("index_edge_time:")
    print(anonymousEdgePPTD.edgeManager.index_edge_time)
    print("aggregation_and_upload_edge_time:")
    print(anonymousEdgePPTD.edgeManager.aggregation_and_upload_edge_time)
    print(
        "cloud_server_aggreate_time=%f,cloud_server_generate_hash_noise_time=%f" % (
            anonymousEdgePPTD.cloudServer.cloud_server_aggreate_time,
            anonymousEdgePPTD.cloudServer.cloud_server_generate_hash_noise_time))

    print("对比方案运行时间")
    print("one client_time = %f" % (anonyMousePPTD.client_manager.all_client_time / params.client_number))
    print("cloud_server_aggreate_time=%f" % (anonyMousePPTD.AS.cloud_server_aggreate_time))


def run_test_computation():
    params.K = 0
    test_result_list = list()
    test_result_list.append(
        ["K", "ODPPTD_one_client_time", "ODPPTD_index_edge_time", "ODPPTD_aggregation_and_upload_edge_time",
         "ODPPTD_cloud_server_aggreate_time", "ODPPTD_cloud_server_generate_hash_noise_time",
         "one_client_time", "cloud_server_aggreate_time"])
    for i in range(10):
        print("开始第%d轮：-------------------------" % (i))
        # 初始化参数
        params.K += 100
        params.client_number = params.K
        params.group_number_list = list()
        for edge_index in range(params.edge_number):
            params.group_number_list.append(int(params.K / params.edge_number))

        # 初始化
        anonymousEdgePPTD = AnonymousEdgePPTD()
        # 密钥和随机种子协商
        anonymousEdgePPTD.key_agreement()
        # 生成数据
        anonymousEdgePPTD.data_generator()

        # 添加极端值
        anonymousEdgePPTD.generate_extreme_data_index(params.K, params.M, params.extreme_client_rate,
                                                      params.extreme_task_rate)
        anonymousEdgePPTD.add_extreme_data()

        # 边缘节点之间协商数据上传位置
        all_group_in_client_data_index = anonymousEdgePPTD.generate_data_index(params.select_index)  # 组内数据添加位置
        de_all_group_client_data_index = anonymousEdgePPTD.edgeManager.de_all_group_client_data_index  # 整体数据添加位置

        # 客户端加载数据
        anonymousEdgePPTD.client_load_data(anonymousEdgePPTD.all_client_data)
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
        edge_masking_data_all_group = anonymousEdgePPTD.edge_generate_edge_masking_data_all_group(
            hash_noise_others_group,
            2)
        # 云中心聚合数据
        anonymous_all_client_data = anonymousEdgePPTD.cloud_server_aggregation_edge_masking_data(
            edge_masking_data_all_group, anonymousEdgePPTD.data_section)

        print("***********************************************************************")
        print("开始进行真值发现")
        # 对原始数据做TD
        td_result_original_data = anonymousEdgePPTD.original_data_TD(anonymousEdgePPTD.origin_client_data)
        print("原始数据真值发现结果")
        print(td_result_original_data)
        print("直接TD的RMSE = %f" % (TestUtils.get_RMSE(td_result_original_data, anonymousEdgePPTD.base_data_list)))

        # 对有离群值数据做TD
        # td_result_original_data = anonymousEdgePPTD.original_data_TD(anonymousEdgePPTD.all_client_data)
        # print("有离群值数据直接真值发现结果")
        # print(td_result_original_data)
        # print("直接TD的RMSE = %f" % (TestUtils.get_RMSE(td_result_original_data, anonymousEdgePPTD.base_data_list)))

        # 云中心执行TD
        print("云中心TD")
        td_result_anonymous_all_client_data = anonymousEdgePPTD.cloud_server_TD(anonymous_all_client_data)
        print("真值发现结果")
        print(td_result_anonymous_all_client_data)
        print("本方案RMSE = %f" % (
            TestUtils.get_RMSE(td_result_anonymous_all_client_data, anonymousEdgePPTD.base_data_list)))

        # 执行对比方案
        print("************************************************************************")
        print("执行对比方案")
        # 初始化
        anonyMousePPTD = AnonyMousePPTD()
        # DR生成有各个用户的随机数种子，以及数据添加位置
        seed_list, all_data_index_list = anonyMousePPTD.DR_init()
        anonyMousePPTD.client_init(seed_list, all_data_index_list)
        all_client_masking_data = anonyMousePPTD.client_upload_data_(anonymousEdgePPTD.all_client_data)
        anonymous_all_client_data = anonyMousePPTD.as_aggregation_masking_data(all_client_masking_data,
                                                                               data_miss_list_all_group,
                                                                               anonymousEdgePPTD.data_section)
        td_result_anonymous_all_client_data = anonyMousePPTD.as_td(anonymous_all_client_data)
        print("真值发现结果")
        print(td_result_anonymous_all_client_data)
        print("对比方案RMSE = %f" % (
            TestUtils.get_RMSE(td_result_anonymous_all_client_data, anonymousEdgePPTD.base_data_list)))

        print("***********************计算开销******************************")

        print("边缘节点个数:%d,用户个数:%d" % (params.edge_number, params.K))
        print("本方案运行时间")
        print("one_client_time = %f" % (anonymousEdgePPTD.clientManager.all_client_time / params.client_number))
        print("index_edge_time:")
        print(anonymousEdgePPTD.edgeManager.index_edge_time)
        print("aggregation_and_upload_edge_time:")
        print(anonymousEdgePPTD.edgeManager.aggregation_and_upload_edge_time)
        print(
            "cloud_server_aggreate_time=%f,cloud_server_generate_hash_noise_time=%f" % (
                anonymousEdgePPTD.cloudServer.cloud_server_aggreate_time,
                anonymousEdgePPTD.cloudServer.cloud_server_generate_hash_noise_time))

        print("对比方案运行时间")
        print("one client_time = %f" % (anonyMousePPTD.client_manager.all_client_time / params.client_number))
        print("cloud_server_aggreate_time=%f" % anonyMousePPTD.AS.cloud_server_aggreate_time)

        test_result_list.append([params.K, anonymousEdgePPTD.clientManager.all_client_time / params.client_number,
                                 anonymousEdgePPTD.edgeManager.index_edge_time[0],
                                 anonymousEdgePPTD.edgeManager.aggregation_and_upload_edge_time[0],
                                 anonymousEdgePPTD.cloudServer.cloud_server_aggreate_time,
                                 anonymousEdgePPTD.cloudServer.cloud_server_generate_hash_noise_time,
                                 anonyMousePPTD.client_manager.all_client_time / params.client_number,
                                 anonyMousePPTD.AS.cloud_server_aggreate_time])
    TestUtils.write_csv("D:/workPlace/researchRecord/anonymousPPTD/testResult/", "test_computation_result.csv",
                        test_result_list)


# run_once()
run_test_computation()
