import os
import time
import math
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-f", type=str, default=None, required=True,
                    help="输入同级目录下图片的名称")
args  = parser.parse_args()

SAVE_DIR = os.getcwd()

def save_img(data, width=None, height=None, sqrt_num=None):
    with open(os.path.join(SAVE_DIR, "fix_width.bmp"), "wb") as f:
        f.write(data[:0x12] + width.to_bytes(4, byteorder="little", signed=False) + data[0x16:])

    with open(os.path.join(SAVE_DIR, "fix_height.bmp"), "wb") as f:
        f.write(data[:0x16] + height.to_bytes(4, byteorder="little", signed=False) + data[0x1a:])

    with open(os.path.join(SAVE_DIR, "fix_sqrt.bmp"), "wb") as f:
        f.write(data[:0x12] + sqrt_num.to_bytes(4, byteorder="little", signed=False) * 2 + data[0x1a:])

def get_pixels_size(data):
    bfSize = int.from_bytes(data[0x2:0x2+4], byteorder="little", signed=False)
    bfOffBits = int.from_bytes(data[0xa:0xa+4], byteorder="little", signed=False)
    biBitCount = int.from_bytes(data[0x1c:0x1c+2], byteorder="little", signed=False)
    channel = biBitCount // 8
    # 由于宽高都会被修改，所以我计算出来的Padding_size也不是正确的，没有意义
    # padding_size = (4 - col * channel % 4) * row if col * channel % 4 != 0 else 0
    # pixels_size = (bfSize - bfOffBits - padding_size) // channel
    return (bfSize - bfOffBits) // channel


if __name__ == '__main__':
    file_path = os.path.abspath(args.f)
    if  os.path.splitext(args.f)[-1] != ".bmp":
        print("您的文件后缀名不为BMP!")
        time.sleep(1)
        exit(-1)

    with open(file_path, "rb") as f:
        data = f.read()
    col = abs(int.from_bytes(data[0x12:0x12+4], byteorder="little", signed=True))
    row = abs(int.from_bytes(data[0x16:0x16+4], byteorder="little", signed=True))
    pixels_size = get_pixels_size(data)

    width, height = pixels_size // row, pixels_size // col
    sqrt_num = int(math.sqrt((pixels_size)))
    save_img(data, width=width, height=height, sqrt_num=sqrt_num)

    print("温馨提示：由于填充字节的问题，所以可能会偏差几个像素!")
    print(f"1.修复宽度: {width}")
    print(f"2.修复高度: {height}")
    print(f"3.修复宽度高度为: {sqrt_num}")
    time.sleep(1)