import os
import binascii
import py_mini_racer

# 这个库的打包尤为麻烦，需要手动去改dll的代码

if __name__ == '__main__':
    with open("./js/rabbit.js", "r") as f:
        jsCode = f.read()
    
    crx = py_mini_racer.MiniRacer()
    crx.eval(jsCode)
    
    cipher = "U2FsdGVkX19bEN3D8vFeG39VyYXPwle2mMQLh5T1HYiSI1XCx7rJhsDnp9qLpUQByITd05Uu05ZAv0o="
    key = "Gui_1s_shumu"
    print(binascii.a2b_hex(crx.call("RabbitDecrypt", cipher, key)))
    os.system("pause")