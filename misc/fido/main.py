import os
import sys
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-f", default=None, required=True, type=str,
                  help="请输入文件路径，没有目录会自动使用剪切板内容")
args = parser.parse_args()

if __name__ == '__main__':
    pyDir = os.path.dirname(sys.executable)
    fidoPath = os.path.join(pyDir, "Scripts", "fido.exe")

    filePath = os.path.abspath(args.f)
    
    os.system(f"{fidoPath} {filePath}")
    os.system("pause")
