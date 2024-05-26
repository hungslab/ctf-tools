import os
import cv2
import time
import argparse
from tqdm import tqdm
from core import PathCore, ImageCore


parser = argparse.ArgumentParser()
parser.add_argument("-f", type=str, default=None, required=True,
                    help="输入同级目录下文件的名称")
args  = parser.parse_args()

if __name__ == '__main__':
    gifPath = os.path.abspath(args.f)
    _, _, saveDir = PathCore.get_save_info(gifPath)
    PathCore.clear_and_create_dir(saveDir)

    gif = cv2.VideoCapture(gifPath)
    n_frames = gif.get(cv2.CAP_PROP_FRAME_COUNT)

    with tqdm(range(int(n_frames)), desc="Save Image") as bar:
        for i in bar:
            ret, frame = gif.read() # 读取当前帧图像
            if ret:
                ImageCore.save_img(os.path.join(saveDir, f"{i}.png"), frame, ext='.png')
            else:
                print("获取某一帧图像出现错误!")
                break
            
    gif.release() # 释放资源
    print("Split GIF Successful!")
    time.sleep(0.5)