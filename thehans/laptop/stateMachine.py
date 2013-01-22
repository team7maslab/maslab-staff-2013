# stateMachine.py
# state machine code for 2013 Maslab Team 7

import arduinoSimpleSerial as arduino
import time, eye, random, sys

class State:
    ourBalls = 0
    ourBallsMax = 8         # need to figure out what the max actually is
    theirBalls = 0
    theirBallsMax = 10      # need to figure out what the max actually is
    endgameTime = 30

    phase = 1
    # phase 1 = before we get 5 balls
    # phase 2 = after we get 5 balls
    # phase 4 = endgame
    
    topTowerAttempted = False
    ballFound = False
    prevState = "start"
    stopTime = 0
    
# need some kind of auto timeout

    def nextState(self, stopTime):
        stopTime = self.stopTime
        timeLeft = self.stopTime - time.time()
        time.sleep(0.5)     # just for testing- take this out later
        
        print "timeLeft = ", timeLeft

        if (timeLeft <= 0):
            print "game over"
            sys.exit(0)
            # need actual kill code here

        if (self.collision()):
            # this should replace the collision avoidance code in the getIRData method in arduino
            arduino.motorCommand(-0.5)
            arduino.turnCommand(-0.5)
            arduino.packetExchange()
            arduino.motorCommand(-0.5)
            arduino.turnCommand(0.5)
            
        if(timeLeft < self.endgameTime):
            self.phase = 3
            if (self.ourBalls > 0):
                return self.scoreTower()
            else:
                return self.scoreWall()

        elif(self.prevState == "start"):
            self.phase = 1
            return self.wallFollow()
        
        elif(self.prevState == "wallFollow"):
            if (self.ballFound):
                return self.getBalls()
            else:
                return self.wallFollow()
        
        elif(self.prevState == "getBalls"):
            if (self.phase == 1):                # we're in phase 1
                if (self.ourBalls >=5):
                    self.phase = 2
                    return self.scoreTower()
                elif (self.theirBalls >= self.theirBallsMax):
                    return self.scoreWall()
                else:
                    return self.wallFollow()
            else:                               # we're in phase 2
                if (self.ourBalls >= self.ourBallsMax):
                    return self.scoreTower()
                else:
                    return self.getBalls()                        
                
        elif(self.prevState == "scoreTower"):
            if (self.ourBalls != 0):
                return self.scoreTower()
            else:
                if (self.phase == 1):
                    self.phase = 2
                    return self.explore()
                elif (self.phase == 2):
                    return self.explore()
                elif (self.phase == 3):
                    return self.scoreWall()
            
        elif(self.prevState == "scoreWall"):
            if (self.phase == 1):
                return self.wallFollow()
            else:
                return self.explore()
            
        elif(self.prevState == "explore"):
            if (self.theirBalls >= self.theirBallsMax):
                return self.scoreWall()
            else:
                return self.getBalls()
            
    def collision(self):
        # get IR and bump data, determine if we've hit a wall
        # actually check this

        return False
    
    def wallFollow(self):
        print "state: wallFollow"
        self.prevState = "wallFollow"
        # stuff
        # set ballFound to true or false
        return self.nextState(self.stopTime)

    def explore(self):
        print "state: explore"
        self.prevState = "explore"
        # stuff
        return self.nextState(self.stopTime)

    def getBalls(self):
        print "state: getBalls"
        self.prevState = "getBalls"
        # use methods from the current main.py
        # need to have rush substate when we are close enough

        return self.nextState(self.stopTime)

    def scoreTower(self):
        print "state: scoreTower"
        self.prevState = "scoreTower"
        if (topTowerAttempted):
            # try for the second tower
            pass
        else:
            # try for the top tower
            self.topTowerAttempted = True
        # find the tower
        # go up to it
        # activate arm
        return self.nextState(self.stopTime)

    def scoreWall(self):
        print "state: scoreWall"
        # find the wall
        # go up to it perpendicularly
        # activate enemy roller

        return self.nextState(self.stopTime)
