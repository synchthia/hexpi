#!/usr/bin/env python3

import sys
from util import ir

if len(sys.argv) < 2:
    print("Usage: hexpi <gpio> <signal...>")
    sys.exit(0)

# default = 2
gpio = int(sys.argv[1])
signal = list(map(int, sys.argv[2:]))

ir.send(gpio, signal)
