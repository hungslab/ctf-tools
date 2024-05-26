# FIX_PNG

**关于项目：**

- 一部分是来自于铜匠师傅的代码
- 目前分为2种方式，如果crc32出错，就会遍历宽高爆破crc32相同的宽高；另一种情况是如果crc32相同会自动尝试铜匠师傅的代码（根据IDAT层的数据暴力爆破宽高）

<br>

**爆破流程：**

1. 第一次尝试，会默认宽度正确，爆破高度
2. 第二次尝试，会默认高度正确，爆破宽度
3. 第三次尝试，会爆破宽度和高度

<br>

# Usage

```
Usage: python .\main.py -f <xxx.png>
    example:
        python .\main.py -f .\demo\test.png
```

虽然使用了Go语言重构了，但是使用方式还是和以前一样，因为我用Python调用 `BrutePNG.exe`

<br>

# 效果

**正常情况：**

<img src="./images/python&go.png">

**暴力爆破：**

<img src="./images/image2.png">

<br>

# 优化思路

我将Python语言重构到了Go语言，针对大尺寸图片（1920*1080）的爆破，提升效果如下：

Go：爆破高度 `1ms`，爆破宽度 `2ms`，爆破高度和宽度 `189ms`；Python：爆破宽度和高度 `12s`

<img src="./images/python&go.png">

<img src="./images/python.png">
