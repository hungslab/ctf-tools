import hashlib
import itertools
from string import digits, ascii_letters

alpha_bet = digits + ascii_letters
strlist = itertools.product(alpha_bet, repeat=6)

sha256 = "58e682ebf9bc9d4550c31b8546c7d2f57fdcb50fafd3718aa7e34190080f1de4"

xxxx = ''
for i in strlist:
    data = i[0] + i[1] + i[2] + i[3] + i[4] + i[5]
    data_sha = hashlib.sha256(data.encode('utf-8')).hexdigest()
    if data_sha == str(sha256):
        xxxx = data
        break

print(xxxx)
