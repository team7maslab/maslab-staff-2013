# stateMachine.py
# state machine code for 2013 Maslab Team 7

import arduinoSimpleSerial as arduino
import time, eye, random, sys, virtualBot

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

    # virtualBot
    bot = virtualBot.VirtualBot()
    virtual = True

    # arduino
    ard = arduino.Arduino()
    
# need some kind of auto timeout

    def nextState(self, stopTime):
        stopTime = self.stopTime
        timeLeft = self.stopTime - time.time()
        time.sleep(0.5)     # just for testing- take this out later

        print " "
        print "ourBalls = ", self.ourBalls, "| theirBalls = ", self.theirBalls, "| timeLeft = ", timeLeft
        if (timeLeft <= 0):
            print "game over"
            sys.exit(0)
            # need actual kill code here

        if(timeLeft < 90 and self.theirBalls == 0):
            divertNext = True           # divert the next ball to the middle hopper
            ############ fill this in on Arduino side

        if (self.collision()):
            # this should replace the collision avoidance code in the getIRData method in arduino

            # commented out for testing
##            self.ard.motorCommand(-0.5)
##            self.ard.turnCommand(-0.5)
##            self.ard.packetExchange()
##            self.ard.motorCommand(-0.5)
##            self.ard.turnCommand(0.5)
            pass
            
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
        # virtualBot code
        if (self.virtual):
            collide = self.bot.collision()

        else:
        # get IR and bump data, determine if we've hit a wall
        # actually check this
            return False
        return collide
    
    def wallFollow(self):
        print "state: wallFollow"
        self.prevState = "wallFollow"
        # stuff
        # set ballFound to true or false

        # virtualBot code
        if (self.virtual):
            self.ballFound = self.bot.ballFound()
        else:
            # use camera to find balls
            pass
 
        return self.nextState(self.stopTime)

    def explore(self):
        print "state: explore"
        self.prevState = "explore"
        # stuff

        # virtualBot code
        if (self.virtual):
            self.ballFound = self.bot.ballFound()
        else:
            # use the camera to find balls
            pass

        return self.nextState(self.stopTime)

    def getBalls(self):
        print "state: getBalls"
        self.prevState = "getBalls"
        
        # virtualBot code
        if (self.virtual):
            [ours, theirs] = self.bot.getBalls()
            self.ourBalls += ours
            self.theirBalls += theirs
        else:
            # use methods from the current main.py
            # need to have rush substate when we are close enough
            pass

        return self.nextState(self.stopTime)

    def scoreTower(self):
        print "state: scoreTower"
        self.prevState = "scoreTower"
        if (self.topTowerAttempted):
            # try for the second tower
            self.ourBalls = 0

            # virtualBot code
            if (self.virtual):
                self.bot.scoreTower()
            else:
                # find the tower
                # go up to it
                # activate arm
                pass

        else:
            # try for the second tower
            self.ourBalls = 0

            # virtualBot code
            if (self.virtual):
                self.bot.scoreTower()
            else:
                # find the tower
                # go up to it
                # activate arm
                pass
            self.topTowerAttempted = True

        return self.nextState(self.stopTime)

    def scoreWall(self):
        print "state: scoreWall"

        # virtualBot code
        if (self.virtual):
                self.bot.scoreTower()
        else:
            # find the wall
            # go up to it perpendicularly
            # activate enemy roller
            pass
        self.theirBalls = 0
        return self.nextState(self.stopTime)
