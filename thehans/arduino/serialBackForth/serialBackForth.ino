#include <SoftwareSerial.h>
#include <Servo.h>

// Specify the char commands coming from the laptop
#define query 'Q'        // 0 numbers follow
#define forward 'F'      // 1 number (1-9) follows
#define backward 'B'     // 1 number (1-9) follows
#define left 'L'         // 0 numbers follow
#define right 'R'        // 0 numbers follow
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
int pwm1 = 10;
int dir1 = 11;
int pwm2 = 12;
int dir2 = 13;

// ball handling motors
int roller = 53;
int helix = 52;
int arm = 51;

// sensor indicies
int ir1 = 1;
int ir2 = 2;
int ir3 = 3;
int bump1 = 4;
int bump2 = 5;

// ball counting
int ballBump = 6;        // switch index counting the number of balls going up the helix
String currBumpVal = 'LOW';
String = 'LOW';

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
void pid(int inputSpeed, boolean pOnly){
  // ******* PID controller here
  
  
  pidMotorSpeeds correctedSpeeds;
  // ********* correctedSpeeds.leftSpeed = something
  // ********* correctedSpeeds.rightSpeed = something
  analogWrite(pwm1, corrected.leftSpeed);
  analogWrite(pwn2, corrected.rightSpeed);
}
  

// Helper function to end our retVal string with the ';' command
// and a null character
void endRetVal()
{
  retVal[retIndex] = ';';
  retVal[retIndex+1] = 0;
}

// Helper function to send the retVal through the serial connection
// as well as reset the retIndex variable
void sendRetVal()
{
  Serial.print(retVal);
  Serial.flush();
  retIndex = 0;
}

// ??? are we using serialRead()?


// handlers for different inputs go here
void killAllAction(){
  // kill all the things
}

void queryAction(){
  // stuff
}

void forwardAction(){
  char go;
  go = serial.read();    // reading in one char to determine speed
  int goInt = atoi(go);
  digitalWrite(dir1, HIGH);
  digitalWrite(dir2, HIGH);
  // *********** need to write PID method to ensure forward motion
  pid(goInt, false);
}

void backwardAction(){
  char go;
  go = serial.read();    // reading in one char to determine speed
  int goInt = atoi(go);
  digitalWrite(dir1, LOW);
  digitalWrite(dir2, LOW);
  // *********** need to write PID method to ensure backwards motion
  pid(goInt, false);
}

void leftAction(){
  char go;
  go = serial.read();    // reading in one char to determine speed
  int goInt = atoi(go);
  digitalWrite(dir1, HIGH);
  digitalWrite(dir2, LOW);
  analogWrite(pwm1, goInt);
  analogWrite(pwn2, goInt);
}

void rightAction(){
  char go;
  go = serial.read();    // reading in one char to determine speed
  int goInt = atoi(go);
  digitalWrite(dir1, LOW);
  digitalWrite(dir2, HIGH);
  analogWrite(pwm1, goInt);
  analogWrite(pwn2, goInt);
}

void helixAction(){
  char onOff;
  onOff = serial.read();  // reading in one char to turn on or off
  //********************************** stuff
}

void armAction(){
  char upDown;
  upDown = serial.read();  // reading in one char to move up or down
  // ********************************* stuff
}

void enemyHopperAction(){
  char upDown;
  upDown = serial.read();  // reading in one char to move up or down
  // ********************************* stuff
}

void getIRData(){
  writeToRetValue('I');
  // ********************************* need to make sure these chars are 2 digits
  writeToRetValue(analogRead(ir1));
  writeToRetValue(analogRead(ir2));
  writeToRetValue(analogRead(ir3));
}

void getBumpData(){
  writeToRetValue('U');
  writeToRetValue(digitalRead(bump1));
  writeToRetValue(digitalRead(bump2));
}

void checkNewBalls(){
  writeToRetValue('K');
  currBumpVal = digitalRead(ballBump);
  
  if (currBumpVal == HIGH && prevBumpVal == LOW){
    // ************ call encoder method here to check the color of the ball 
    int ballType;
    // label ballType as ours (1) or opponent's (0)
    if (ballType == 1){
      writeToRetValue(1);
      writeToRetValue(0);
    else{
      writeToRetValue(0);
      writeToRetValue(1);
    }
  prevBumpVal = currBumpVal;
}

void loop(){

  // ******* NEED TO SPECIFY WHEN THE GAME MODE IS RETURNED
  
  if (Serial.available() > 0){
    //------------ READ IN ALL THE COMMMANDS -------------
    // Command packet format:
    // F9LG1H1A1;
    // follows convention in the defines at the top
    boolean done = false;
    while (!done){
          
        // Read in the first character, which tells us what to do
        char in = serial.read();
        
        // Performs actions based on the char read in
        switch(in){
          case killAll:
            killAllAction();
          case query:
            queryAction();
            break;
          case forward:
            forwardAction();
            break;
          case backward:
            backwardAction();
          case left:
            leftAction();
          case right:
            rightAction();            
          case helix:
            helixAction();
          case intake:
            intakeAction();
          case arm:
            armAction();
          case enemyHopper:
            enemyHopperAction();
        }
      }
  }
  
  getIRData();
  getBumpData();
  checkNewBalls();
  endRetVal();
  sendRetVal();  
}
