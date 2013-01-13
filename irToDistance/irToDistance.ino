// http://luckylarry.co.uk/arduino-projects/arduino-using-a-sharp-ir-sensor-for-distance-calculation/
// only works for values within the range of 4 to 30 inches

int IRpin = 1;                                    // analog pin for reading the IR sensor
int exponent = -1.10;                             // *** need to calibrate this value

void setup() {
  Serial.begin(9600);                             // start the serial port
}

void loop() {
  float volts = analogRead(IRpin)*0.0048828125;   // value from sensor * (5/1024) - if running 3.3.volts then change 5 to 3.3
  float distance = 65*pow(volts, exponent);       // worked out from graph 65 = theretical distance / (1/Volts)S - luckylarry.co.uk
  distance = distance*0.393701;                   // convert to inches
  Serial.println(distance);                       // print the distance
  delay(100);                                     // arbitary wait time.
}
