import hashlib

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from gmssl import func

import params


class Encrypt:
    parameters = None

    def __init__(self):
        self.parameters = dh.DHParameterNumbers(p=params.p, g=params.g, q=None, ).parameters()

    def generate_dh_key(self):
        private_key = self.parameters.generate_private_key()
        public_key = private_key.public_key()
        return private_key.private_numbers().x, public_key.public_numbers().y

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

    @staticmethod
    def aes_encryptor(key, plaintext):
        cipher = Cipher(algorithms.AES(key), modes.ECB())
        encryptor = cipher.encryptor()
        ct = encryptor.update(bytes(plaintext)) + encryptor.finalize()
        return ct

    @staticmethod
    def aes_decryptor(key, ciphertext):
        cipher = Cipher(algorithms.AES(key), modes.ECB())
        decryptor = cipher.decryptor()
        dt = decryptor.update(ciphertext) + decryptor.finalize()
        return dt

    @staticmethod
    def aes_list_encryptor(key, plain_list):
        cipher = Cipher(algorithms.AES(key), modes.CFB(b"a" * 16))
        encryptor = cipher.encryptor()
        ct = encryptor.update(bytes(plain_list)) + encryptor.finalize()
        return ct

    @staticmethod
    def aes_list_decryptor(key, ciphertext):
        cipher = Cipher(algorithms.AES(key), modes.CFB(b"a" * 16))
        decryptor = cipher.decryptor()
        dt = decryptor.update(ciphertext) + decryptor.finalize()
        return func.bytes_to_list(dt)

    @staticmethod
    def hashCode(s):
        seed = 31
        h = 0
        for c in s:
            h = int(seed * h) + ord(c)
        return h

    @staticmethod
    def hash_random(plaintext: int):
        hex_temp = hashlib.sha1(bytes(plaintext)).hexdigest()[0:5]
        temp = Encrypt.hashCode(hex_temp)
        return temp


# if __name__ == '__main__':
#     print('PyCharm')
# encrypt = Encrypt()
# a_pri, a_pub = encrypt.generate_dh_key()
# b_pri, b_pub = encrypt.generate_dh_key()
# key = encrypt.generate_aes_key(a_pri, a_pub, b_pub)
# key1 = encrypt.generate_aes_key(b_pri, b_pub, a_pub)
# print(key)
# print(key1)
# print(key == key1)
# print(Encrypt.aes_decryptor(key, Encrypt.aes_encryptor(key, b"a" * 16)))
#
# text = [15, 21, 9, 28, 18, 12, 11, 24, 19, 0]
# print(text.index(9))
# print(text.index(10))
# ct = Encrypt.aes_list_encryptor(key, text)
# print(ct)
# print(ct[0:10])
# print(func.bytes_to_list(ct))
# dt = Encrypt.aes_list_decryptor(key1, ct)
# print(dt)

print(Encrypt.hash_random(10))
# print(Encrypt.hash_random(i))
