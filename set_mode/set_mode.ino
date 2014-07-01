#include <Wire.h>

byte val = 0;
byte pressed = 0;

void setup(void) {
  Serial.begin(9600);
  Wire.begin();
}

void loop() {
  char keypress = 'a';
  
  if (Serial.available()) {
    // read the most recent byte (0-255):
    // or most recent char
    keypress = Serial.read();
  }
  
  // if cmd key is pressed
  if (keypress == 'z') {
    //setMode();
    test(keypress);
  }
  if (keypress == 'x') {
    //resetMode();
    test(keypress);
  }
  if (keypress == 'c') {
    //motorForeward();
    test(keypress);
  }
  if (keypress == 'v') {
    //motorBackward();
    test(keypress);
  }
  if (keypress == 'b') {
    //motorBrake();
    test(keypress);
  }
  
  //SyncAux0  
  // monitor sync value with freq detection / oscilloscope
}

void setMode() {
  // Pico address
  Wire.beginTransmission(B0011011); // x36/37
  // subaddress
  Wire.write(B00011111); //x1F
  // unused bytes
  Wire.write(val);
  Wire.write(val);
  Wire.write(val);
  // data
  Wire.write(B00000110); // x6
  Wire.endTransmission();
}

void resetMode() {
  // Pico address
  Wire.beginTransmission(B0011011); // x36/37
  // subaddress
  Wire.write(B00011111); //x1F
  // unused bytes
  Wire.write(val);
  Wire.write(val);
  Wire.write(val);
  // data
  Wire.write(val); // x0
  Wire.endTransmission();
}

void test(char kp) {
  Serial.print("Testing key press: ");
  Serial.println(kp); 
}
