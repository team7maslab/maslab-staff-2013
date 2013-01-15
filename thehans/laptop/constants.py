# constants.py
# constants to be used by the laptop portion of MASLab control code

# motor parameters
cruiseL = 0.5;      # initial left motor speed
cruiseR = 0.5;      # initial right motor speed
butPressL = 0.2;    # left motor speed for pressing button
butPressR = 0.2;    # right motor speed for pressing button

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

