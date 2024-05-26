import os
import tools
import argparse
import numpy as np
import matplotlib.pyplot as plt


parser = argparse.ArgumentParser()
parser.add_argument("-f", type=str, default=None, required=True,
                    help="输入同级目录下的名称")
parser.add_argument("-show", type=int, default=None, required=False,
                    help="单独显示某个(1.LEFT/MOVE_LEFT, 2.RIGHT/MOVE_RIGHT, 3.ALL/MOVE_ALL)")
args  = parser.parse_args()

TITLE = ["LEFT", "RIGHT", "ALL", "MOVE_LEFT", "MOVE_RIGHT", "MOVE_ALL"]
FILE_PATH = os.path.abspath(args.f)

def read_file():
    if FILE_PATH.endswith(".txt"):
        with open(FILE_PATH, "r") as f:
            data = f.read().splitlines()
    else:
        data = tools.get_data(FILE_PATH)
    return data

def get_pos(mode, btn_mode):
    posx, posy = 0, 0
    pos_left, pos_right, pos_all = [], [], []
    for line in data:

        if mode:
            if len(line) <= 8:
                continue
            x, y = int(line[4:6], 16), int(line[8:10], 16)
        else:
            x, y = int(line[2:4], 16), int(line[5:7], 16)

        if x > 127:
            x -= 256
        if y > 127:
            y -= 256
        posx += x
        posy += y
        # 1 for left , 2 for right , 0 for nothing
        btn_flag = int(line[2:4], 16) if btn_mode else int(line[:2], 16)
        if btn_flag == 1:  # 1 代表左键，2代表右键
            pos_left.append((posx, -posy))
            pos_all.append((posx, -posy))
        elif btn_flag == 2:
            pos_right.append((posx, -posy))
            pos_all.append((posx, -posy))
    return [np.array(pos_left), np.array(pos_right), np.array(pos_all)]

def plot_point(arr, axes, move=False):
    if arr.size != 0:
        axes.plot(arr[:, 0], arr[:, 1], c='purple') if move else axes.scatter(arr[:, 0], arr[:, 1], s=10, c='purple', marker="x")

def printInfo(mode, btn_mode, info):
    all_pos = get_pos(mode, btn_mode)
    if len(list(filter(lambda x: x.size == 0, all_pos))) == 3:
        print("当前模式为空, 已经自动帮您跳过!")
        return
    
    _, axes = plt.subplots(2, 3, figsize=(15, 8))
    for i in range(len(axes)):
        for j in range(len(axes[i])):
            ax = axes[i][j]
            count = i * 3 + j
            ax.set_title(TITLE[count])
            if count < 3:
                plot_point(all_pos[count%3], ax)
            else:
                plot_point(all_pos[count%3], ax, move=True)
    
    print(info)
    plt.tight_layout()
    plt.show()
    
def showInfo(mode, btn_mode, info):
    all_pos = get_pos(mode, btn_mode)
    
    if args.show in [1, 2, 3, 4, 5, 6]:
        arr = all_pos[args.show%3-1]
        if arr.size == 0:
            print("当前模式为空, 已经自动帮您跳过!")
            return
        
        _ = plt.figure(figsize=(15, 8))
        if args.show < 3 :
            plt.scatter(arr[:, 0], arr[:, 1], s=10, c='purple', marker="x")
        else:
            plt.plot(arr[:, 0], arr[:, 1], c='purple')
            
    print(info)
    plt.tight_layout()
    plt.show()
    
if __name__ == '__main__':
    data = read_file()
    
    if args.show:
        showInfo(False, False, "模式1绘制完毕!")
        showInfo(True, False, "模式2绘制完毕!")
        showInfo(False, True, "模式3绘制完毕!")
        showInfo(True, True, "模式4绘制完毕!")
    else:
        printInfo(False, False, "模式1绘制完毕!")
        printInfo(True, False, "模式2绘制完毕!")
        printInfo(False, True, "模式3绘制完毕!")
        printInfo(True, True, "模式4绘制完毕!")