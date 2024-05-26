import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad


class AesCipher:
    def __init__(self, key, version):
        self.key = hashlib.md5(key).hexdigest()[:16].encode()
        self.version = version
    
    @staticmethod
    def decodeBase64(baseStr: str):
        return base64.b64decode(baseStr.encode())
    
    def decrypt(self, enc):
        if self.version == 4:
            cipher = AES.new(self.key, AES.MODE_ECB, use_aesni=True) # 启用AES-NI指令集的硬件加速
        elif self.version == 3:
            cipher = AES.new(self.key, AES.MODE_CBC, iv=b'\0' * 16, use_aesni=True) # 启用AES-NI指令集的硬件加速
        if (dec := self._unpad(cipher.decrypt(enc))):
            return dec

    # def checkSize(self, enc, dec):
    #     return len(dec) + (16 - (len(dec)) % 16) == len(enc)

    def _unpad(self, s):
        try:
            return unpad(s, AES.block_size, style='pkcs7')
        except Exception:
            return None

    # def _unpad(self, s):
    #     return s[:-ord(s[-1:])]

if __name__ == '__main__':
    cipher_text = "qPm3sf5ED5vjWYAJhpDBu9LXU7LgIuNSXa1TLo+aWXjp9SpHbDQJqTuJXlaW2NWG"
    cipher_text = AesCipher.decodeBase64(cipher_text)
    print(AesCipher(b'hunting', version=4).decrypt(cipher_text))
