from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import dh


class ClientManager:
    def __init__(self):
        print("init ClientManager")
        self.Key_generate()

    def Key_generate(self):
        parameters =  dh.generate_parameters(generator=2, key_size=512, backend=default_backend())
        a_private_key = parameters.generate_private_key()
        a_peer_public_key = a_private_key.public_key()

        b_private_key = parameters.generate_private_key()
        b_peer_public_key = b_private_key.public_key()

        a_shared_key = a_private_key.exchange(b_peer_public_key)
        b_shared_key = b_private_key.exchange(a_peer_public_key)
        print(        'a_secret: ' + str(a_shared_key))
        print(
        'b_secret: ' + str(b_shared_key))
