import random

import params
from utils.Encrypt import Encrypt


class Masking:
    client_number = 0
    M = 0
    K = 0
    masking_p = 0
    client_seed_all = list()
    random_all_client = list()

    def __init__(self, client_number, m, k, masking_p):
        self.client_number = client_number
        self.M = m
        self.K = k
        self.masking_p = masking_p

    def generate_seed_i_j(self, seed_start, seed_end):
        """
        用户之间协商m共享的asking随机数种子
        :param seed_start:masking随机数种子起点
        :param seed_end:masking随机数种子终点
        :return:
        """
        for i in range(self.client_number):
            client_random_one = list()
            for j in range(self.client_number):
                client_random_one.append(0)
            self.client_seed_all.append(client_random_one)
        for i in range(self.client_number):
            j = i + 1
            while j < self.client_number:
                temp = random.randrange(seed_start, seed_end)
                self.client_seed_all[i][j] = temp
                self.client_seed_all[j][i] = temp
                j += 1

    def generate_random_all_client(self):
        """
        用户生成本次用的随机数
        :return:
        """
        # 逐个处理用户
        for i in range(self.client_number):
            random_one_client = list()
            for m in range(self.M):
                random_one_client_one_task = list()
                for k in range(self.K):
                    random_one_client_one_task_with_j = list()
                    for j in range(self.client_number):
                        random_one_client_one_task_with_j.append(0)
                    random_one_client_one_task.append(random_one_client_one_task_with_j)
                random_one_client.append(random_one_client_one_task)
            self.random_all_client.append(random_one_client)

        for i in range(self.client_number):
            for m in range(self.M):
                for k in range(self.K):
                    j = i + 1
                    while j < self.client_number:
                        if m == 0 or k == 0:
                            random_noise = Encrypt.random_prf(self.client_seed_all[i][j] + m + k, params.prf_p)
                            self.random_all_client[i][m][k][j] = random_noise
                            self.random_all_client[j][m][k][i] = random_noise
                        else:
                            random_noise = Encrypt.random_prf(self.random_all_client[i][m][-1][j], params.prf_p)
                            self.random_all_client[i][m][k][j] = random_noise
                            self.random_all_client[j][m][k][i] = random_noise
                        j += 1


if __name__ == '__main__':
    print('PyCharm')
    masking = Masking(10, 3, 10, 10000000000000)
    masking.generate_seed_i_j(0, 1000000000)
    print(masking.client_seed_all)
    # 测试PRF
    masking.generate_random_all_client()
    print(masking.random_all_client)
    print("aaaaaaaa")
