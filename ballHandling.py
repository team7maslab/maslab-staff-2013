# ballHandling.py
# used for capturing, counting, and releasing balls

import arduino, constants, time

class ballHandling:
    def __init__(self):
        self.ballsInHopper = 0

    def initArm():
        # fire at the very beginning of a run
        # initializes arm position
        # checks that trapdoor is closed
        
    def groundRoller():
        # collect balls from the ground using rubber band roller
        # include time and speed params (which should be constant)

    def screw():
        # time and speed params
        # lift balls up to hopper level
        # some sort of sensor data to make sure we don't have any balls left in the screw?
        
    def armRoller():
        # release balls using rubber band roller

    def trapdoor(state):
        # open/close trapdoor for lower tower scoring and wall scoring
