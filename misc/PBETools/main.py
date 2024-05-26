import js2py
import base64
import hashlib
import binascii
import contextlib
from Crypto.Util.Padding import unpad
from Crypto.Cipher import AES, DES, DES3, ARC4


def bytes_to_key(data, salt, output=48):
    # extended from https://gist.github.com/gsakkis/4546068
    assert len(salt) == 8, len(salt)
    data += salt
    key = hashlib.md5(data).digest()
    final_key = key
    while len(final_key) < output:
        key = hashlib.md5(key + data).digest()
        final_key += key
    return final_key[:output]

def AES128Decrypt(key, cipher_text):
    dec_Base = base64.b64decode(cipher_text)
    salt = dec_Base[8:16]
    key_iv = bytes_to_key(key, salt, 16+16)
    key, iv = key_iv[:16], key_iv[16:]
    aes = AES.new(key, AES.MODE_CBC, iv)
    return unpad(aes.decrypt(dec_Base[16:]), block_size=aes.block_size)

def AES192Decrypt(key, cipher_text):
    dec_Base = base64.b64decode(cipher_text)
    salt = dec_Base[8:16]
    key_iv = bytes_to_key(key, salt, 24+16)
    key, iv = key_iv[:24], key_iv[24:]
    aes = AES.new(key, AES.MODE_CBC, iv)
    return unpad(aes.decrypt(dec_Base[16:]), block_size=aes.block_size)

def AES256Decrypt(key, cipher_text):
    dec_Base = base64.b64decode(cipher_text)
    salt = dec_Base[8:16]
    key_iv = bytes_to_key(key, salt, 32+16)
    key, iv = key_iv[:32], key_iv[32:]
    aes = AES.new(key, AES.MODE_CBC, iv)
    return unpad(aes.decrypt(dec_Base[16:]), block_size=aes.block_size)

def DESDecrypt(key, cipher_text):
    dec_Base = base64.b64decode(cipher_text)
    salt = dec_Base[8:16]
    key_iv = bytes_to_key(key, salt, 8+8)
    key, iv = key_iv[:8], key_iv[8:]
    des = DES.new(key, DES.MODE_CBC, iv)
    return unpad(des.decrypt(dec_Base[16:]), block_size=des.block_size)
    
def TripleDesDecrypt(key, cipher_text):
    dec_Base = base64.b64decode(cipher_text)
    salt = dec_Base[8:16]
    key_iv = bytes_to_key(key, salt, 24+8)
    key, iv = key_iv[:24], key_iv[24:]
    des3 = DES3.new(key, DES3.MODE_CBC, iv)
    return unpad(des3.decrypt(dec_Base[16:]), block_size=des3.block_size)

def RC4Decrypt(key, cipher_text):
    dec_Base = base64.b64decode(cipher_text)
    salt = dec_Base[8:16]
    key_iv = bytes_to_key(key, salt, 32)
    des3 = ARC4.new(key_iv)
    return des3.decrypt(dec_Base[16:])

def RabbitDecrypt(key, cipher_text):
    # js file from https://tool.ip138.com/aesdes/
    with open("./js/rabbit.js", "r") as f:
        jsCode = f.read()
    
    content = js2py.EvalJs()
    content.execute(jsCode)
    return binascii.a2b_hex(content.RabbitDecrypt(cipher_text, key.decode()))
    # context = execjs.compile(jsCode)
    # return binascii.a2b_hex(context.call('RabbitDecrypt', cipher_text, key.decode()))

def Rabbit2Decrypt(key, cipher_text):
    # js file from https://wishingstarmoye.com/ctf/cryptojs
    with open("./js/rabbit2.js", "r") as f:
        jsCode = f.read()
    
    content = js2py.EvalJs()
    content.execute(jsCode)
    return binascii.a2b_hex(content.RabbitDecrypt(cipher_text, key.decode()))
    # context = execjs.compile(jsCode)
    # return binascii.a2b_hex(context.call('RabbitDecrypt', cipher_text, key.decode()))

def BruteForceDecrypt(key, cipher_text):
    algorithms = {
        "Aes128Decrypt": AES128Decrypt, 
        "Aes192Decrypt": AES192Decrypt, 
        "Aes256Decrypt": AES256Decrypt, 
        "DesDecrypt": DESDecrypt, 
        "TripleDesDecrypt": TripleDesDecrypt, 
        "Rc4Decrypt": RC4Decrypt, 
        "RabbitDecrypt": RabbitDecrypt,
        "Rabbit2Decrypt": Rabbit2Decrypt
    }

    for algorithm in algorithms:
        with contextlib.suppress(Exception):
            plain_text = algorithms[algorithm](key, cipher_text)
            print(f"{algorithm}: {plain_text}")


if __name__ == '__main__':
    # example()
    BruteForceDecrypt(b"Gui_1s_shumu", "U2FsdGVkX19bEN3D8vFeG39VyYXPwle2mMQLh5T1HYiSI1XCx7rJhsDnp9qLpUQByITd05Uu05ZAv0o=")

    # 攻防世界 - Aesop_secret
    BruteForceDecrypt(b"ISCC", "U2FsdGVkX19QwGkcgD0fTjZxgijRzQOGbCWALh4sRDec2w6xsY/ux53Vuj/AMZBDJ87qyZL5kAf1fmAH4Oe13Iu435bfRBuZgHpnRjTBn5+xsDHONiR3t0+Oa8yG/tOKJMNUauedvMyN4v4QKiFunw==")