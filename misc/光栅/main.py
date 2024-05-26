import os
import cv2
import argparse
import numpy as np
from core import ImageCore, PathCore

parser = argparse.ArgumentParser()
parser.add_argument('-f', type=str, default=None, required=True,
                    help='输入文件名称')
parser.add_argument('-frame', type=int, default=5, required=False,
                    help='输入从2开始爆破帧数（default:5）')
parser.add_argument('-n', type=int, default=1, required=False,
                    help='输入像素个数（default:1）')
args  = parser.parse_args()


if __name__ == '__main__':
    filePath = os.path.abspath(args.f)
    img = ImageCore.read_img(filePath, cv2.IMREAD_COLOR)
    row, col = img.shape[:2]
    _, fileName, saveDir = PathCore.get_save_info(filePath)
    PathCore.clear_and_create_dir(saveDir)

    for frame in range(2, args.frame+1):
        black_num = frame * args.n - args.n
        white_num = args.n
        
        img_copy = np.copy(img)
        for x in range(0, col, black_num+white_num):
            cv2.rectangle(img_copy, (x, 0), (x+black_num-1, row), color=0, thickness=-1)
        
        ImageCore.save_img(os.path.join(saveDir, f"frame&{frame}_black_num&{black_num}_white_num&{white_num}.png"), img_copy, ext=".png")
        print(f"帧数: {frame}, 黑色像素块: {black_num}, 白色像素块: {white_num}")
        