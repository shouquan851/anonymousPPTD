import os

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

import params


class Encrypt:
    parameters = None

    def __init__(self):
        self.parameters = dh.DHParameterNumbers(p=params.p, g=params.g, q=None, ).parameters()

    '''
    生成DH公私钥
    '''

    def generate_dh_key(self):
        private_key = self.parameters.generate_private_key()
        public_key = private_key.public_key()
        return private_key.private_numbers().x, public_key.public_numbers().y

    '''
    生成对称密钥
    '''

    def generate_aes_key(self, a_private_key, a_public_key, b_public_key):
        # 生成公私钥
        public_key = dh.DHPublicNumbers(a_public_key, self.parameters.parameter_numbers())
        private_key = dh.DHPrivateNumbers(a_private_key, public_key).private_key()
        b_public_key_ = dh.DHPublicNumbers(b_public_key, self.parameters.parameter_numbers()).public_key()
        # 生成对称密钥
        shared_key = private_key.exchange(b_public_key_)
        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'handshake data',
        ).derive(shared_key)
        return derived_key

    '''
    aes加密
    '''

    @staticmethod
    def aes_encryptor(key, plaintext):
        cipher = Cipher(algorithms.AES(key), modes.ECB())
        encryptor = cipher.encryptor()
        ct = encryptor.update(bytes(plaintext)) + encryptor.finalize()
        return ct

    '''
    aes解密
    '''

    @staticmethod
    def aes_decryptor(key, ciphertext):
        cipher = Cipher(algorithms.AES(key), modes.ECB())
        decryptor = cipher.decryptor()
        dt = decryptor.update(ciphertext) + decryptor.finalize()
        return dt

# if __name__ == '__main__':
#     print('PyCharm')
# encrypt = Encrypt()
# a_pri, a_pub = encrypt.generate_dh_key()
# b_pri, b_pub = encrypt.generate_dh_key()
# key = encrypt.generate_aes_key(a_pri, a_pub, b_pub)
# key1 = encrypt.generate_aes_key(b_pri, b_pub, a_pub)
# print(key)
# print(key1)
# print(key==key1)
# print(Encrypt.aes_decryptor(key, Encrypt.aes_encryptor(key, b"a" * 16)))
