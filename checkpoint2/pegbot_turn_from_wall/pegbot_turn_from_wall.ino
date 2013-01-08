// pins 2 and 4 on the Mega don't work

// motor stuff
int pwm1 = 11;
int dir1 = 12;
int pwm2 = 13;
int dir2 = 10;
int goL = 200;
int goR = 200;

// sensor stuff
int ir = 0;
int irValue = 0;

int on = 1;

void setup()
{
  pinMode(pwm1, OUTPUT);
  pinMode(pwm2, OUTPUT);
  pinMode(dir1, OUTPUT);
  pinMode(dir2, OUTPUT);
  pinMode(ir, INPUT);
  Serial.begin(9600);
}

int forward(int time) {
  digitalWrite(dir1, HIGH);
  digitalWrite(dir2, HIGH);
  analogWrite(pwm1, goL);
  analogWrite(pwm2, goR);
  delay(time);
}

int backward(int time) {
  digitalWrite(dir1, LOW);
  digitalWrite(dir2, LOW);
  analogWrite(pwm1, goL);
  analogWrite(pwm2, goR);
  delay(time);
}

int left(int time) {
  digitalWrite(dir1, HIGH);
  digitalWrite(dir2, LOW);
  analogWrite(pwm1, goL);
  analogWrite(pwm2, goR);
  delay(time);
}

int right(int time) {
  digitalWrite(dir1, LOW);
  digitalWrite(dir2, HIGH);
  analogWrite(pwm1, goL);
  analogWrite(pwm2, goR);
  delay(time);
}

int avoidWall() {
  irValue = analogRead(ir);
  Serial.println(irValue);
  if (irValue > 300){
    analogWrite(pwm1, 0);
    analogWrite(pwm2, 0);
    delay(500);
    backward(300);
    right(250);
    delay(500);
  }
}

void loop()
{
  forward(100);
  avoidWall();
}
