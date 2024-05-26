import uuid
from Crypto.Util.number import *

flag = f"BYXS20{{{uuid.uuid4()}}}"
seed = bytes_to_long(flag.encode())
length = seed.bit_length()
print(length)

a = getPrime(length)
b = getPrime(length)
m = getPrime(length)

results = []
for _ in range(10):
    seed = (a * seed + b) % m
    results.append(seed)

print(f"results = {results}")