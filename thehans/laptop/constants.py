# constants.py
# constants to be used by the laptop portion of MASLab control code

# motor parameters
defaultSpeed = 0.5      # initial left motor speed

# time parameters
gameTime = 180     # 3-minute game period
endGame = 30       # end game entered when there are 30 seconds left in the game
buttonDelay = 30   # delay between button presses
butPressTime = 0.5 # ??? time required for a button press
step = 0.1         # time step used for forward/

# controller gains
##### need to calibrate this
angleKp = 0.005

# space clearance values
centerClear = 200        # enough space in front to continue forward
sideClear = 250          # enough space on sides to consider allClear
tooClose = 100           # correction threshold for wall following
tooFar = 200             # correction threshold for wall following
# tooClose < tooFar < sideClear


# movement tolerances
angleTOLdeg = 1
angleTOLrad = 0.02

angleMoveDeg = 5

maxBalls = 10

buttonDelay = 30

towerFoundThresh = 15
towerCloseThresh = 25

