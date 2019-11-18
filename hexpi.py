#!/usr/bin/env python3

import sys
import os
from util import ir, aeha
import web
import logging

# Logging
LOG_LEVEL = logging.INFO
if os.getenv("DEBUG", "") != "":
    LOG_LEVEL = logging.DEBUG

logging.basicConfig(
        format='[%(asctime)s] [%(levelname)s] %(message)s',
        datefmt='%Y/%m/%d %H:%M:%S %z',
        level=LOG_LEVEL
)

if len(sys.argv) < 3:
    print("Usage: hexpi <gpio> <http|hex [code...]|ir [signals...]>")
    sys.exit(0)

# default = 2
gpio = int(sys.argv[1])
mode = sys.argv[2]
signal = []
if mode == "http":
    port = os.getenv("HTTP_PORT")
    if port is None:
        port = "8081"
    web.start(port, gpio)

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
