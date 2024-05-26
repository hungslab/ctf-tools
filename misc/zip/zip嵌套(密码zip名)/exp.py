import io
import zipfile

with open("99020.zip", "rb") as f:
    data = f.read()
password = "99020.zip".split(".")[0].encode()



while True:
    with zipfile.ZipFile(io.BytesIO(data), "r") as zf:
        all_files_processed = True
        for i in zf.filelist:
            fileName = i.filename.encode("cp437").decode("gbk")
            if zipfile.is_zipfile(io.BytesIO(zf.read(i.filename, pwd=password))):
                print(fileName)
                data = zf.read(i.filename, pwd=password)
                password = i.filename.split(".")[0].encode()
                all_files_processed = False
            else:
                print(fileName)
                with open(fileName, "wb") as f:
                    f.write(zf.read(i.filename, pwd=password))

        if all_files_processed:
            break
