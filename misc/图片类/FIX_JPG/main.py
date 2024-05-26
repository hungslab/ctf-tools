import os
import time
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-f", type=str, default=None, required=True,
                    help="输入同级目录下图片的名称")
parser.add_argument("-n", type=int, default=2, required=False,
                    help="输入放大的倍数 (默认: 2倍)")
args  = parser.parse_args()


if __name__ == '__main__':
    filePath = os.path.abspath(args.f)
    shfflePath, ext = os.path.splitext(filePath)
    shffleName = shfflePath.split("\\")[-1]
    
    with open(filePath, "rb") as f:
        data = f.read()

    if (index := data.rfind(b"\xff\xc0\x00\x11\x08")) == -1:
        print("没有找到SOFx层!")
        time.sleep(0.5)
        exit(-1)
        
    index += 5
    height = int.from_bytes(data[index:index+2], byteorder="big", signed=False) * args.n
    
    out_data = data[:index] + height.to_bytes(2, byteorder="big", signed=False) + data[index+2:]
    with open("fix_1.jpg", "wb") as f:
        f.write(out_data)
    print(f"图像高度已经修改为了{args.n}倍!")
    time.sleep(0.5)
    
