def encrypt(v, k):
    v0 = v[0]
    v1 = v[1]
    x = 0
    delta = 0x9E3779B9
    k0 = k[0]
    k1 = k[1]
    k2 = k[2]
    k3 = k[3]
    for i in range(32):
        x += delta
        x = x & 0xFFFFFFFF
        v0 += ((v1 << 4) + k0) ^ (v1 + x) ^ ((v1 >> 5) + k1)
        v0 = v0 & 0xFFFFFFFF
        v1 += ((v0 << 4) + k2) ^ (v0 + x) ^ ((v0 >> 5) + k3)
        v1 = v1 & 0xFFFFFFFF
    v[0] = v0
    v[1] = v1
    return v
def decrypt(v, k):
    v0 = v[0]
    v1 = v[1]
    x = 0xC6EF3720
    delta = 0x9E3779B9
    k0 = k[0]
    k1 = k[1]
    k2 = k[2]
    k3 = k[3]
    for i in range(32):
        v1 -= ((v0 << 4) + k2) ^ (v0 + x) ^ ((v0 >> 5) + k3)
        v1 = v1 & 0xFFFFFFFF
        v0 -= ((v1 << 4) + k0) ^ (v1 + x) ^ ((v1 >> 5) + k1)
        v0 = v0 & 0xFFFFFFFF
        x -= delta
        x = x & 0xFFFFFFFF
    v[0] = v0
    v[1] = v1
    return v
    
if __name__ == '__main__':
    encrypted = [0x284C2234, 0x3910C558]
    key = [1702060386, 1870148662, 1634038898, 1634038904]
    # encrypted = encrypt(plain, key)
    decrypted = decrypt(encrypted, key)
    
    print('Plain: ',  [hex(num) for num in decrypted])