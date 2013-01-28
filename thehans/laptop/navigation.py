# navigation.py
# handles robot navigation

import constants, time, math

class Navigation():

    def __init__(self):
        self.check = True
        self.spinAngleLeft = 0          # how much do we have left to spin  - TODO- change to time
        self.spinReadings = []
        self.spinDone = True            # are we done spinning to check for furthest area?
        self.spinBack = False           # are we spinning back to point in the direction of the furthest area?

    # move to a direction specified by eye.py
    def moveToX (self, arduino, x):
        arduino.motorCommand(constants.defaultSpeed)
        arduino.turnCommand(x)
        arduino.packetExchange()

    # s-shaped backwards curve to get away from a collision
    def backUpFromHit (self, arduino):
        ## TODO - integrate this to work with motor turn time
        arduino.motorCommand(0-constants.defaultSpeed)
        arduino.turnCommand(0-constants.defaultSpeed)
        arduino.packetExchange()
        time.sleep(0.2)
        arduino.motorCommand(0-constants.defaultSpeed)
        arduino.turnCommand(constants.defaultSpeed)
        arduino.packetExchange()

    # basic forward command
    def forward (self, arduino):
        ## TODO - integrate this to work with motor turn time
        arduino.motorCommand(constants.defaultSpeed)
        arduino.packetExchange()

    # basic backward command
    def backward (self, arduino):
        ## TODO - integrate this to work with motor turn time
        arduino.motorCommand(0-constants.defaultSpeed)
        arduino.packetExchange()

    # basic turn command
    ## TODO - need to rework this to take time and direction
    def turn (self, arduino, time, direction):
        print "navigation.turn"
        turnDir = 0
        if (direction == "left"):
            turnDir = 1
        else:
            turnDr = -1
        arduino.turnCommand(turnDir*constants.step)
        arduino.packetExchange()

    # follow a left-side wall
    def wallFollow (self, arduino, IRdata):
        print "navigation.wallFollow"
        leftIR = IRdata[0]
        centerIR = IRdata[1]
        rightIR = IRdata[2]
        
        # allClear- nothing in the way- turn slightly to try to catch a wall
        if (centerIR >= constants.centerClear and leftIR >= constants.sideClear and rightIR >= constants.sideClear):
            self.forward(arduino)
            self.turn(arduino, 0.5*constants.step, "left")

        # following wall- go straight
        elif (leftIR > constants.tooClose and leftIR < constants.tooFar and centerIR > constants.tooClose):
            self.forward(arduino)

        # robot is too close- turning away from wall
        elif (leftIR <= constants.tooClose):
            heading = (constants.tooClose-leftIR)*constants.angleKp
            self.turn(arduino, constants.step, "right")

        # robot is too far- turning towards wall
        elif (leftIR >= constants.tooFar and leftIR < constants.sideClear):
            heading = (constants.tooClose-leftIR)*constants.angleKp
            self.turn(arduino, constants.step, "left")

        # only center IR is too close (facing wedge)
        elif (centerIR <= constants.tooClose and leftIR > constants.sideClear and rightIR > constants.sideClear):
            self.backward(arduino, constants.step)

        ### other conditions?
        else:
            pass

    def explore (self, arduino, IRdata):
        print "navigation.explore"
        leftIR = IRdata[0]
        centerIR = IRdata[1]
        rightIR = IRdata[2]
        sumIR = leftIR + centerIR + rightIR
        
        if (self.spinDone and self.spinBack == False):
            self.spinAngleLeft = 270

        if math.fabs(self.spinAngleLeft) > 0:     #must finish spin
            if math.fabs(self.spinAngleLeft) <= constants.angleTOLdeg:    #can spin in 1 cycle
                self.turn(arduino, constants.angleTOLdeg)
                self.spinAngleLeft = 0
                self.spinDone = True
            else:
                if self.spinAngleLeft > 0:   #calculate the angle's sign
                    sign = 1
                    direction = "right"
                else:
                    sign = -1
                    direction = "left"

            ## TODO - integrate this to work with motor turn time
                self.turn(arduino, constants.step, direction)
                self.spinAngleLeft -= sign*constants.angleMoveDeg
                self.spinDone = False

                # record IR readings
                if self.spinBack == False:
                    self.spinReadings.append((sumIR, self.spinAngleLeft))

        else:                            #choose a direction and move fwd

            # TODO- rework this to work with just amount of time spun rather than angles
            if (len(self.spinReadings) > 0):
                angle = self.spinReadings[0][1]
                sumIR = self.spinReadings[0][0]

                subset = [self.spinReadings[0]]
                          
                # find the angle with the greatest sumIR and add it to the subset list
                print "finding open space"
                for i in range(0, len(self.spinReadings)-1):
                    if (self.spinReadings[i][0] > sumIR):
                        sumIR = self.spinReadings[i][0]
                        angle = self.spinReadings[i][1]
                        subset = []
                        subset.append(self.spinReadings[i])
                    elif (self.spinReadings[i][0] == sumIR):
                        subset.append(self.spinReadings[i])

                # take a random value and go to it
                tempTup = random.choice(subset)
                angle = tempTup[1]

                print "ANGLE", angle, "SUM IR", sumIR
                self.spinReadings = []
                self.spin_angle_left = 0

                walk_dazi = 0-angle
                
                # clear the lists
                self.spinReading = []
                subset = []
                self.spinDone = True
                self.spinBack = True
            
                # spin to appropriate direction
                if walk_dazi > 0:   #calculate the angle's sign
                    sign = 1
                else:
                    sign = -1

                self.spinAngleLeft = walk_dazi-sign*constants.angleMoveDeg
                
            else:
                self.forward(arduino)

    def align(self, arduino, IRdata, bumpData):
        print "navigation.align"
        leftBump = bumpData[0]
        rightBump = bumpData[1]
        leftIR = IRdata[0]
        centerIR = IRdata[1]
        rightIR = IRdata[2]

        # if both bumpers have been activated, we are aligned
        if (leftBump and rightBump):
            return True         # returns whether or not we have been aligned
        # if only the left bumper has been activated, turn the right wheel forward
        elif (leftBump):
            self.turn(arduino, constants.timeStep, "right")
            return False
        # if only the right bumper has been activated, turn the left wheel forward
        elif (rightBump):
            self.turn(arduino, constants.timeStep, "left")
            return False
