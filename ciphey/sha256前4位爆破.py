import hashlib
import itertools
from string import digits, ascii_letters, punctuation

alpha_bet = digits + ascii_letters + punctuation
strlist = itertools.product(alpha_bet, repeat=4)

sha256 = "b31fdcc13591c8b8dbd1e3ac77b459f5d844e59d5e762f368ebf31b24e21b4d4"
tail = "BuRB7ZHmeR4nGjtI"

xxxx = ''

for i in strlist:
    data = i[0] + i[1] + i[2] + i[3]
    data_sha = hashlib.sha256((data + str(tail)).encode('utf-8')).hexdigest()
    if data_sha == str(sha256):
        xxxx = data
        break

print(xxxx)


