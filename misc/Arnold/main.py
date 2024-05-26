import os
import cv2
import argparse
import numpy as np
from core import ImageCore, PathCore


parser = argparse.ArgumentParser()
parser.add_argument('-t', type=str, default=None, required=True, choices=["encode", "decode"],
                    help='encode | decode')
parser.add_argument('-f', type=str, default=None, required=True,
                    help='输入文件名称')
parser.add_argument('-n', type=str, default=1, required=False,
                    help='输入参数n')
parser.add_argument('-a', type=str, default=None, required=False,
                    help='输入参数a')
parser.add_argument('-b', type=str, default=None, required=False,
                    help='输入参数b')
args  = parser.parse_args()


# def arnold(img, n, a, b):
#     new_img = np.zeros((r, c, 3), np.uint8)

#     for _ in range(n):
#         for i in range(r):
#             for j in range(c):
#                 x = (i + b * j) % r
#                 y = (a * i + (a * b + 1) * j) % c
#                 new_img[x, y] = img[i, j]
#         img = np.copy(new_img)
#     return new_img

# def dearnold(img, n, a, b):
#     new_img = np.zeros((r, c, 3), np.uint8)

#     for _ in range(n):
#         for i in range(r):
#             for j in range(c):
#                 x = ((a * b + 1) * i - b * j) % r
#                 y = (-a * i + j) % c
#                 new_img[x, y] = img[i, j]
#         img = np.copy(new_img)
#     return new_img

def arnold(img, n, a, b, r, c, copy=True):
    new_img = np.empty_like(img, np.uint8)

    for _ in range(n):
        y, x = np.meshgrid(np.arange(c), np.arange(r))
        new_x = (x + b * y) % r
        new_y = (a * x + (a * b + 1) * y) % c
        new_img[new_x, new_y] = img
        img = np.copy(new_img)
        if copy:
            img = np.copy(new_img)
    return new_img

def dearnold(img, n, a, b, r, c, copy=True):
    new_img = np.empty_like(img, np.uint8)

    for _ in range(n):
        y, x = np.meshgrid(np.arange(c), np.arange(r))
        new_x = ((a * b + 1) * x - b * y) % r
        new_y = (-a * x + y) % c
        new_img[new_x, new_y] = img
        if copy:
            img = np.copy(new_img)
    return new_img

def saveImage(new_img, savePath):
    savaPath = os.path.join(saveDir, savePath)
    ImageCore.save_img(savaPath, new_img, ext=".png")
        
def start(img_path, n, a, b):
    img = ImageCore.read_img(img_path, cv2.IMREAD_UNCHANGED)
    r, c = img.shape[:2]
    
    img_copy = img.copy()
    if args.t == "encode":
        new_img = arnold(img_copy, n, a, b, r, c, copy=False)
        if n != 1:
            new_img_copy = arnold(img_copy, n, a, b, r, c)
    elif args.t == "decode":
        new_img = dearnold(img_copy, n, a, b, r, c, copy=False)
        if n != 1:
            new_img_copy = dearnold(img_copy, n, a, b, r, c)

    savePath = f"{file_name}_n{n}_a{a}_b{b}.png"
    saveImage(new_img, savePath)
    
    if n != 1:
        saveCopyPath = f"{file_name}_n{n}_a{a}_b{b}_copy.png"
        saveImage(new_img_copy, saveCopyPath)


def bruteForce(img_path):
    if n := input("请输入n的范围 (如:1-10, 回车默认为1): "):
        n_lis = list(map(lambda x: int(x), n.split("-")))
    else:
        n_lis = [1, 2]

    if a := input("请输入a的范围 (如:1-10, 回车默认为1-10): "):
        a_lis = list(map(lambda x: int(x), a.split("-")))
    else:
        a_lis = [1, 10]
        
    if b := input("请输入b的范围 (如:1-10, 回车默认为1-10): "):
        b_lis = list(map(lambda x: int(x), b.split("-")))
    else:
        b_lis = [1, 10]

    for n in range(n_lis[0], n_lis[1]):
        for a in range(a_lis[0], a_lis[1]):
            for b in range(b_lis[0], b_lis[1]):
                start(img_path, n, a, b)

if __name__ == '__main__':
    img_path = os.path.abspath(args.f)
    saveDir = "./output"
    os.makedirs(saveDir, exist_ok=True)
    PathCore.clear_and_create_dir(saveDir)

    file_name = os.path.splitext(img_path)[0].split("\\")[-1]

    if args.a is None and args.b is None:
        bruteForce(img_path)
        exit(0)
    
    n, a, b = eval(args.n), eval(args.a), eval(args.b)
    start(img_path, n, a, b)

