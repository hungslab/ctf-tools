import re

with open("./flag.pdf", "rb") as f:
    data = f.read()

print(b''.join(re.findall(b"<<(.*?)/Filter", data)))