#!/usr/bin/env python3

import sys
import os
from util import ir, aeha
import web

if len(sys.argv) < 3:
    print("Usage: hexpi <gpio> <http|hex|ir> [code...]")
    sys.exit(0)

# default = 2
gpio = int(sys.argv[1])
mode = sys.argv[2]
signal = []
if mode == "http":
    port = os.getenv("HTTP_PORT")
    if port is None:
        port = "8081"
    web.start(port)

elif mode == "hex":
    def f(n):
        return int(n, 0)
    for s in sys.argv[3:]:
        hexCode = list(map(f, s.split(",")))
        signal.append(hexCode)

    signal = aeha.toCode(430, signal, 13300)
elif mode == "ir":
    signal = list(map(int, sys.argv[3:]))

ir.send(gpio, signal)
