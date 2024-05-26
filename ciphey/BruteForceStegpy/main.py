import os
import mmap
import queue
import datetime
import argparse
import threading
from core import lsb2
from multiprocessing import cpu_count


parser = argparse.ArgumentParser()
parser.add_argument('-f', type=str, default=None, required=True,
help='输入文件名称')
parser.add_argument('-d', type=str, default=None, required=True,
help='输入字典的文件名称')
parser.add_argument('-p', type=int, default=cpu_count(),
help='线程数')
args = parser.parse_args()


def read_large_file(file_path):
    # 使用mmap映射文件
    with open(file_path, "r+b") as f:
        with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
            while True:
                yield mm.readline().rstrip(b"\r\n")
                if mm.tell() == len(mm):
                    break

def producer(dic_path, queue_password, process_num):
    global success
    for password in read_large_file(dic_path):
        queue_password.put(password)
        
        if success:
            queue_password.queue.clear()
            break
    
    for _ in range(process_num):
        queue_password.put(None)

def consumer(queue_password):
    global encrypted_data, host, success
    while True:
        pwd = queue_password.get()
        if pwd is None or success:
            return

        tmp = host.read_message(encrypted_data, pwd)
        if tmp != "Wrong password.":
            if not success:   
                success = True
                print(f"Find Password: {pwd.decode()}, Message: {tmp}")
            return


if __name__ == '__main__':
    filePath = os.path.abspath(args.f)
    wordListsPath = os.path.abspath(args.d)
    process_num = args.p - 1

    success = False
    thread_num = cpu_count()
    queue_password = queue.Queue()
    host = lsb2.HostElement(filePath)
    encrypted_data = host.decode_message()

    print(f'[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] 开始执行, 使用线程数: {thread_num}.')
    t = threading.Thread(target=producer, args=(wordListsPath, queue_password, thread_num))
    t.start()
    
    threads = []
    for _ in range(thread_num):
        t = threading.Thread(target=consumer, args=(queue_password, ))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print(f'[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] BruteForceAES执行完毕!')