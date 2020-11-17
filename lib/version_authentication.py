import requests

from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.Signature import PKCS1_v1_5

from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
import base64
import config
import json

class RsaUtil:

    def __init__(self):
        self.pri_key_obj = None
        self.verifier = None
        self.signer = None
        pri_key = RSA.importKey(base64.b64decode(config.pri_key))
        self.pri_key_obj = Cipher_pkcs1_v1_5.new(pri_key)
        self.signer = PKCS1_v1_5.new(pri_key)

    def private_long_decrypt(self, data, sentinel=b'decrypt error'):
        data = base64.b64decode(data)
        length = len(data)
        default_length = 128
        res = []
        for i in range(0, length, default_length):
            res.append(self.pri_key_obj.decrypt(data[i:i + default_length], sentinel))
        return str(b''.join(res), encoding = "utf-8")

    def sign(self, data, charset='utf-8'):
        h = SHA256.new(data.encode(charset))
        signature = self.signer.sign(h)
        return base64.b64encode(signature)

    def verify(self, data, sign,  charset='utf-8'):
        h = SHA256.new(data.encode(charset))
        return self.verifier.verify(h, base64.b64decode(sign))


def get_version():
    url = "http://47.102.159.15:8002/get_version"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    rsa = RsaUtil()
    data = rsa.private_long_decrypt(response.content)
    data = json.loads(data)
    return data