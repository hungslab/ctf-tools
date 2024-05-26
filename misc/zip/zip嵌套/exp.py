import io
import zipfile

with open("49183-secret.zip", "rb") as f:
    data = f.read()
    
all_files_processed = False  # 初始化标志变量

while True:
    with zipfile.ZipFile(io.BytesIO(data), "r") as zf:
        for i in zf.filelist:
            fileName = i.filename.encode("cp437").decode("gbk")
            if zipfile.is_zipfile(io.BytesIO(zf.read(i.filename))):
                data = zf.read(i.filename)
                print(i.filename)
                # if (extra := zf.getinfo(i.filename).extra):
                #     print(i.filename, extra)
                    
                # if (comment := zf.getinfo(i.filename).comment):
                #     print(i.filename, comment)
            else:
                all_files_processed = True
                with open(fileName, "wb") as f:
                    f.write(zf.read(i.filename))

        if all_files_processed:
            break