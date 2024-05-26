import os
import re
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-f", type=str, default=None, required=True,
                    help="输入同级目录下图片的名称")
args  = parser.parse_args()

if __name__ == '__main__':
    file_path = os.path.abspath(args.f)

    with open(file_path, "r", encoding='utf-8') as f:
        data = f.read()

    print(set(re.findall('[^a-zA-Z0-9,<.>/?;:\'\"\[\]{}\\\|`~!@#$%^&*()_\-+= \t\n\r\f\v，《。》？；：’‘”“【】、·！—\u4e00-\u9fa5]', data)))
    os.system('pause')