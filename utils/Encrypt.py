import hashlib
import time

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from gmssl import func


class Encrypt:
    parameters = None

    def __init__(self, p, g):
        self.parameters = dh.DHParameterNumbers(p=p, g=g, q=None, ).parameters()

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
    def aes_list_encryptor(key, plain_list: list):
        cipher = Cipher(algorithms.AES(key), modes.CFB(b"a" * 16))
        encryptor = cipher.encryptor()
        ct = encryptor.update(bytes(plain_list)) + encryptor.finalize()
        # ct = encryptor.update(func.list_to_bytes(plain_list)) + encryptor.finalize()
        return ct

    @staticmethod
    def aes_list_decryptor(key, ciphertext):
        cipher = Cipher(algorithms.AES(key), modes.CFB(b"a" * 16))
        decryptor = cipher.decryptor()
        dt = decryptor.update(ciphertext) + decryptor.finalize()
        return list(dt)

    @staticmethod
    def hashCode(s):
        seed = 31
        h = 0
        for c in s:
            h = int(seed * h) + ord(c)
        return h

    @staticmethod
    def hash_random(plaintext: int):
        # hex_temp = hashlib.sha1(bytes(plaintext)).hexdigest()[0:5]
        hex_temp = hashlib.sha1(plaintext.to_bytes(4, byteorder='big')).hexdigest()[0:5]
        temp = Encrypt.hashCode(hex_temp)
        return temp

    @staticmethod
    def random_prf(seed, p):
        # hex_temp = hashlib.sha1(bytes(seed)).hexdigest()
        hex_temp = hashlib.sha1(seed.to_bytes(4, byteorder='big')).hexdigest()
        temp = Encrypt.hashCode(hex_temp)
        return temp % p


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
# text = [15, 21, 9, 28, 18, 12, 11, 24, 19, 0,15, 21, 9, 28, 18, 12, 11, 24, 19, 0,15, 21, 9, 28, 18, 12, 11, 24, 19, 0,15, 21, 9, 28, 18, 12, 11, 24, 19, 0,15, 21, 9, 28, 18, 12, 11, 24, 19, 0,15, 21, 9, 28, 18, 12, 11, 24, 19, 0,15, 21, 9, 28, 18, 12, 11, 24, 19, 0,15, 21, 9, 28, 18, 12, 11, 24, 19, 0,15, 21, 9, 28, 18, 12, 11, 24, 19, 0,15, 21, 9, 28, 18, 12, 11, 24, 19, 0,15, 21, 9, 28, 18, 12, 11, 24, 19, 0,15, 21, 9, 28, 18, 12, 11, 24, 19, 0]
# text = [15, 21, 9, 28, 18, 12, 11, 24, 19, 0]
# print(text.index(9))
# print(text.index(10))
# ct = Encrypt.aes_list_encryptor(key, text)
# print(ct)
# print(ct[0:10])
# print(func.bytes_to_list(ct))
# dt = Encrypt.aes_list_decryptor(key1, ct)
# print(dt)
#
# print(Encrypt.hash_random(0))

# times = 100000
# start_1 = time.perf_counter()
# for i in range(times):
#     a = func.list_to_bytes(text)
#     # b = func.bytes_to_list(a)
# start_2 = time.perf_counter()
# for i in range(times):
#     a = bytes(text)
#     # b = list(a)
# start_3 = time.perf_counter()
#
# print(start_2 - start_1)
# print(start_3 - start_2)

# seed = 1000000000
# times = 100000
# start_1 = time.perf_counter()
# for i in range(times):
#     a = bytes(seed)
#     # b = func.bytes_to_list(a)
# start_2 = time.perf_counter()
# for i in range(times):
#     a = seed.to_bytes(32, byteorder='big')
#     # b = int.from_bytes(a,byteorder='big')
#     # print(b)
#     # b = list(a)
# start_3 = time.perf_counter()
#
# print(start_2-start_1)
# print(start_3-start_2)
