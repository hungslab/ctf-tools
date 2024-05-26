import io
import re
import rarfile

rarfile.UNAR_TOOL = "./UnRAR.exe"

with open("./500.txt", "r") as f:
    password_data = f.read()

with open('500.rar', 'rb') as f:
    data = f.read()
    
def getPassword(password_data):
    return str(eval(password_data)).encode()

while True:
    with rarfile.RarFile(io.BytesIO(data), 'r') as rf:
        isClose = True
        for f in rf.infolist():
            # 如果是文件，则打印出文件名
            fileName = f.filename
            pwd = getPassword(password_data)
            if fileName.endswith(".rar"):
                print(fileName, pwd)
                data = rf.read(fileName, pwd=pwd)
                isClose = False
            elif re.search('\d+.txt', fileName):
                password_data = rf.read(fileName, pwd=pwd)
            else:
                print(fileName)
                rf.extract(fileName, ".", pwd=pwd)
        
        if isClose:
            exit()