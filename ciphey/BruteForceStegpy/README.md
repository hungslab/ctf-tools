# BruteForceStegpy

## Usage

```
$ python .\main.py -h
usage: main.py [-h] -f F -d D [-p P]

optional arguments:
  -h, --help  show this help message and exit
  -f F        输入文件名称
  -d D        输入字典的文件名称
  -p P        线程数

example:
	python .\main.py -f .\demo\top1000.png -d .\demo\top1000.txt
	python .\main.py -f .\demo\top10000.png -d .\demo\top10000.txt
```

## 演示

```
$ python .\main.py -f .\demo\top1000.png -d .\demo\top1000.txt
[2023-05-28 02:06:26] 开始执行, 使用线程数: 20.
Find Password: freepass, Message: flag{this_is_flag}
[2023-05-28 02:06:29] BruteForceAES执行完毕!
```

支持 `rockyou` 这种大字典：

```
$ python .\main.py -f .\demo\keyiscassandra.png -d .\demo\rockyou.txt
[2023-05-28 02:08:05] 开始执行, 使用线程数: 20.
Find Password: cassandra, Message: flag{this_is_flag}
[2023-05-28 02:08:17] BruteForceAES执行完毕!
```

