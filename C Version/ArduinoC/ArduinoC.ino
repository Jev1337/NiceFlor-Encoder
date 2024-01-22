#include "codes.h"

int* gettx(int serial, int button_id, int code, int repeat){
  int snbuff[4]; 
  snbuff[0] = (byte)(serial & 0xFF);
  snbuff[1] = (byte)((serial & 0xFF00) >> 8); 
  snbuff[2] = (byte)((serial & 0xFF0000) >> 16);
  snbuff[3] = (byte)((serial & 0xFF000000) >> 24);

  int encbuff[7];
  int enccode = pgm_read_word(NICE_FLOR_S_TABLE_ENCODE + code);

  int ki = NICE_FLOR_S_TABLE_KI[code & 0xFF] ^ (enccode & 0xFF);

  encbuff[0] = button_id & 0x0F;
  encbuff[1] = ((repeat ^ button_id ^ 0x0F) << 4) | ((snbuff[3] ^ ki) & 0x0F);  
  encbuff[2] = (byte)(enccode >> 8);
  encbuff[3] = (byte)(enccode & 0xFF);
  encbuff[4] = snbuff[2] ^ ki;
  encbuff[5] = snbuff[1] ^ ki;  
  encbuff[6] = snbuff[0] ^ ki;

  Serial.println(encbuff[0], HEX);
  Serial.println(encbuff[1], HEX);
  Serial.println(encbuff[2], HEX);
  Serial.println(encbuff[3], HEX);
  Serial.println(encbuff[4], HEX);
  Serial.println(encbuff[5], HEX);
  Serial.println(encbuff[6], HEX);

  return encbuff;
}

void setup() {
  Serial.begin(115200);
  gettx(0x00E48DCA, 1, 2 ,1);

}



void loop() {

}
