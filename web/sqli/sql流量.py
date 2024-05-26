import re
a=[]
with  open("flag.pcapng","rb") as f:
    for i in f.readlines():
        if b"1%27+or+ascii%28substr%28%28select+group_concat%28password%29+from+user+where+userName%3D%27flag%27%29" in i:
            a.append(i.strip())
a1={}
flag=''
for i in a: 
    b = re.search(br"%2C(\d+)%2C1%29%29%3E(\d+)", i).group(1).decode()
    c = re.search(br"%2C(\d+)%2C1%29%29%3E(\d+)", i).group(2).decode()
    print(b)
    print(c)
    a1[int(b)] = int(c)
print(a1)
for i in range(1,11):
    flag = flag + chr(a1[i])
print(flag)
# ISCTF{sql_is_very_easy}
