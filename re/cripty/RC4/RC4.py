import binascii

def rc4_crypt(PlainBytes:bytes, KeyBytes:bytes) -> str:
    '''[summary]
    rc4 crypt
    Arguments:
        PlainBytes {[bytes]} -- [plain bytes]
        KeyBytes {[bytes]} -- [key bytes]
    
    Returns:
        [string] -- [hex string]
    '''
    keystreamList = []
    cipherList = []
    keyLen = len(KeyBytes)
    plainLen = len(PlainBytes)
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + KeyBytes[i % keyLen]) % 256
        S[i], S[j] = S[j], S[i]
 
    i = 0
    j = 0
    for m in range(plainLen):
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        k = S[(S[i] + S[j]) % 256]
        cipherList.append(k ^ PlainBytes[m])
 
    result_hexstr = ''.join(['%02x' % i for i in cipherList])
    return result_hexstr.upper()
 
if __name__ == "__main__":
    data = '7FD71DC7B23190B05971E41306606EA290DC7CB2D5'
    key = "litctf!"
    result = rc4_crypt(binascii.a2b_hex(data)[::-1], key.encode())
    print(result)
    print(bytes.fromhex(result))

