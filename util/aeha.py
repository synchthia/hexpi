#!/usr/bin/python3

def toCode(T, byte, interval):
    code = []
    i = 0
    length = len(byte)

    # byte[ 0, 1, 2 ]
    for i in range(length):
        c = byte[i]
        v0 = T*8
        v1 = T*4
        code.append(int(v0))
        code.append(int(v1))

        # byte[ 0:[0, 1, ....] ]
        for j in range(len(c)):
            for k in range(8):
                if (c[j] & (1 << k)) != 0:
                    v3 = T*3
                    code.append(int(T))
                    code.append(int(v3))
                else:
                    code.append(int(T))
                    code.append(int(T))
        if i >= length-1:
            code.append(int(T))
            i = i + 1
            cont = 0
        else:
            code.append(int(interval))
            code.append(int(interval))
        i = i + 1
    return code
