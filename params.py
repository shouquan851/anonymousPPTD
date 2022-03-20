edge_number = 10
client_number = 1000
group_number_list = [100, 100, 100, 100, 100, 100, 100, 100, 100, 100]
# client_number = 100
# group_number_list = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10]

# datagenerate
# 可靠程度,越接近100 越可靠
base_data_rate = 1  # 随即生成地面真值之后乘以的倍数(更加分散)
base_data_start = 1  # 随机生成地面真值的起点
base_data_end = 1000  # 随机生成地面真值的终点
reliable_client_rate = 70  # 可靠用户的比例,0-100 越接近100 可靠用户越多
unreliable_start = 70
unreliable_end = 85
reliable_start = 90
reliable_end = 99

miss_rate = 100/1000  # 用户掉线情况 0表示不缺失,越接近1 缺失越多
miss_number = 1000/1000  # 用户掉线个数 1表示不缺失,越接近0 缺失越多
extreme_client_rate = 0/1000  # 提交极端值的用户比率 越接近1 越多
extreme_client_number = 20  # 提交极端值的用户个数
extreme_task_rate = 1  # 提交极端值的用户任务极端的比率 越接近1 越多
error_rate = 3
spite_client_vs_error_client = 0  # 恶意用户和传感器偏差的可能 该数值越大,则越有可能是恶意用户
extreme_detection_flag = True  # 是否进行极端值检测
extreme_detection_flag_ = True  # 对比方案是否进行极端值检测
extreme_detection_small_rate = 0.1
extreme_detection_big_rate = 2.5
extreme_data = 1000000

# TD
K = client_number
M = 50
count = 50

# DH
p = 9584766362985668998675320225938492576833127437546441475200651386681661214949815198902067575999636607649757091547852460848597727186027733861209248123986003
q = None
g = 2

# noise
select_index = 0  # 选择哪个边缘节点的随机向量
client_noise = 0
edge_masking_noise = 0
edge_noise = 0
ru_start = 0
ru_end = 1000
seed_start = 0
seed_end = 100000
masking_p = 100000
prf_p = 10000
