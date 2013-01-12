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
#define balls = 'K'      // 2 2-digit numbers follow
                         // number of our balls in hopper, number of enemy balls in hopper

#define doneChar = ';'   // 0 numbers follow
#define killAll 'Z'      // 0 numbers follow

// handlers for different inputs go here
void queryAction(){
  // stuff
}

void forwardAction(){
  char go;
  go = serial.read();    // reading in one char to determine speed
  // ******************************** stuff 
}

void backwardAction(){
  char go;
  go = serial.read();    // reading in one char to determine speed
  // ******************************** stuff 
}

void leftAction(){
  // ******************************** stuff
}

void rightAction(){
  // ******************************** stuff
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


void loop(){
  
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
