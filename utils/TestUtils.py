class TestUtils:

    def __init__(self):
        pass

    @staticmethod
    def get_RMSE(result_list, truth_list):
        M = len(result_list)
        temp = 0
        for m in range(M):
            temp = temp + (result_list[m] - truth_list[m]) ** 2
        return (temp / M) ** 0.5
