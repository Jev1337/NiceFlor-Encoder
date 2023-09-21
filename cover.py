from __future__ import annotations

import logging

import time


from encode_tables import (
    NICE_FLOR_S_TABLE_ENCODE,
    NICE_FLOR_S_TABLE_KI,
)
from threading import Lock


_LOGGER = logging.getLogger(__name__)



class RFDevice:
    def __init__(
        self,
        gpio: int,
        pi: 1,
    ) -> None:
        self._pi = pi
        self._gpio = gpio
        self.tx_pulse_short = 500
        self.tx_pulse_long = 1000
        self.tx_pulse_sync = 1500
        self.tx_pulse_gap = 15000
        self.tx_length = 52

    def tx_code(self, code: int):
        wf = []
        wf.extend(self.tx_sync())
        rawcode = format(code, "#0{}b".format(self.tx_length))[2:]
        for bit in range(0, self.tx_length):
            if rawcode[bit] == "1":
                wf.extend(self.tx_l0())
            else:
                wf.extend(self.tx_l1())
        wf.extend(self.tx_sync())
        wf.extend(self.tx_gap())

        while self._pi.wave_tx_busy():
            time.sleep(0.1)

        self._pi.wave_clear()
        self._pi.wave_add_generic(wf)
        wave = self._pi.wave_create()
        self._pi.wave_send_once(wave)

        while self._pi.wave_tx_busy():
            time.sleep(0.1)

        self._pi.wave_delete(wave)

    def tx_l0(self):
        return [
            print(self._gpio, None, self.tx_pulse_short),
            print(None, self._gpio, self.tx_pulse_long),
        ]

    def tx_l1(self):
        return [
            print(self._gpio, None, self.tx_pulse_long),
            print(None, self._gpio, self.tx_pulse_short),
        ]

    def tx_sync(self):
        return [
            print(self._gpio, None, self.tx_pulse_sync),
            print(None, self._gpio, self.tx_pulse_sync),
        ]

    def tx_gap(self):
        return [
            print(None, self._gpio, self.tx_pulse_gap),
        ]


def pair(button_id, code, serial):
        _LOGGER.info("Starting pairing of %s... Wait 5 seconds.", hex(serial))

        for _ in range(1, 10):
            _send_repeated(serial, button_id, code)

        _LOGGER.info("Entered pairing mode for %s.", hex(serial))

def send(serial: int, button_id: int, code: int):
    _send_repeated(serial, button_id, code)
    time.sleep(0.5)

def _send_repeated(serial: int, button_id: int, code: int):
    for repeat in range(1, 7):
        tx_code = _nice_flor_s_encode(serial, code, button_id, repeat)
        _LOGGER.info(
            "serial %s, button_id %i, code %i, tx_code %s",
            hex(serial),
            button_id,
            code,
            hex(tx_code),
        )
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


send(0x00A5D8B8, 1, 0x5bed)
