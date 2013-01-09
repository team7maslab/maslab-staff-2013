# constants.py
# constants to be used by the laptop portion of MASLab control code

## arduino pins
# movement motors
pwmL = 13;  # left motor pwm
dirL = 12;  # left motor direction
curL = 11;  # left motor current
pwmR = 10;  # right motor pwm
dirR = 9;   # right motor direction
curL = 8;   # right motor current
# ball-handling motors
# sensors
irF = 7;    # front IR sensor
irL = 6;    # left IR sensor
irR = 5;    # right IR sensor

# motor parameters
cruiseL = 200;      # normal left motor speed
cruiseR = 200;      # normal right motor speed
butPressL = 150;    # left motor speed for pressing button
butPressR = 150;    # right motor speed for pressing button

# time parameters
butPressTime = 0.5  # time required for a button press

# tolerances
speedTOL = 0.1;     # not sure what unit this is, number was just picked randomly for now
angleTOL = 5;       # degrees
