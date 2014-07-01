#include <Wire.h>

byte val = 0;

#define hallPin 2
#define syncPin 3
#define motorPin 9
#define controlA 12
#define controlB 13

volatile unsigned long startTime = 0;
volatile unsigned long endTime = 0;
volatile unsigned long counter = 0;
volatile float frequency = 0;
float target = 20.0; // Hz
int controlOn = 0;
int motorVal = 0;

void setup()
{
  pinMode(hallPin, INPUT);
  digitalWrite(hallPin, HIGH);
  pinMode(syncPin, INPUT);
  digitalWrite(syncPin, HIGH);

  pinMode(controlA, OUTPUT);
  digitalWrite(controlA, LOW);
  pinMode(controlB, OUTPUT);
  digitalWrite(controlB, LOW);  // CCW rotation
  pinMode(motorPin, OUTPUT);
  analogWrite(motorPin, motorVal);

//  Serial.begin (115200);
  Serial.begin (9600);
  Wire.begin();
  
  // Attach interrupts
  //attachInterrupt(syncPin-2, read_sync, RISING);
  attachInterrupt(hallPin-2, read_encoder, RISING);
}

void loop()
{
  Serial.println(frequency);
 
  if (controlOn == 1) {
    controlAlgorithm();
  }
  
  
  char keypress = 'a';
  if (Serial.available()) {
    // read the most recent byte (0-255):
    // or most recent char
    keypress = Serial.read();
  }
  
  // if cmd key is pressed
  if (keypress == 'z') {  // fast mode
    setMode();
    test(keypress);
    
  } else if (keypress == 'x') {  // regular mode
    resetMode();
    test(keypress);
    
  } else if (keypress == 'c') {  // forward
    digitalWrite(controlA, HIGH);
    digitalWrite(controlB, LOW);
    controlOn = 0;   //1;
    motorVal = 250;
    analogWrite(motorPin, motorVal);
    test(keypress);
    
  } else if (keypress == 'v') {  // backward
    digitalWrite(controlA, LOW);
    digitalWrite(controlB, HIGH);
    controlOn = 0;
    motorVal = 200;
    analogWrite(motorPin, motorVal);
    test(keypress);
    
  } else if (keypress == 'b') {  // brake
    controlOn = 0;
    motorVal = 0;
    analogWrite(motorPin, motorVal);
    digitalWrite(controlA, LOW);
    digitalWrite(controlB, LOW);
    test(keypress);
    
  } else {
    //test(keypress);
  }
  
}


void read_encoder()
{
  counter++;
  endTime = micros();
  frequency = 500000.0 / ((float)(endTime - startTime));
  startTime = endTime;
}


void controlAlgorithm() {
  float error = target - abs(frequency);
  
  if (error < -0.2) { motorVal = motorVal - 1; }
  if (error > 0.2) { motorVal = motorVal + 1; }
  
  if (motorVal > 255) { motorVal = 255; }
  else if (motorVal < 0) { motorVal = 0; }
  
  analogWrite(motorPin, motorVal);
  
  Serial.print("    motorVal = ");
  Serial.println(motorVal);

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
  Serial.print("Key pressed: ");
  Serial.println(kp); 
}
