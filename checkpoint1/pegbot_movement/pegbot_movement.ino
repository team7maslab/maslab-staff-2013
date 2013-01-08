// pins 2 and 4 on the Mega don't work

// motor stuff
int pwm1 = 13;
int dir1 = 12;
int pwm2 = 11;
int dir2 = 10;
int go = 255;

// sensor stuff
int ir = 0;

int on = 1;

void setup()
{
  pinMode(pwm1, OUTPUT);
  pinMode(pwm2, OUTPUT);
  pinMode(dir1, OUTPUT);
  pinMode(dir2, OUTPUT);
  pinMode(ir, INPUT);
}

int motorForward() {
  digitalWrite(dir1, HIGH);
  digitalWrite(dir2, LOW);
  analogWrite(pwm1, go);
  analogWrite(pwm2, go);
  delay(3000);
}

int motorBackward() {
  digitalWrite(dir1, LOW);
  digitalWrite(dir2, HIGH);
  analogWrite(pwm1, go);
  analogWrite(pwm2, go);
  delay(3000);
}

int turnRight() {
  digitalWrite(dir1, HIGH);
  digitalWrite(dir2, HIGH);
  analogWrite(pwm1, go);
  analogWrite(pwm2, go);
  delay(3000);
}

int turnLeft() {
  digitalWrite(dir1, LOW);
  digitalWrite(dir2, LOW);
  analogWrite(pwm1, go);
  analogWrite(pwm2, go);
  delay(3000);
}

void loop()
{
  while (on == 1){
    motorForward();
    motorBackward();
    //turnRight();
    //turnLeft();
    on++;
  }
  while (on != 1){
  }
  
}
