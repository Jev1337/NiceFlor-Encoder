#include <stdio.h>
#include <stdint.h>
#include <unistd.h>
#include "tables.h"


uint64_t encode(uint8_t encbuff[7]) {
    uint64_t encoded = 0;
    encoded |= ((uint64_t)(encbuff[6] << 4) & 0xF0) << 0;
    encoded |= ((uint64_t)((encbuff[5] & 0x0F) << 4) | ((uint64_t)(encbuff[6] & 0xF0) >> 4)) << 8;
    encoded |= ((uint64_t)((encbuff[4] & 0x0F) << 4) | ((uint64_t)(encbuff[5] & 0xF0) >> 4)) << 16;
    encoded |= ((uint64_t)((encbuff[3] & 0x0F) << 4) | ((uint64_t)(encbuff[4] & 0xF0) >> 4)) << 24;
    encoded |= ((uint64_t)(encbuff[2] & 0x0F) << 4 | (uint64_t)(encbuff[3] & 0xF0) >> 4) << 32;
    encoded |= ((uint64_t)(encbuff[1] & 0x0F) << 4 | (uint64_t)(encbuff[2] & 0xF0) >> 4) << 40;
    encoded |= ((uint64_t)(encbuff[0] & 0x0F) << 4 | (uint64_t)(encbuff[1] & 0xF0) >> 4) << 48;
    encoded = encoded ^ 0xFFFFFFFFFFFFF0;
    encoded = encoded >> 4;
    return encoded;
}
uint64_t _nice_flor_s_encode(uint32_t serial, uint32_t code, uint8_t button_id, uint8_t repeat) {
    uint8_t snbuff[4] = {serial & 0xFF, (serial >> 8) & 0xFF, (serial >> 16) & 0xFF, (serial >> 24) & 0xFF};
    uint8_t encbuff[7];

    uint32_t enccode = NICE_FLOR_S_TABLE_ENCODE[code];
    uint8_t ki = NICE_FLOR_S_TABLE_KI[code & 0xFF] ^ (enccode & 0xFF);

    encbuff[0] = button_id & 0x0F;
    encbuff[1] = ((repeat ^ button_id ^ 0x0F) << 4) | (snbuff[3] ^ ki & 0x0F);
    encbuff[2] = enccode >> 8;
    encbuff[3] = enccode & 0xFF;
    encbuff[4] = snbuff[2] ^ ki;
    encbuff[5] = snbuff[1] ^ ki;
    encbuff[6] = snbuff[0] ^ ki;

    printf("encbuff: %02X, %02X, %02X, %02X, %02X, %02X, %02X\n", encbuff[0], encbuff[1], encbuff[2], encbuff[3], encbuff[4], encbuff[5], encbuff[6]);

    return encode(encbuff);
}


void _send_repeated(uint32_t serial, uint8_t button_id, uint32_t code) {
    for (uint8_t repeat = 1; repeat < 7; repeat++) {
        uint64_t tx_code = _nice_flor_s_encode(serial, code, button_id, repeat);
        printf("TX Code: 0x%016llX\n", tx_code);
    }
}

void send(uint32_t serial, uint8_t button_id, uint32_t code) {
    _send_repeated(serial, button_id, code);
    usleep(500000); // Delay for 0.5 seconds
}


int main() {
    send(0x00E48DCA,2,32);
}