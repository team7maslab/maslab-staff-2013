# constants.py
# constants to be used by the laptop portion of MASLab control code

# motor parameters
defaultSpeed = 0.5;      # initial left motor speed
ninetyDegTurn = 0.3;     # causes a 90 degree turn in 0.5 seconds

# time parameters
gameTime = 180;     # 3-minute game period
endGame = 150;      # end game entered when there are 30 seconds left in the game
buttonDelay = 30;   # delay between button presses
butPressTime = 0.5; # ??? time required for a button press
pidTimeStep = 0.1;  # time step used in PID control

# controller gains
##### need to calibrate all these
speedKp = 0.1;
speedKi = 0.1;
speedKd = 0.1;
angleKp = 0.1;
angleKi = 0.1;
angleKd = 0.1;
trackingKp = 0.1;

