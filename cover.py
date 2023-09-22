
import logging
import time


from encode_tables import (
    NICE_FLOR_S_TABLE_ENCODE,
    NICE_FLOR_S_TABLE_KI,
)


tx_pulse_short = 500
tx_pulse_long = 1000
tx_pulse_sync = 1500
tx_pulse_gap = 15000
tx_length = 52

def tx_code(code: int):
    wf = []
    wf.extend(tx_sync())
    rawcode = format(code, "#0{}b".format(tx_length))[2:]
    for bit in range(0, tx_length):
        if rawcode[bit] == "1":
            wf.extend(tx_l0())
        else:
            wf.extend(tx_l1())
    wf.extend(tx_sync())
    wf.extend(tx_gap())
    return wf
def tx_l0():
    return [
        print(tx_pulse_short),
        print(tx_pulse_long),
    ]

def tx_l1():
    return [
        print(tx_pulse_long),
        print(tx_pulse_short),
    ]

def tx_sync():
    return [
        print(tx_pulse_sync),
        print(tx_pulse_sync),
    ]

def tx_gap():
    return [
        print(tx_pulse_gap),
    ]


def pair(button_id, code, serial):
        for _ in range(1, 10):
            _send_repeated(serial, button_id, code)

def send(serial: int, button_id: int, code: int):
    _send_repeated(serial, button_id, code)
    time.sleep(0.5)

def _send_repeated(serial: int, button_id: int, code: int):
    for repeat in range(1, 7):
        tx_code = _nice_flor_s_encode(serial, code, button_id, repeat)
        print("TX Code: ", hex(tx_code))

def encode(encbuff):
    encoded = 0
    encoded |= ((encbuff[6] << 0x4) & 0xF0) << 0
    encoded |= (((encbuff[5] & 0x0F) << 4) | ((encbuff[6] & 0xF0) >> 4)) << 8
    encoded |= (((encbuff[4] & 0x0F) << 4) | ((encbuff[5] & 0xF0) >> 4)) << 16
    encoded |= (((encbuff[3] & 0x0F) << 4) | ((encbuff[4] & 0xF0) >> 4)) << 24
    encoded |= (((encbuff[2] & 0x0F) << 4) | ((encbuff[3] & 0xF0) >> 4)) << 32
    encoded |= (((encbuff[1] & 0x0F) << 4) | ((encbuff[2] & 0xF0) >> 4)) << 40
    encoded |= (((encbuff[0] & 0x0F) << 4) | ((encbuff[1] & 0xF0) >> 4)) << 48
    encoded = encoded ^ 0xFFFFFFFFFFFFF0
    encoded = encoded >> 4
    return encoded

def _nice_flor_s_encode(
    serial: int, code: int, button_id: int, repeat: int
) -> int:
    snbuff = [None] * 4
    snbuff[0] = serial & 0xFF
    snbuff[1] = (serial & 0xFF00) >> 8
    snbuff[2] = (serial & 0xFF0000) >> 16
    snbuff[3] = (serial & 0xFF000000) >> 24

    encbuff = [None] * 7
    enccode = NICE_FLOR_S_TABLE_ENCODE[code]
    ki = NICE_FLOR_S_TABLE_KI[code & 0xFF] ^ (enccode & 0xFF)

    encbuff[0] = button_id & 0x0F
    encbuff[1] = ((repeat ^ button_id ^ 0x0F) << 4) | ((snbuff[3] ^ ki) & 0x0F)
    encbuff[2] = enccode >> 8
    encbuff[3] = enccode & 0xFF
    encbuff[4] = snbuff[2] ^ ki
    encbuff[5] = snbuff[1] ^ ki
    encbuff[6] = snbuff[0] ^ ki

    #display encbuff as one hex
    print("encbuff: ", hex(encbuff[0]), ",",  hex(encbuff[1]),",", hex(encbuff[2]),",", hex(encbuff[3]),",", hex(encbuff[4]),",", hex(encbuff[5]), ",", hex(encbuff[6]))

    return encode(encbuff)


send(0x00E48DCA,1,3)