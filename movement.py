# movement.py
# used for getting the robot to move around the field
# doesn't handle ball capture/release

import arduino, constants, time

class movement:
    def __init__(self):

    ## basic movements ##
    def forward():
        # include time, speed? params

    def backward():
        # include time, speed? params

    def turn():
        # include degree, time, speed? params

    def stop():
        # technically shouldn't be necessary, but why not?

    ## other movements ##
    
    def wander():
        # some kind of wandering
        # maybe turn and go towards the furthest area
        # maybe some sort of random motion
        # other?

    def wallFollow():
        # need stuff from camera

    def findTarget(target):
        # need stuff from camera
        # rotate to center the target in vision system
        forward() # go towards target
        
    def pressButton():
        # align robot with release chute
        forward() # press button
        backward() # release button
        # wait for balls (figure out how long this should take
        # need something here to keep track of number of balls inside hopper

    def avoidWall():
        # some collision avoidance function
        # sensors should throw some sort of collision or collisionImminent flag
        # move away from obstacle until flag is false

    def getUnstuck():
        # similar to the avoidWall function, but used when we don't detect a collision
        # we're trying to move, but not getting anywhere, so try something else
        
