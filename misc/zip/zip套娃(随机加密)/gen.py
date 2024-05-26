import random
import pyminizip
import os


# 压缩文件的路径
file_to_zip = "flag.txt"

# 压缩后的文件名
zip_file_name = "第一层.zip"

# 压缩文件的密码
password = str(random.randint(9,99999))
print("pwd:",password)
# 使用pyminizip创建带有密码的压缩包
pyminizip.compress(file_to_zip, None, zip_file_name, password, 5)

for i in range(999):
    file_to_zip = zip_file_name
    file_name_to_remove = zip_file_name
    # 压缩后的文件名
    zip_file_name = str(random.randint(9,99999)) + ".zip"

    # 压缩文件的密码
    password = str(random.randint(9,99999))

    print("pwd:",password)
    # 使用pyminizip创建带有密码的压缩包
    pyminizip.compress(file_to_zip, None, zip_file_name, password, 5)

    print("zip_file_name",zip_file_name)

    os.remove(file_name_to_remove)

print("done")

