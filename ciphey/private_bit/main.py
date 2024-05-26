import os
import argparse
from lxml import etree


parser = argparse.ArgumentParser()
parser.add_argument('-f', type=str, default=None, required=True,
                    help='输入MP3音频 (音频同目录需要有010editor导出的Xml文件!)')
parser.add_argument("-hex", nargs='?', const=True, default=False,
                    help="使用hex编码输出")
parser.add_argument("-bit", nargs='?', const=True, default=False,
                    help="使用bit编码输出")
args  = parser.parse_args()

def getInfo():
    with open(filePath, "rb") as f:
        for start in starts:
            f.seek(int(str(start)[:-1], 16), 0)
            data = f.read(4)
            yield [
                f"{data[i] >> n & 1}"
                for i, n in [[-2, 0], [-1, 3], [-1, 2]]
            ]

if __name__ == '__main__':
    filePath = os.path.abspath(args.f)
    baseDir = os.path.dirname(filePath)
    fileSuffix, ext = os.path.splitext(filePath)
    fileName = fileSuffix.split("\\")[-1]

    xmlPath = os.path.join(baseDir, f"{fileName}.xml")
    if not os.path.exists(xmlPath):
        print("没有找到010editor导出的xml文件!")
        exit(-1)

    with open(xmlPath, "rb") as f:
        root = etree.HTML(f.read())
    starts = root.xpath("//variable[starts-with(name, 'struct MPEG_FRAME mf')]/start/text()")

    res = {
        "private_bit": "",
        "copyright": "",
        "original": ""
    }

    for i in getInfo():
        res["private_bit"] += i[0]
        res["copyright"] += i[1]
        res["original"] += i[2]

    if args.bit:
        for key, value in res.items():
            print(f"{key} bits:\n{value}")
        print("")

    for key, value in res.items():
        data = bytes((int(value[i:i+8], 2)) for i in range(0, len(value), 8))
        print(f"{key}:")
        print(data.hex()) if args.hex else print(data)
    