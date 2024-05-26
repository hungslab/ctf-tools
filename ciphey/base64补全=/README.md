# 补全原理

base64编码后的字符串，每4字节一组。

---

例子：（下面的base64编码后的字符串都没有 `=` 符号）

| 编码后   | len  | 补全几个 `=` 符号        | 补全后   | 解码后 |
| -------- | ---- | ------------------------ | -------- | ------ |
| aGVsbA   | 6    | 4 - (6 % 4) = 2          | aGVsbA== | hell   |
| aGVsbG8  | 7    | 4 - (7 % 4) = 1          | aGVsbG8= | hello  |
| aGVsbG93 | 8    | 8 % 4 == 0，所以不需要补 | aGVsbG93 | hellow |



代码逻辑：

- 1.先用 `len % 4` 如果等于0，就说明不需要补`=`
- 2.`len % 4` 不等于0，就说明需要补`=`，末尾补全 `4 - (len % 4)` 位 `=`

---

Python代码：

```python
wf = open("base64_str补全=后.txt", "w")

with open("base64_str.txt", "r") as f:
    data = f.read()
    data = data.splitlines()

for line in data:
    missing_padding = len(line) % 4
    if missing_padding != 0:
        line += "=" * (4 - missing_padding)
    wf.write(line + "\n")
```

