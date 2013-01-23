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
//#define mode 'M'         // 0 = idle, 1 = passive opponent, 2 = aggressive       ************ need to use this at some point
#define ir 'I'           // 3 3-digit numbers follow- one number for each IR
                         // IR values are scaled by Arduino- high = close, low = far
#define bump 'U'         // x numbers (0 or 1) follow ***** need to specify how many bump sensors there are
#define balls 'K'        // 2 numbers follow (0 or 1)
                         // +1 to our balls in hopper, +1 to enemy balls in hopper

#define doneChar ';'     // 0 numbers follow
#define killAll 'Z'      // 0 numbers follow

// wheel motor indicies
int pwm1 = 4;    // left
int dir1 = 22;
//int motorCurr1 = 12;
int pwm2 = 5;    // right
int dir2 = 23;
//int motorCurr2 = 15;

// ball handling motor indicies
int intakeInd = 6;
int enemyRollerInd = 7;
int helixInd = 8;
int armInd = 10;

// sensor indicies
int ir1 = A1;
int ir2 = A2;
int ir3 = A3;
int bump1 = 27;
int bump2 = 28;

// tracking mode of the robot (0 = idle, 1 = passive opponent, 2 = active opponent)
int gameMode = 0;

// default move speed
int leftSpeed = 0;
int rightSpeed = 0;
int maxSpeed = 0;
int maxPower = 255;
  
// ball counting
int ballBump = 6;        // switch index counting the number of balls going up the helix
int currBumpVal = 0;
int prevBumpVal = 0;
int armServoMaxDegree = 90; // *********** figure out what the actual value of this is

// encoder values
int enc1Val = 0;
int enc1Prev = 0;
int enc2Val = 0;
int enc2Prev = 0;

// stuck detection
int ir1Val = 0;
int ir1Prev = 0;
int ir2Val = 0;
int ir2Prev = 0;
int ir3Val = 0;
int ir3Prev = 0;
int curr1Val = 0;
int curr1Prev = 0;
int curr2Val = 0;
int curr2Prev = 0;
int irTOL = 50;          // tolerance for what values we'll call equal **** might need to change
int currTOL = 10;        // tolerance for what values we'll call equal **** need to test to see what's reasonable **********
int currHIGH = 50;       // values we'll call high current **** need to test to see what's reasonable*******

boolean done = false;
char in;
int conflictDist = 400;

// setup 
void setup(){
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
 // pinMode(motorCurr1, INPUT);
 // pinMode(motorCurr2, INPUT);

  Serial.begin(9600);
  
  pinMode(13, OUTPUT);
  digitalWrite(13, HIGH);
}

// The dynamically sized return string
char* retVal;
int retIndex;

// Helper function to keep track of retIndex and use it to write
// a character to the correct location in the retVal array
void writeToRetVal(char c){
  retVal[retIndex] = c;
  retIndex++;
}

// Helper function to end our retVal string with the ';' command
// and a null character, and then to send the value in
void sendData(){
  retVal[retIndex] = ';';
  retVal[retIndex+1] = 0;
  Serial.flush();
  retIndex = 0;
}

// Loop until input is not -1 (which means no input was available)
char serialRead(){
  char in;
  while ((in = Serial.read()) == -1) {}
  return in;
}

// Read a char from serial and convert to an int
int readToInt(){
  char val;
  val = serialRead();
  int intVal =  val - '0';
  return intVal;
}

// Stop all robot action
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

// PID
void pid(int inputSpeed, int leftRight){
  // forward = 0, backward = 1, left = 2, right = 3
  // *********************************************************** PID controller goes here- just movement code right now
  
  inputSpeed = (int) inputSpeed/9.0*maxPower;
  
  if (leftRight == 0){        // going forward
    leftSpeed += inputSpeed;
    rightSpeed += inputSpeed;
  }
  
  else if (leftRight == 1){    // going backward
    leftSpeed -= inputSpeed;
    rightSpeed -= inputSpeed;
  }    
  
  else if (leftRight == 2){    // going left
    leftSpeed -= inputSpeed;
    rightSpeed += inputSpeed;
  }
  
  else if (leftRight == 3){      // going right
    leftSpeed += inputSpeed;
    rightSpeed -= inputSpeed;
  }
}

void forwardAction(){
  // *********** need to write PID method to ensure forward motion ************** test w/ encoders
  pid(readToInt(), 0);
}

void backwardAction(){
  // *********** need to write PID method to ensure backwards motion
  pid(readToInt(), 1);
}

void leftAction(){
  // *********** need some kind of integration into mapping to figure out the angle driven (maybe here?)
  pid(readToInt(), 2);
}

void rightAction(){
  // *********** need some kind of integration into mapping to figure out the angle driven (maybe here?)
  pid(readToInt(), 3);
}

void moveRobot(){

  // set robot direction
  boolean leftNeg = false;
  boolean rightNeg = false;
  
  if (leftSpeed < 0){
    digitalWrite(dir1, LOW);
    leftNeg = true;
  }
  else{
    digitalWrite(dir1, HIGH);
  }
  
  if (rightSpeed < 0){
    digitalWrite(dir2, LOW);
    rightNeg = true;
  }
  else{
    digitalWrite(dir2, HIGH);
  }
  
  // normalize speed values
  leftSpeed = abs(leftSpeed);
  rightSpeed = abs(rightSpeed);
  int maxValue;
  if (leftSpeed > maxPower || rightSpeed > maxPower){
    if (leftSpeed > rightSpeed){
      maxValue = leftSpeed;
    }
    else{
      maxValue = rightSpeed;
    }
  }
  else{
    maxValue = maxPower;
  }

//  Serial.print(leftSpeed);
//  Serial.print(" ");
//  Serial.println(rightSpeed);
//  Serial.println(maxValue);
  
  leftSpeed = (int) (leftSpeed+0.0)/(maxValue+0.0)*maxPower;
  rightSpeed = (int) (rightSpeed+0.0)/(maxValue+0.0)*maxPower;
  
  // send speed values to the motors
  analogWrite(pwm1, leftSpeed);
  analogWrite(pwm2, rightSpeed);

  if (leftNeg){
    Serial.print("left wheel speed: ");
    Serial.print(0-leftSpeed);
  }
  else{
    Serial.print("left wheel speed: ");
    Serial.print(leftSpeed);
  }
  
  Serial.print("    ");
  if (rightNeg){
    Serial.print("right wheel speed: ");
    Serial.println(0-rightSpeed);
  }
  else{
    Serial.print("right wheel speed: ");
    Serial.println(rightSpeed);
  }
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
  //writeToRetVal('I');
  ir1Val = analogRead(ir1);
  ir2Val = analogRead(ir2);
  ir3Val = analogRead(ir3);  
  
  Serial.print(ir1Val);
  Serial.print(" ");
  Serial.print(ir2Val);
  Serial.print(" ");
  Serial.println(ir3Val);  
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

boolean stuckDetect(){
  int stuckVotes = 0;
  
  if (abs(ir1Val - ir1Prev) < irTOL){
    stuckVotes++;
  }
  if (abs(ir2Val - ir2Prev) < irTOL){
    stuckVotes++;
  }
  if (abs(ir3Val - ir3Prev) < irTOL){
    stuckVotes++;
  }
  if (abs(curr1Val - curr1Prev) < currTOL && curr1Val > currHIGH){      // if motor current values are high and unchanging
    stuckVotes++;
  }
  if (abs(curr2Val - curr2Prev) < currTOL && curr2Val > currHIGH){
    stuckVotes++;
  }
  
  // ********** need to integrate w/ encoder...
    
  ir1Prev = ir1Val;
  ir2Prev = ir2Val;
  ir3Prev = ir3Val;
  curr1Prev = curr1Val;
  curr2Prev = curr2Val;
  
  if (stuckVotes > 3){
    return true;
  }
  else{
    return false;
  }
}  

void loop(){
  // ******* NEED TO SPECIFY WHEN THE GAME MODE IS RETURNED
  Serial.print("IR data: ");
  getIRData();
  getBumpData();
//  Serial.print("avialable to read in: ");
//  Serial.println(Serial.available());
  if (Serial.available() > 1){

    //------------ READ IN ALL THE COMMMANDS -------------
    // Command packet format:
    // F5L2G1H1A1;
    // follows convention in the defines at the top
    done = false;
    
     // reset the speeds first
    leftSpeed = 0;
    rightSpeed = 0;
    maxSpeed = 0;

    while (!done && (in = serialRead()) != NULL){
        //checkNewBalls();
        //sendData();
      
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
          case doneChar:
            done = true;
            Serial.flush();
            break;
        }      
    }
    moveRobot();
  }
  //else{
    //Serial.println("nothing more to read in");
  //}
  // read in sensor data  
//  boolean amIStuck = stuckDetect(); // stuck detection
  
}
