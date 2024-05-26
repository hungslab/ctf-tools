from Crypto.Cipher import AES
import base64
import binascii

# 数据类
class MData():
  def __init__(self, data = b"",characterSet='utf-8'):
    # data肯定为bytes
    self.data = data
    self.characterSet = characterSet

  def saveData(self,FileName):
    with open(FileName,'wb') as f:
      f.write(self.data)

  def fromString(self,data):
    self.data = data.encode(self.characterSet)
    return self.data

  def fromBase64(self,data):
    self.data = base64.b64decode(data.encode(self.characterSet))
    return self.data

  def fromHexStr(self,data):
    self.data = binascii.a2b_hex(data)
    return self.data

  def toString(self):
    return self.data.decode(self.characterSet)

  def toBase64(self):
    return base64.b64encode(self.data).decode()

  def toHexStr(self):
    return binascii.b2a_hex(self.data).decode()

  def toBytes(self):
    return self.data

  def __str__(self):
    try:
        return self.toString()
    except Exception:
        return self.toBase64()


### 封装类
class AEScryptor():
  def __init__(self,key,mode,iv = '',paddingMode= "NoPadding",characterSet ="utf-8",keylegth= 16):
      '''
      构建一个AES对象
      key: 秘钥，字节型数据
      mode: 使用模式，只提供两种，AES.MODE_CBC, AES.MODE_ECB, AES.MODE_CFB, AES.MODE_OFB, AES.MODE_CTR
      iv： iv偏移量，字节型数据
      paddingMode: 填充模式，默认为NoPadding, 可选NoPadding，ZeroPadding，PKCS5Padding，PKCS7Padding
      characterSet: 字符集编码
      keylegth: 密钥长度
      '''
      self.key = key
      self.mode = mode
      self.iv = iv
      self.characterSet = characterSet
      self.paddingMode = paddingMode
      self.data = ""
      self.keylegth = keylegth

  def __ZeroPadding(self,data,keylegth):

      if keylegth == 24:
        data += b'\x00'
        while len(data) % 24 != 0:
            data += b'\x00'
        return data
      elif keylegth == 32:
        data += b'\x00'
        while len(data) % 32 != 0:
            data += b'\x00'
        return data
      else:
        data += b'\x00'
        while len(data) % 16 != 0:
            data += b'\x00'
        return data

  def __StripZeroPadding(self,data,keylegth):
      data = data[:-1]
      if keylegth == 24:
        while len(data) % 24 != 0:
            data = data.rstrip(b'\x00')
            if data[-1] != b"\x00":
                break
        return data

      elif keylegth == 32:
        while len(data) % 32 != 0:
            data = data.rstrip(b'\x00')
            if data[-1] != b"\x00":
                break
        return data

      else:
        while len(data) % 16 != 0:
            data = data.rstrip(b'\x00')
            if data[-1] != b"\x00":
                break
        return data

  def __PKCS5_7Padding(self,data,keylegth):
      if keylegth == 24:
        needSize = 24-len(data) % 24
        if needSize == 0:
            needSize = 24
      elif keylegth == 32:
        needSize = 32-len(data) % 32
        if needSize == 0:
            needSize = 32
      else:
        needSize = 16-len(data) % 16
        if needSize == 0:
            needSize = 16
      return data + needSize.to_bytes(1,'little')*needSize

  def __StripPKCS5_7Padding(self,data,keylegth):
      paddingSize = data[-1]
      return data.rstrip(paddingSize.to_bytes(1,'little'))

  def __paddingData(self,data,keylegth):
      if self.paddingMode == "NoPadding":
          if keylegth == 24:
            if len(data) % 24 == 0:
                return data
            else:
                return self.__ZeroPadding(data,keylegth)
          elif keylegth == 32:
            if len(data) % 32 == 0:
                return data
            else:
                return self.__ZeroPadding(data,keylegth)
          else:
            if len(data) % 16 == 0:
                return data
            else:
                return self.__ZeroPadding(data,keylegth)

      elif self.paddingMode == "ZeroPadding":
          return self.__ZeroPadding(data,keylegth)
      elif self.paddingMode == "PKCS5Padding" or self.paddingMode == "PKCS7Padding":
          return self.__PKCS5_7Padding(data,keylegth)
      else:
          print("不支持Padding")

  def __stripPaddingData(self,data,keylegth):
      if self.paddingMode == "NoPadding":
          return self.__StripZeroPadding(data,keylegth)
      elif self.paddingMode == "ZeroPadding":
          return self.__StripZeroPadding(data,keylegth)

      elif self.paddingMode == "PKCS5Padding" or self.paddingMode == "PKCS7Padding":
          return self.__StripPKCS5_7Padding(data,keylegth)
      else:
          print("不支持Padding")

  def setCharacterSet(self,characterSet):
      '''
      设置字符集编码
      characterSet: 字符集编码
      '''
      self.characterSet = characterSet

  def setPaddingMode(self,mode):
      '''
      设置填充模式
      mode: 可选NoPadding，ZeroPadding，PKCS5Padding，PKCS7Padding
      '''
      self.paddingMode = mode

  def decryptFromBase64(self,entext):
      '''
      从base64编码字符串编码进行AES解密
      entext: 数据类型str
      '''
      mData = MData(characterSet=self.characterSet)
      self.data = mData.fromBase64(entext)
      return self.__decrypt()

  def decryptFromHexStr(self,entext):
      '''
      从hexstr编码字符串编码进行AES解密
      entext: 数据类型str
      '''
      mData = MData(characterSet=self.characterSet)
      self.data = mData.fromHexStr(entext)
      return self.__decrypt()

  def decryptFromString(self,entext):
      '''
      从字符串进行AES解密
      entext: 数据类型str
      '''
      mData = MData(characterSet=self.characterSet)
      self.data = mData.fromString(entext)
      return self.__decrypt()

  def decryptFromBytes(self,entext):
      '''
      从二进制进行AES解密
      entext: 数据类型bytes
      '''
      self.data = entext
      return self.__decrypt()

  def encryptFromString(self,data):
      '''
      对字符串进行AES加密
      data: 待加密字符串，数据类型为str
      '''
      self.data = data.encode(self.characterSet)
      return self.__encrypt()

  def __encrypt(self):
      if self.mode == AES.MODE_CBC:
          aes = AES.new(self.key,self.mode,self.iv)

      #不需要向量
      elif self.mode == AES.MODE_ECB:
          aes = AES.new(self.key,self.mode)

      elif self.mode == AES.MODE_CFB:
        aes = AES.new(self.key,self.mode,self.iv)

      #不需要填充
      elif self.mode == AES.MODE_OFB:
        aes = AES.new(self.key,self.mode,self.iv)
      elif self.mode == AES.MODE_CTR:
        aes = AES.new(self.key,self.mode,self.iv)

      else:
          print("不支持这种模式")
          return

      data = self.__paddingData(self.data)
      enData = aes.encrypt(data)
      return MData(enData)

  def __decrypt(self):
    if self.mode == AES.MODE_CBC:
        aes = AES.new(self.key,self.mode,self.iv)
    elif self.mode == AES.MODE_ECB:
        aes = AES.new(self.key,self.mode)
    elif self.mode == AES.MODE_CFB:
      aes = AES.new(self.key,self.mode,self.iv)

    #不需要填充
    elif self.mode == AES.MODE_OFB:
      aes = AES.new(self.key,self.mode,self.iv)
    elif self.mode == AES.MODE_CTR:
      aes = AES.new(self.key,self.mode,self.iv)
    else:
        print("不支持这种模式")
        return
    data = aes.decrypt(self.data)
    return MData(
        self.__stripPaddingData(data, keylegth=self.keylegth),
        characterSet=self.characterSet,
    )

def padding(raw: bytes, padding: int, max_length: int = None):
    '''
    部分加解密是需要补齐位数到指定padding的
    '''
    c = len(raw)/padding
    block: int = int(c)
    if block != c:
        block += 1
    result = raw.ljust(padding*block, b'\0')
    if max_length:
        result = result[0:max_length]
    return result
  
if __name__ == '__main__':
    aes = AEScryptor(key=b"0b02e4e4593d3a36bf044f44d7038a7f", mode=AES.MODE_CBC, iv=b"d66573dc87b47ed3", keylegth="32")
    print(aes.decryptFromBase64("U2FsdGVkX1/WZXPch7R+06foxuECAoVuKd+g9Rck+UM="))
    