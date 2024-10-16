def encrypt(rounds, v, k):
    v0 = v[0]
    v1 = v[1]
    x = 0
    delta = 0x9E3779B9
    for i in range(rounds):
        v0 += (((v1 << 4) ^ (v1 >> 5)) + v1) ^ (x + k[x & 3])
        v0 = v0 & 0xFFFFFFFF
        x += delta
        x = x & 0xFFFFFFFF
        v1 += (((v0 << 4) ^ (v0 >> 5)) + v0) ^ (x + k[(x >> 11) & 3])
        v1 = v1 & 0xFFFFFFFF
    v[0] = v0
    v[1] = v1
    return v
def decrypt(rounds, v, k):
    v0 = v[0]
    v1 = v[1]
    delta = 0x9E3779B9
    x = delta * rounds
    for i in range(rounds):
        v1 -= (((v0 << 4) ^ (v0 >> 5)) + v0) ^ (x + k[(x >> 11) & 3])
        v1 = v1 & 0xFFFFFFFF
        x -= delta
        x = x & 0xFFFFFFFF
        v0 -= (((v1 << 4) ^ (v1 >> 5)) + v1) ^ (x + k[x & 3])
        v0 = v0 & 0xFFFFFFFF
    v[0] = v0
    v[1] = v1
    return v
if __name__ == '__main__':
    # encrypted = [0xA3699626, 0xBD780B3D, 0x9DA52862]
    encrypted = [0x0B3D9DA5, 0x2862A369, 0X9626BD78]
    key = [2, 0, 2, 4]
    rounds = 32
    # encrypted = encrypt(rounds, plain, key)

    decrypted = decrypt(rounds, encrypted, key)
    decrypted = decrypt(rounds, decrypted, key)
    print('Plain: ',  [hex(num & 0xffffffff) for num in decrypted])