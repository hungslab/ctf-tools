import pyshark

def find_flag():
    cap = pyshark.FileCapture("modbus-alarm.pcapng")
    idx = 1
    for c in cap:
        for pkt in c:
            if pkt.layer_name == "modbus" and int(pkt.func_code) == 6:
                payload = str(c["TCP"].payload).replace(":", "")
                print(hex_to_ascii(payload))
                print("{0} *".format(idx))
        idx += 1
def hex_to_ascii(payload):
    data = payload
    flags = []
    for d in data:
        _ord = ord(d)
        if (_ord > 0) and (_ord < 128):
            flags.append(chr(_ord))
    return ''.join(flags)

if __name__ == '__main__':
    find_flag()