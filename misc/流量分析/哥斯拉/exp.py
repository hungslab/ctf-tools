import gzip
import base64

def encode(D, K):
	D = list(D)
	for i in range(len(D)):
		c = K[i + 1 & 15]
		D[i] = D[i] ^ c
	return bytes(D)

key = b"3c6e0b8a9c15224a"
cipher_text = ""[16:-16]
cipher_text = ""

out = encode(base64.b64decode(cipher_text), key)
print(gzip.decompress(out))