# navigation.py
# handles robot navigation

import constants, time

class Navigation():

    def __init__(self):
        self.check = True

    def backUpFromHit (self, arduino):
        arduino.motorCommand(0-constants.defaultSpeed)
        arduino.turnCommand(0-constants.defaultSpeed)
        arduino.packetExchange()
        time.sleep(0.2)
        arduino.motorCommand(0-constants.defaultSpeed)
        arduino.turnCommand(constants.defaultSpeed)
        arduino.packetExchange()

    def forward (arduino, time):
        arduino.motorCommand(constants.defaultSpeed)
        arduino.packetExchange()
        time.sleep(time)

    def backward (arduino, time):
        arduino.motorCommand(0-constants.defaultSpeed)
        arduino.packetExchange()
        time.sleep(time)

    def turn (arduino, heading, time):
        arduino.motorCommand(constants.defaultSpeed)
        arduino.packetExchange()
        time.sleep(time)

    def wallFollow (arduino, IRdata):
        leftIR = IRdata[0]
        centerIR = IRdata[1]
        rightIR = IRdata[2]
        
        # allClear
        if (centerIR >= constants.centerClear and leftIR >= constants.sideClear and rightIR >= constants.sideClear):
            self.goForward(arduino, constants.step)

            #### check if we are at a convex area and follow if possible
        

        # following wall
        elif (leftIR > constants.tooClose and leftIR < constants.tooFar and centerIR > constants.tooClose):
            #### use P control here to determine heading
            self.goForward(arduino, heading)
        # turning away from wall
        elif (leftIR <= constants.tooClose):
            #### use P control here to determine heading
            self.turn (arduino, "right", heading)

        # turning towards wall
        elif (leftIR >= constants.tooFar and leftIR < constants.sideClear):
            self.turn (arduino, "left", heading)

        # only center IR is too close (facing wedge)
        elif (centerIR <= constants.tooClose):
            self.backward(arduino, constants.step)

        ### other conditions?
        else:
            pass

    def explore (arduino, IRdata):
        leftIR = IRdata[0]
        centerIR = IRdata[1]
        rightIR = IRdata[2]

        ### need encoders for this
        
            

