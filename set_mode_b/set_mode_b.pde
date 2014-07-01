import processing.serial.*;
Serial port;

void setup() {
  //size(256, 150);
  println("Available serial ports:");
  println(Serial.list());
  port = new Serial(this, Serial.list()[0], 9600);  
  
  //port = new Serial(this, "COM1", 9600);
 }
 
void draw() {
  // write the current X-position of the mouse to the serial port as a byte
  //port.write(mouseX);
}

void keyPressed() {
  //println(key);
  port.write(key);
}

