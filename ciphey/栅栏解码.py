from base64 import *

def basedecode(cip):
    while 1:
        cip = cip[::-1]
        try:
            cip = b16decode(cip)
            continue
        except:
            pass
        try:
            cip = b32decode(cip)
            continue
        except:
            pass
        try:
            cip = b64decode(cip)
            continue
        except:
            pass
        return cip

def wzhalan(content, n):
    table = [['' for i in range(len(content))] for j in range(n)]
    x,y = 0,[i for i in range(n)]
    y.extend([j for j in range(n-2,0,-1)])
    co_ordinates = []   # 得到坐标
    for i in range(len(content)):
        co_ordinates.append((y[x%(2*n-2)],x))
        x += 1
    order = sorted(co_ordinates,key=lambda x:x[0])
    dic = {}
    for i in range(len(content)):
        dic[order[i]] = content[i]
    result = ""
    for i in co_ordinates:
        result += dic[i]
    return result


if __name__ == '__main__':
    file = open('./edocnEesaB.txt','r')
    cip = file.readline()
    content = basedecode(cip).decode()
    for n in range(2,len(content)+1,1):
         result = wzhalan(content,n)
         print(result)
