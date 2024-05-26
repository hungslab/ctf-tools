import mmap
import time


def read_large_file(file_path):
    # 使用mmap映射文件
    with open(file_path, "r+b") as f:
        with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
            while True:
                yield mm.readline().rstrip(b"\r\n")
                if mm.tell() == len(mm):
                    break


if __name__ == '__main__':
    dic_path = "./demo/top10000.txt"

    t0 = time.time()
    for _ in range(1000):
        dic_list = list(read_large_file(dic_path))
    print(time.time() - t0)

    t0 = time.time()
    dic_list = []
    for _ in range(1000):
        with open(dic_path, "r", encoding="latin1") as f:
            while line := f.readline():
                dic_list.append(line.strip())
    print(time.time() - t0)
    
    