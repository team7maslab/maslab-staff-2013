#include <SoftwareSerial.h>
#include <Servo.h>

// Specify the char commands coming from the laptop
#define query 'Q'        // 0 numbers follow
#define forward 'F'      // 1 number (1-9) follows
#define backward 'B'     // 1 number (1-9) follows
#define left 'L'         // 1 number (1-9) follows
#define right 'R'        // 1 number (1-9) follows
#define helix 'H'        // 1 number (0 or 1) follows
#define intake 'G'       // 1 number (0 or 1) follows
#define arm 'A'          // 1 number (0 or 1) follows
#define enemyHopper 'E'  // 1 number (0 or 1) follows

// Specify the char commands being sent from Arduino
#define mode = 'M'       // 0 = idle, 1 = passive opponent, 2 = aggressive 
#define ir = 'I'         // 3 2-digit numbers (00-99) follow- one number for each IR
                         // IR values are scaled by Arduino- high = close, low = far
#define bump = 'U'       // x numbers (0 or 1) follow ***** need to specify how many bump sensors there are
#define balls = 'K'      // 2 numbers follow (0 or 1)
                         // +1 to our balls in hopper, +1 to enemy balls in hopper

#define doneChar = ';'   // 0 numbers follow
#define killAll 'Z'      // 0 numbers follow

// wheel motor indicies
int pwm1 = 11;
int dir1 = 12;
int pwm2 = 13;
int dir2 = 10;

// ball handling motor indicies
int intakeInd = 53;
int enemyRollerInd = 52;
int helixInd = 51;
int armInd = 50;

// sensor indicies
int ir1 = 1;
int ir2 = 2;
int ir3 = 3;
int bump1 = 4;
int bump2 = 5;

// tracking mode of the robot (0 = idle, 1 = passive opponent, 2 = active opponent)
int gameMode = 0;

// default move speed
int leftSpeed = 0;
int rightSpeed = 0;
int maxSpeed = 0;
  
// ball counting
int ballBump = 6;        // switch index counting the number of balls going up the helix
int currBumpVal = 0;
int prevBumpVal = 0;
int armServoMaxDegree = 90; // *********** figure out what the actual value of this is

// setup 
void setup()
{
  pinMode(pwm1, OUTPUT);
  pinMode(pwm2, OUTPUT);
  pinMode(dir1, OUTPUT);
  pinMode(dir2, OUTPUT);
  pinMode(intakeInd, OUTPUT);
  pinMode(enemyRollerInd, OUTPUT);
  pinMode(helixInd, OUTPUT);
  pinMode(armInd, OUTPUT);
  pinMode(ir1, INPUT);
  pinMode(ir2, INPUT);
  pinMode(ir3, INPUT);
  pinMode(bump1, INPUT);
  pinMode(bump2, INPUT);

  Serial.begin(9600);
}


//---- Return String ---------------------
// The dynamically sized return string
char* retVal;
int retIndex;

// Helper function to keep track of retIndex and use it to write
// a character to the correct location in the retVal array
void writeToRetVal(char c)
{
  retVal[retIndex] = c;
  retIndex++;
}
//----------------------------------------

// PID
void pid(int inputSpeed, int leftRight){
  // left = 1, right = 0
  // ******* PID controller goes here- filler code right now
  
  if (leftRight == 0){
    inputSpeed = (int) inputSpeed/9.0*255.0;
    leftSpeed += inputSpeed;
    rightSpeed += inputSpeed;
  }
  
  else if (leftRight == 1){
    rightSpeed += (int) inputSpeed/9.0*255.0;
  }
  
  else if (leftRight == 2){
    leftSpeed += (int) inputSpeed/9.0*255.0;
  }
  
  // normalize
  if (leftSpeed > rightSpeed){
    maxSpeed = leftSpeed;
  }
  else{
    maxSpeed = rightSpeed;
  }
  
  if (maxSpeed > 255){
    rightSpeed = (int) rightSpeed/(maxSpeed + 0.0);
    leftSpeed = (int) leftSpeed/(maxSpeed + 0.0);
  }
  
  analogWrite(pwm1, leftSpeed);
  analogWrite(pwm2, rightSpeed);

  Serial.print(leftSpeed);
  Serial.print(" ");
  Serial.println(rightSpeed);
//  Serial.println(maxSpeed);
}
  

// Helper function to end our retVal string with the ';' command
// and a null character, and then to send the value in
void sendData()
{
  retVal[retIndex] = ';';
  retVal[retIndex+1] = 0;
//  Serial.print(retVal);
  Serial.flush();
  retIndex = 0;
}

char serialRead()
{
  char in;
  // Loop until input is not -1 (which means no input was available)
  while ((in = Serial.read()) == -1) {}
  return in;
}

int readToInt(){
  char val;
  val = serialRead();
  int intVal =  val - '0';
  return intVal;
}


void killAllAction(){
  analogWrite(pwm1, 0);
  analogWrite(pwm2, 0);
  analogWrite(intakeInd, 0);
  analogWrite(enemyRollerInd, 0);
  analogWrite(helix, 0);
}

void queryAction(){
  // ***************************** 
}

void forwardAction(){
  int goInt = readToInt();
  digitalWrite(dir1, HIGH);
  digitalWrite(dir2, HIGH);
  // *********** need to write PID method to ensure forward motion
  pid(goInt, 0);
}

void backwardAction(){
  int goInt = readToInt();
  digitalWrite(dir1, LOW);
  digitalWrite(dir2, LOW);
  // *********** need to write PID method to ensure backwards motion
  pid(goInt, 0);
}

void leftAction(){
  int goInt = readToInt();
  //digitalWrite(dir1, HIGH);
  //digitalWrite(dir2, LOW);
  // *********** need to write PID method to ensure backwards motion
  pid(goInt, 1);
}

void rightAction(){
  int goInt = readToInt();
  //digitalWrite(dir1, LOW);
  //digitalWrite(dir2, HIGH);
  // *********** need to write PID method to ensure backwards motion
  pid(goInt, 2);
}

void helixAction(){
  int onOff = readToInt();
  analogWrite(helixInd, 255*onOff);
}

void intakeAction(){
  int onOff = readToInt();
  analogWrite(intakeInd, 255*onOff);
}

void enemyHopperAction(){
  int onOff = readToInt();
  analogWrite(enemyRollerInd, 255*onOff);
}

void armAction(){
  int upDown;
  upDown = readToInt();
  analogWrite(armInd, armServoMaxDegree*upDown);
}

void getIRData(){
  writeToRetVal('I');
  // ********************************* need to make sure these chars are 2 digits
  writeToRetVal(analogRead(ir1));
  writeToRetVal(analogRead(ir2));
  writeToRetVal(analogRead(ir3));
}

void getBumpData(){
  writeToRetVal('U');
  writeToRetVal(digitalRead(bump1));
  writeToRetVal(digitalRead(bump2));
}

void checkNewBalls(){
  writeToRetVal('K');
  
  currBumpVal = digitalRead(ballBump);
  
  if (currBumpVal == HIGH && prevBumpVal == LOW){
    // ************ call encoder method here to check the color of the ball 
    int ballType;
    // label ballType as ours (1) or opponent's (0)
    if (ballType == 1){
      writeToRetVal(1);
      writeToRetVal(0);
    }
    else{
      writeToRetVal(0);
      writeToRetVal(1);
    }
  prevBumpVal = currBumpVal;
  }
}

void loop()
{

  // ******* NEED TO SPECIFY WHEN THE GAME MODE IS RETURNED
  
  // reset the speeds first
  leftSpeed = 0;
  rightSpeed = 0;
  maxSpeed = 0;
  
  if (Serial.available() > 0){
    //------------ READ IN ALL THE COMMMANDS -------------
    // Command packet format:
    // F9LG1H1A1;
    // follows convention in the defines at the top
    boolean done = false;
    while (!done){
          
        // Read in the first character, which tells us what to do
        char in = serialRead();
        
        // Performs actions based on the char read in
        switch(in){
          case killAll:
            killAllAction();
            break;
          case query:
            queryAction();
            break;
          case forward:
            forwardAction();
            break;
          case backward:
            backwardAction();
            break;
          case left:
            leftAction();
            break;
          case right:
            rightAction();
            break;
          case helix:
            helixAction();
            break;
          case intake:
            intakeAction();
            break;
          case arm:
            armAction();
            break;
          case enemyHopper:
            enemyHopperAction();
            break;
      }
    }
  }
  //getIRData();
  //getBumpData();
  //checkNewBalls();
  //sendData();
}
