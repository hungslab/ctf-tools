# Arnold

# Usage

```
$ python main.py -h
usage: main.py [-h] -t {encode,decode} -f F [-n N] [-a A] [-b B]

optional arguments:
  -h, --help          show this help message and exit
  -t {encode,decode}  encode | decode
  -f F                输入文件名称
  -n N                输入参数n
  -a A                输入参数a
  -b B                输入参数b
```

# Example

1. 知道 `n和a和b`

```
$ python .\main.py -f .\demo\catcat_7_100_100.png -t decode -n 7 -a 100 -b 100
$ python .\main.py -f .\demo\encode_1_31_13.png -t decode -n 1 -a 31 -b 13
$ python .\main.py -f .\demo\girlfriend_0x61_0x726e_0x6f6c64.png -t decode -n 0x61 -a 0x726e -b 0x6f6c64
$ python .\main.py -f .\demo\sictf2023_2_1_2.bmp -t decode -n 2 -a 1 -b 2
```

2. 不知道 `n和a和b`

```
$ python .\main.py -f .\demo\sictf2023_2_1_2.bmp -t decode
请输入n的范围 (如:1-10, 回车默认为1): 1-5
请输入a的范围 (如:1-10, 回车默认为1-10): 1-5
请输入b的范围 (如:1-10, 回车默认为1-10): 1-5
```

<img src="./images/image.png">
