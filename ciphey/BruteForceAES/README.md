# BruteForceAES

## Usage

1. 修改代码里面的 `enc` 参数为 `base64` 字符串

```
Usage: $ python .\BruteForceAES.py -d <wordlistsPath> -v <冰蝎流量版本(默认3)>
    example:
        python .\BruteForceAES.py -d .\wordlists\Byxs20_top2w5.txt
        python .\BruteForceAES.py -d .\wordlists\Byxs20_top2w5.txt -v 3
        python .\BruteForceAES.py -d .\wordlists\Byxs20_top2w5.txt -v 4
```

```
$ python .\BruteForceAES.py -d .\wordlists\Byxs20_top2w5.txt -v 3
[2023-04-25 20:53:38] 开始爆破, 线程数: 20.
Find Password: enjoy, AES key: 76e369257240ded4, Message: b'{"status":"c3VjY2Vzcw==","msg":""}'
[2023-04-25 20:53:39] 爆破结束!
```