
#define encoderPin  3

volatile unsigned long startTime = 0;
volatile unsigned long endTime = 0;
volatile unsigned long temp = 0;
unsigned long counter = 0;
float frequency = 0;


void setup() { 
  pinMode(encoderPin, INPUT); 
  digitalWrite(encoderPin, HIGH);       // turn on pullup resistor

  attachInterrupt(1, doEncoder, CHANGE);  // encoder pin on interrupt 0 (pin 2)
  //Serial.begin(115200);
  Serial.begin(9600);
} 

void loop(){
  frequency = 500000.0 / ((float)(endTime - startTime));
  Serial.println(frequency);

}
  
void doEncoder() {
  temp = micros();
  startTime = endTime;
  endTime = temp;
}


