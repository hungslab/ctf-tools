import os
import subprocess


filters = ["usb.capdata", "usbhid.data"]
CACHE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache")

def get_input():
    while True:
        if (tmp := input("[+]: 请选择数据类型(1.usb.capdata 2.usbhid.data 3.回车默认): ")) in ["1", "2"]:
            return int(tmp)
        elif tmp == "":
            return None

def get_length(file_path, filter):
    command = f'D:\\Tools\\web-sec\\漏洞分析\\Wireshark\\tshark.exe -r {file_path} -Y {filter} -T fields -e {filter}'
    res = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    with open(f"{os.path.join(CACHE_PATH, filter)}.txt", "w") as f:
        data = res.stdout.read().decode("gbk").replace("\r\n", "\n")
        f.write(data)
    return len(data.splitlines())

def get_select(file_path):
    size = round(os.path.getsize(file_path) / (1024 * 1024), 2)
    lengths = [get_length(file_path, filter) for filter in filters]

    if lengths[0] == 0 and lengths[1] == 0:
        print(f"[-]: usb.size: {size}(MB), usb.capdata: {lengths[0]}, usbhid.data: {lengths[1]}, 默认读取: {filters[0]}")
        print("请检查您的流量名是否有空格或符号, 如果有请删除并重新命名!")
        exit(-1)
    elif lengths[0] >= lengths[1]:
        print(f"[-]: usb.size: {size}(MB), usb.capdata: {lengths[0]}, usbhid.data: {lengths[1]}, 默认读取: {filters[0]}")
        select = 1
    else:
        print(f"[-]: usb.size: {size}(MB), usb.capdata: {lengths[0]}, usbhid.data: {lengths[1]}, 默认读取: {filters[1]}")
        select = 2

    if (tmp := get_input()) is not None:
        select = tmp
    return select

def get_data(file_path):
    select = get_select(file_path)
    with open(f"{os.path.join(CACHE_PATH, filters[select - 1])}.txt", "r") as f:
        data = f.read().splitlines()
    return data

if __name__ == '__main__':
    print(get_data("usb.pcapng"))