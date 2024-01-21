from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_v1_5
from Cryptodome.Hash import SHA1

def rsa_public_key(mod, exp):
    return RSA.construct((mod, exp))

def pkcs1v15_encrypt(key, message):
    return PKCS1_v1_5.new(key).encrypt(message)

def sha1_hash(data):
    return SHA1.new(data).digest()
