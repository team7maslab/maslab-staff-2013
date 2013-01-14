// pins 2 and 4 on the Mega don't work

#define motorChar 'M'
#define initChar 'I'
#define doneChar ';'

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

void stopMotors(){
  analogWrite(pwm1, 0);
  analogWrite(pwm2, 0);
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

char serialRead()
{
  char in;
  // Loop until input is not -1 (which means no input was available)
  while ((in = Serial.read()) == -1) {}
  return in;
}

void loop()
{
  // Check if there is any input, otherwise do nothing
  if (Serial.available() > 0)
  {
    //------------ READ IN ALL THE COMMMANDS -------------
    // Command packet format:
    // An1234Bm5678;
    // A, B = mode markers (telling us what type of command it is)
    // n, m = length markers (telling us how many arguments follow
    //     the command)
    // 1234, 5678 = command arguments
    // ; = special mode marker that deliminates the end of the command
    //     packet

    // Use the done helper variable to know when to move on
    boolean done = false;
    while (!done)
    {
      // Read in the first character, which is the mode, telling
      // us what to do
      char mode = serialRead();

      // Perform actions based on the mode read in
      switch (mode)
      {
        case initChar:
          // Process all the input data and set up all the dynamic
          // arrays
          // initAll();
          return;
          break;

        case motorChar:
          // Process the next characters and use them to set motor
          // speeds
          //moveMotors();
          forward(100);
          Serial.write('K;');
          break;

        case doneChar:
          stopMotors();
          // We're done reading in input from python
          done = true;
          break;
          
        default:
          Serial.write('K;');
          left(100);
          break;
      }
    }

    //------------- WRITE OUT ALL THE SENSOR DATA -----------

  }
}
