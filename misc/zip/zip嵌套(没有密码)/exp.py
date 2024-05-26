import io
import zipfile

with open("110111.zip", "rb") as f:
    data = f.read()

info = "110111"

while True:
    with zipfile.ZipFile(io.BytesIO(data), "r") as zf:
        all_files_processed = True
        for i in zf.filelist:
            fileName = i.filename.encode("cp437").decode("gbk")
            if zipfile.is_zipfile(io.BytesIO(zf.read(i.filename))):
                print(fileName)
                data = zf.read(i.filename)
                all_files_processed = False
                
                info += f" {fileName.replace('.zip', '')}"
            else:
                print(fileName)
                with open(fileName, "wb") as f:
                    f.write(zf.read(i.filename))

        if all_files_processed:
            break

print(info)