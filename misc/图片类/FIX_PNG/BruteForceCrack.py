import os
import zlib
import struct

# 老铜匠
def crack_no_inter(bt_ch, width, data, tmppath, chuncks):
    interlace = b'\x00'  # 首先考虑逐行扫描的情况
    for i in bt_ch:
        # print('当前处理的值是：{}'.format(i))
        for w in range(width):
            colortype = i[0]
            colorchannel = i[1]
            bits = i[2]
            scanline = bits * colorchannel * w // 8 + 1
            if len(data) % scanline == 0:
                data1 = list(data[::(bits * colorchannel * w // 8 + 1)])

                if set(data1).issubset(b'\x00\x01\x02\x03\x04') and len(data1) != 1:  # 如果每片的头部合集都在，0,1,2,3,4以内，就说明切片可能正确，得到宽度

                    # print(w, len(data1), colortype, ':', colorchannel, ':', bits)
                    head = b'\x89\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d\x49\x48\x44\x52' + \
                        w.to_bytes(4,'big') + len(data1).to_bytes(4, 'big') + \
                        bits.to_bytes(1, 'big') + colortype.to_bytes(1,'big') + b'\x00\x00' + interlace
                    headcrc = zlib.crc32(head[12:])
                    head = head + headcrc.to_bytes(4, 'big')
                    print(f"[-] 宽度: {w}, hex: {hex(w)}")
                    print(f"[-] 高度: {len(data1)}, hex: {hex(len(data1))}\n")
                    with open(f"{tmppath}{w}X{len(data1)}_{colortype}_{colorchannel}_{bits}.png", 'wb') as fw:
                        fw.write(head + b''.join(chuncks))
                elif len(data1) == 1:
                    break
    # print('逐行扫描完成，请在output目录下查看是否有正常显示的图片，下面开始隔行扫描，先考虑常见的色彩模式(非灰度)，分辨率在2000x2000以内')

def pngbaoli_def(filename):
    file = filename
    fr = open(file, 'rb').read()
    tmppath = './output/'
    if not os.path.exists(tmppath):
        os.mkdir(tmppath)
    # print(tmppath)
    chunckid = [b'IHDR', b'PLTE', b'IDAT', b'IEND', b'cHRM', b'gAMA', b'iCCP', b'sBIT', b'sRGB', 
                b'bKGD', b'hIST', b'tRNS', b'pHYs', b'sPLT', b'tIME', b'iTXt', b'tEXt', b'zTXt']
    chuncks = []
    i = 4
    while i < len(fr):
        if fr[i:i + 4] in chunckid:
            try:
                datalen, dataname = struct.unpack(">I4s", fr[i - 4:i + 4])
                dataformat = f'>I4s{str(datalen)}s4s'
                datalen, dataname, data, datacrc = struct.unpack(dataformat, fr[i - 4:i - 4 + 8 + datalen + 4])
                realcrc = zlib.crc32(dataname + data).to_bytes(4, 'big')
                if realcrc != datacrc:
                    datacrc = realcrc
                    # print(dataname, 'crc32 fixed')
                # print(datalen, bytes.decode(dataname, encoding='utf-8'), hex(int.from_bytes(datacrc, 'big')))
                chuncks.append(fr[i - 4:i - 4 + 8 + datalen] + realcrc)
                i = i + 8 + datalen + 4  # 最少加一，防止出现iend
            except Exception:
                # 防止不能解析的结构体中出现png chunckid的关键字，指针直接指向下一个。
                i += 1
                continue
        else:
            i += 1

    for chk in chuncks:  # 直接丢弃IHDR头部
        if chk[4:8] == b'IHDR':
            chuncks.remove(chk)

    blocks = [tmp[8:int.from_bytes(tmp[:4], 'big') + 8] for tmp in chuncks if tmp[4:8] == b'IDAT']
    blocks = b''.join(blocks)  # 组合数据
    data = zlib.decompressobj().decompress(blocks)  # 解码zlib得到像素（含filter）
    bt_ch_my = [(2, 3, 8)]  # 比较常用的2,3,8
    crack_no_inter(bt_ch_my, 10001, data, tmppath, chuncks)
    bt_ch_my = [(6, 4, 8)]  # 比较常用的6,4,8
    crack_no_inter(bt_ch_my, 10001, data, tmppath, chuncks)