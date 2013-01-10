/* Read Encoder
 * Connect Encoder to Pins encoder0PinA, encoder0PinB, and +5V.
 *
 * Sketch by max wolf / www.meso.net
 * v. 0.1 - very basic functions - mw 20061220
 *
 */

// B is clockwise of A

int encoder0PinA = 31;
int encoder0PinB = 30;

int lastA = LOW;
int lastB = LOW;
int nowA = LOW;
int nowB = LOW;

int n = 0;
boolean changeA = false;
boolean changeB = false; 


void setup() { 
  pinMode (encoder0PinA,INPUT);
  pinMode (encoder0PinB,INPUT);
  Serial.begin (9600);
} 

void loop() {
  nowA = digitalRead(encoder0PinA);
  nowB = digitalRead(encoder0PinB);
  changeA = (nowA != lastA);
  changeB = (nowB != lastB);
  
  if (changeA && (nowA != nowB)){
    n++;
  }
  else if (changeB && (nowA != nowB)){
    n--;
  }
  else if (changeA && (nowA == nowB)){
    n--;
  }
  else if (changeB && (nowA == nowB)){
    n++;
  }

  Serial.println(n);
  lastA = nowA;
  lastB = nowB;
}

