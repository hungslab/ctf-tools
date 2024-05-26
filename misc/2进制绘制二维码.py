import os
import cv2
import time
import shutil
import argparse
import numpy as np


parser = argparse.ArgumentParser()
parser.add_argument('-f', type=str, default=None, required=True,
                    help='输入文件名称')
parser.add_argument('-size', type=int, default=1,
                    help='图片放大倍数(默认1倍)')
args = parser.parse_args()

file_path = os.path.join(args.f)

saveDir = "./out"
if os.path.exists(saveDir):
    shutil.rmtree(saveDir, ignore_errors=True)
os.makedirs(saveDir)

def crete_img(bin_str):
    np_arr = np.frombuffer(bin_str.encode(), dtype=np.uint8) - ord('0') # 使用 - ord('0') 将 ASCII 码值为 48 的字符 '0' 转换为整数 0，将 ASCII 码值为 49 的字符 '1' 转换为整数 1。

    img = np_arr.copy()
    img[img==1] = 255

    invert_img = np_arr.copy()
    invert_img[img==0] = 255
    invert_img[img==1] = 0
    return img, invert_img

if __name__ == '__main__':
    size = args.size
    
    with open(file_path, "r") as f:
        bin_str = f.read().strip()

    img, invert_img = crete_img(bin_str)
    
    dic = {X: int(len(bin_str) / X) for X in range(1, len(bin_str)) if len(bin_str) % X == 0}
    for row, col in dic.items():
        save_img = img.reshape(row, col)
        save_invert_img = invert_img.reshape(row, col)

        if size > 1:
            save_img = cv2.resize(save_img, None, fx=size, fy=size, interpolation=cv2.INTER_AREA)
            save_invert_img = cv2.resize(save_invert_img, None, fx=size, fy=size, interpolation=cv2.INTER_AREA)
        
        cv2.imwrite(f"./{saveDir}/{col}_{row}.png", save_img)
        cv2.imwrite(f"./{saveDir}/{col}_{row}_inverse.png", save_invert_img)
        print(f"[-] 宽度:{col:6} 高度:{row:6}, 已保存在运行目录out中...")
    print("[-] 已经遍历完所有情况, 即将自动关闭!")
    time.sleep(0.5)
