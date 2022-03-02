from utils.Encrypt import Encrypt


class CloudServer:
    private_key = None
    public_key = None
    aes_key_list_with_client = None

    def __init__(self):
        print("init CloudServer")

    '''
    生成dh公私钥
    '''
    def generate_dh_key(self):
        encrypt = Encrypt()
        self.private_key, self.public_key = encrypt.generate_dh_key()
    '''
    生成和用户的共享密钥
    '''
    def generate_aes_key(self, public_key_client_list):
        aes_key_list_with_client = list()
        encrypt = Encrypt()
        for public_key_client in public_key_client_list:
            aes_key_list_with_client.append(
                encrypt.generate_aes_key(self.private_key, self.public_key, public_key_client))
        self.aes_key_list_with_client = aes_key_list_with_client
        return aes_key_list_with_client
