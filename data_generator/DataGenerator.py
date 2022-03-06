import random

import params


class DataGenerator:
    base_data = list()
    reliable_client = list()
    all_client_data = list()

    def __init__(self):
        print("init DataGenerator")

    def generate_base_data(self, base_data_rate, base_data_start, base_data_end, reliable_client_rate):
        """
        生成地面真值和用户可靠性(观测准确度)
        :param base_data_rate: 随即生成地面真值之后乘以的倍数(更加分散)
        :param base_data_start: 随机生成地面真值的起点
        :param base_data_end: 随机生成地面真值的终点
        :param reliable_client_rate: 可靠用户的比例,0-100 越接近100 可靠用户越多
        """
        base_data = list()
        reliable_client = list()
        for m in range(params.M):
            base_data.append(random.randint(base_data_start, base_data_end) * base_data_rate)
        for k in range(params.K):
            temp = random.randint(0, 100)
            if temp < reliable_client_rate:
                reliable_client.append(random.randint(params.reliable_start, params.reliable_end) / 100)
            else:
                reliable_client.append(random.randint(params.unreliable_start, params.unreliable_end) / 100)
        self.base_data = base_data
        self.reliable_client = reliable_client

    def generate_client_data(self):
        all_client_data = list()
        for k in range(params.K):
            one_client_data = list()
            for m in range(params.M):
                # 生成高斯噪声,模拟用户观测不准确
                noise = self.base_data[m] * random.gauss(0, self.reliable_client[k])
                one_client_data.append(self.base_data[m] + noise*0.2)
            all_client_data.append(one_client_data)
        self.all_client_data = all_client_data
        return self.all_client_data
