#!/usr/bin/python3

import logging
import os
import time
import pigpio

def send(gpio: int, signal: []) -> None:
    """ Send IR Signal """

    if os.getenv("NO_IR_SEND", "") != "":
        logging.warning("NO_IR_SEND provided. IR Signal won't send.")
        return

    try:
        pi = pigpio.pi()
        freq = 38.0
        pi.set_mode(gpio, pigpio.OUTPUT)
    except:
        raise Exception("Failed communicate to pigpio.")

    pi.wave_add_new()

    emit_time = time.time()
    marks_wid = {}
    spaces_wid = {}
    wave = [0]*len(signal)

    for i in len(signal):
        ci = signal[i]
        if i & 1:
            if ci not in spaces_wid:
                pi.wave_add_generic([pigpio.pulse(0, 0, ci)])
                spaces_wid[ci] = pi.wave_create()
            wave[i] = spaces_wid[ci]
        else:
            if ci not in marks_wid:
                wf = carrier(gpio, freq, ci)
                pi.wave_add_generic(wf)
                marks_wid[ci] = pi.wave_create()
            wave[i] = marks_wid[ci]

    delay = emit_time - time.time()
    if delay > 0.0:
        time.sleep(delay)

    pi.wave_chain(wave)

    while pi.wave_tx_busy():
        time.sleep(0.002)

    gap_s = 100 / 1000.0
    emit_time = time.time() + gap_s

    for i in marks_wid:
        pi.wave_delete(marks_wid[i])
    marks_wid = {}

    for i in spaces_wid:
        pi.wave_delete(spaces_wid[i])
    spaces_wid = {}

    pi.stop()
    return

def carrier(gpio, frequency, micros) -> []:
    wf = []
    cycle = 1000.0 / frequency
    cycles = int(round(micros/cycle))
    on = int(round(cycle / 2.0))
    sofar = 0
    for c in range(cycles):
        target = int(round((c+1)*cycle))
        sofar += on
        off = target - sofar
        sofar += off
        wf.append(pigpio.pulse(1<<gpio, 0, on))
        wf.append(pigpio.pulse(0, 1<<gpio, off))
    return wf
