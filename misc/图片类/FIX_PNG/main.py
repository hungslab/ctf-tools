import os
import zlib
import time
import argparse
import subprocess
import BruteForceCrack


parser = argparse.ArgumentParser()
parser.add_argument("-f", type=str, default=None, required=True,
                    help="输入同级目录下图片的名称")
args  = parser.parse_args()

PNG_NAME = args.f.split("\\")[-1]
PNG_DIR = os.path.abspath(args.f)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# import struct, datetime, itertools

# def calculation_crc32(width, height):
#     return zlib.crc32(data[12:16] + struct.pack('>i', width) + struct.pack('>i', height) + data[24:29])

# def save_png(width, height):
#     with open(os.path.join(BASE_DIR, f"fix_{PNG_NAME}"), "wb") as f:
#         end = datetime.datetime.now()
#         duration = end - start
#         hours, remainder = divmod(duration.seconds, 3600)
#         minutes, seconds = divmod(remainder, 60)
#         milliseconds = duration.microseconds // 1000
#         print(f"[-] 宽度: {width}, hex: {hex(width)}")
#         print(f"[-] 高度: {height}, hex: {hex(height)}")
#         print(f"[-] 运行时间为：{hours}小时 {minutes}分钟 {seconds}秒 {milliseconds}毫秒")
#         print(f"[-] CRC32: {hex(original_crc32)}, 已经为您保存到运行目录中!")
#         f.write(data[:16] + struct.pack(">i", width) + struct.pack(">i", height) + data[24:])
#     time.sleep(1)
#     exit()

if __name__ == '__main__':
    data = open(PNG_DIR, 'rb').read()
    crc32key = zlib.crc32(data[12:29]) # 计算crc
    original_width, original_height = int.from_bytes(data[0x10:0x10+4], byteorder="big", signed=False), int.from_bytes(data[0x14:0x14+4], byteorder="big", signed=False)
    original_crc32 = int(data[29:33].hex(), 16) # 原始crc

    if os.path.splitext(PNG_NAME)[1] != ".png":
        print("[-] 您的文件后缀名不为PNG!")
        time.sleep(1)
        exit(-1)

    if crc32key == original_crc32: # 计算crc对比原始crc
        print("[-] 计算CRC32, 宽高没有问题, 开始尝试暴力破解!(感谢老铜匠)")
        BruteForceCrack.pngbaoli_def(args.f)
    else:
        executablePath = os.path.join(BASE_DIR, "BrutePNG", "BrutePNG.exe")
        result = subprocess.run([f"{executablePath}", f"{PNG_DIR}"], capture_output=True)
        output = result.stdout.decode("utf-8")
        print(output)

    time.sleep(1)
    exit(0)
        
        # start = datetime.datetime.now()
        # print("[-] 爆破高度中...")
        # for height in range(0x1FFF):
        #     if calculation_crc32(original_width, height) == original_crc32:
        #         save_png(original_width, height)

        # print("[-] 爆破宽度中...")
        # for width in range(0x1FFF):
        #     if calculation_crc32(width, original_height) == original_crc32:
        #         save_png(width, original_height)

        # print("[-] 爆破宽度和高度中...")
        # for width, height in itertools.product(range(0x1FFF), range(0x1FFF)): # 理论上0x FF FF FF FF，但考虑到屏幕实际/cpu，0x1FFF就差不多了，也就是8191宽度和高度
        #     if calculation_crc32(width, height) == original_crc32: # 计算当图片大小为width:height时的CRC校验值，与图片中的CRC比较，当相同，则图片大小已经确定
        #         save_png(width, height)
