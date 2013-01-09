# movement.py
# used for getting the robot to move around the field
# doesn't handle ball capture/release

import arduino, constants, time
# need to import sensor feeds

####    make all of these closed-loop

class movement:
    def __init__(self, camera): # takes camera feed
        self.ard = arduino.Arduino() # is this needed here?
        # need to define a currentPin
        self.mL = arduino.Motor(ard, currentPinL, constants.dirL, constants.pwmL)
        self.mR = arduino.Motor(ard, currentPinR, constants.dirR, constants.pwmR)
        self.cam = camera
        
    ## basic movements ##
    def forward(action, time):
        if (action == "cruise"):
            mR.setSpeed(constants.cruiseR)
            mL.setSpeed(constants.cruiseL)
            time.sleep(time)
        elif (action == "button"):
            mR.setSpeed(constants.butPressR)
            mL.setSpeed(constants.butPressL)
            time.sleep(constants.butPressTime)

        # use encoders to correct for wheel differences

    def backward():
        # include time, speed? params
        # negative speed = backwards
        if (action == "cruise"):
            mR.setSpeed(0-constants.cruiseR)
            mL.setSpeed(0-constants.cruiseL)
            time.sleep(time)
        elif (action == "button"):
            mR.setSpeed(0-constants.butPressR)
            mL.setSpeed(0-constants.butPressL)
            time.sleep(constants.butPressTime)

        # use encoders to correct for wheel differences
        
    def turn(degree):
        # include degree, time, speed? params
        # use gyro and controller to set this properly
        mR.setSpeed(constants.goR)
        mL.setSpeed(constants.goL)

        # use encoders to correct for wheel differences

    def stop():
        mR.setSpeed(0)
        mL.setSpeed(0)

    ## other movements ##
    
    def wander():
        # some kind of wandering
        # maybe turn and go towards the furthest area
        # maybe some sort of random motion
        # other?

    def randomWalk():
        # robot, go home, you're drunk!

    def wallFollow():
        # need stuff from camera
        # need stuff from one IR
        # target the wall and use IR info to keep it at a constant distance

    def findTarget(target):
        # need stuff from camera
        # rotate to center the target in vision system
        forward("cruise") # go towards target
        # use camera to close the control loop
        
    def pressButton():
        # align robot with release chute
        forward("button") # press button
        backward("button") # release button
        # wait for balls (figure out how long this should take
        # need something here to keep track of number of balls inside hopper

    def avoidWall():
        # some collision avoidance function
        # sensors should throw some sort of collision or collisionImminent flag
        # move away from obstacle until flag is false

    def getUnstuck():
        # similar to the avoidWall function, but used when we don't detect a collision
        # we're trying to move, but not getting anywhere, so try something else
        
