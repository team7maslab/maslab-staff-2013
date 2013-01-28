# stateMachine.py
# state machine code for 2013 Maslab Team 7

import time, eye, random, sys, virtualBot

class State:
    def __init__(self):
        self.ourBalls = 0
        self.ourBallsMax = 8         # need to figure out what the max actually is
        self.theirBalls = 0
        self.theirBallsMax = 10      # need to figure out what the max actually is
        self.endgameTime = 30

        self.phase = 1
        # phase 1 = before we get 5 balls
        # phase 2 = after we get 5 balls
        # phase 4 = endgame
        
        self.topTowerAttempted = False
        self.ballFound = False
        self.prevState = "start"
        self.stopTime = 0
   
# need some kind of auto timeout

    def nextState(self, stopTime):
        stopTime = self.stopTime
        timeLeft = self.stopTime - time.time()

        print " "
        print "ourBalls = ", self.ourBalls, "| theirBalls = ", self.theirBalls, "| timeLeft = ", timeLeft
        if (timeLeft <= 0):
            print "game over"
            return "end"
            # need actual kill code here

        #### will fill in later for actual competition (not seeding)
        #if(timeLeft < 90 and self.theirBalls == 0):
            #divertNext = True           # divert the next ball to the middle hopper
            ############ fill this in on Arduino side

        if(timeLeft < self.endgameTime):
            self.phase = 3
            if (self.ourBalls > 0):
                return "scoreTower"
            else:
                return "scoreWall"
             
        elif(self.prevState == "start"):
            self.phase = 1
            return "wallFollow"
        
        elif(self.prevState == "wallFollow"):
            if (self.ballFound):
                return "getBalls"
            else:
                return "wallFollow"
        
        elif(self.prevState == "getBalls"):
            if (self.ballFound):
                return "getBalls"
            else:
                if (self.phase == 1):                # we're in phase 1
                    if (self.ourBalls >=5):
                        self.phase = 2
                        return "scoreTower"
                    elif (self.theirBalls >= self.theirBallsMax):
                        return "scoreWall"
                    else:
                        return "wallFollow"
                else:                               # we're in phase 2
                    if (self.ourBalls >= self.ourBallsMax):
                        return "scoreTower"
                    else:
                        return "getBalls"
                
        elif(self.prevState == "scoreTower"):
            if (self.ourBalls != 0):
                return "scoreTower"
            else:
                if (self.phase == 1):
                    self.phase = 2
                    return "explore"
                elif (self.phase == 2):
                    return "explore"
                elif (self.phase == 3):
                    return "scoreWall"
            
        elif(self.prevState == "scoreWall"):
            if (self.theirBalls != 0):
                return "scoreWall"
            else:
                if (self.phase == 1):
                    return "wallFollow"
                else:
                    return "explore"
            
        elif(self.prevState == "explore"):
            if (self.theirBalls >= self.theirBallsMax):
                return "scoreWall"
            else:
                return "getBalls"
