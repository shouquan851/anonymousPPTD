edge_number = 4
client_number = 500
group_number_list = [100, 100, 100, 200]

# datagenerate
# 可靠程度,越接近100 越可靠
unreliable_start = 60
unreliable_end = 70
reliable_start = 90
reliable_end = 99
miss_rate = 1  #  用户掉线情况 1表示不缺失,越接近0 缺失越多
extreme_client_rate = 0.01  # 提交极端值的用户比率 越接近1 越多
extreme_task_rate = 1  # 提交极端值的用户任务极端的比率 越接近1 越多
error_rate = 3
spite_client_vs_error_client = 1000  # 恶意用户和传感器偏差的可能 该数值越大,则越有可能是传感器偏差
extreme_detection_flag = True  # 是否进行极端值检测
extreme_detection_flag_ = False  # 对比方案是否进行极端值检测
extreme_detection_small_rate = 0.5
extreme_detection_big_rate = 1.5
extreme_data = 100000000

# TD
K = client_number
M = 10
count = 10

# DH
p = 9584766362985668998675320225938492576833127437546441475200651386681661214949815198902067575999636607649757091547852460848597727186027733861209248123986003
q = None
g = 2

# noise
select_index = 2
client_noise = 0
edge_masking_noise = 0
edge_noise = 0
ru_start = 0
ru_end = 1000
seed_start = 0
seed_end = 100000
masking_p = 100000
prf_p = 10000
