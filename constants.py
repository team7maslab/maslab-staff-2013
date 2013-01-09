# constants.py
# constants to be used by the laptop portion of MASLab control code

## arduino pins
# movement motors
pwmL = 11;  # left motor pwm
dirL = 12;  # left motor direction
pwmR = 13;  # right motor pwm
dirR = 10;  # right motor direction
# ball-handling motors
# sensors

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
