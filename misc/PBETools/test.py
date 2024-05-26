from main import *

if __name__ == '__main__':
    # AES
    print(AES128Decrypt(b"123", "U2FsdGVkX19sTZDwd5c0MQwWhW8HWVNuOmpGsE+bhLa0gXITdVSojT0vsmuuXfGn"))
    print(AES192Decrypt(b"123", "U2FsdGVkX19sTZDwd5c0MRcERwLNxNRA+hdHfykE+DlDOGNjDd7w+1b0ZrwU3NVR"))
    print(AES256Decrypt(b"123", "U2FsdGVkX1/Cypfk69uqZGCEDOF9loE4vVJ03hh01Yif+Y/ZigZdO53dU/UBdY48"))
    
    # DES
    print(DESDecrypt(b"123", "U2FsdGVkX1+C4UoPrPwGrt4DxgzHxcqxwG9lpDns87Rb+wW4bCeQpg=="))
    
    # 3DES
    print(TripleDesDecrypt(b"123", "U2FsdGVkX1/ysI7dcQULvLVMVtPrvu8n1y6wJdckvz18Q4EUzal5Gw=="))

    # RC4
    print(RC4Decrypt(b"123", "U2FsdGVkX18c7nwA2OsstI0a+jJP5UUwaSoyp/FHUCieYpNR"))
    
    # Rabbit
    print(RabbitDecrypt(b"Gui_1s_shumu", "U2FsdGVkX19bEN3D8vFeG39VyYXPwle2mMQLh5T1HYiSI1XCx7rJhsDnp9qLpUQByITd05Uu05ZAv0o="))
    print(AES256Decrypt(b"hahaha,youcantgetflag!!", "U2FsdGVkX18s+Wam0HiVp+vgdF9bvG6SlUvWFqhNN6cnm9HH9eITVxxJW9CzPg/R"))
