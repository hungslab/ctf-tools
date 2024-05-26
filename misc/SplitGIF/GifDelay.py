import os
import imageio
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-f", type=str, default=None, required=True,
                    help="输入同级目录下文件的名称")
args  = parser.parse_args()


if __name__ == '__main__':
    gif_path = os.path.abspath(args.f)

    output = []
    with imageio.get_reader(gif_path) as gif:
        for _ in gif:
            meta = gif.get_meta_data()
            delay_times = meta['duration']
            output.append(f"{delay_times}")
    print(output)