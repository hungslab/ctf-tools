import hashlib

plaintext = "flag{#00#_P4ssw0rd_N3v3r_F0rg3t_63####}"

Dic = [chr(i) for i in range(97, 123)]  # 小写字母
dic = [chr(i) for i in range(65, 91)]  # 大写字母
num = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
for i in range(len(Dic)):
    for j in range(len(dic)):
        for a in range(len(num)):
            for b in range(len(num)):
                for c in range(len(num)):
                    m = 'flag{' + Dic[i] + '00' + dic[j] + '_P4ssw0rd_N3v3r_F0rg3t_63' + num[a] + num[b] + num[c]
                    md5 = hashlib.md5(m.encode('utf-8')).hexdigest()
                    if md5 == 'ac7f4d52c3924925aa9c8a7a1f522451':
                        print(m, md5)
