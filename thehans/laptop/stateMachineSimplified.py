# stateMachineSimplified.py
# state machine code for 2013 Maslab Team 7

import time, eye, random, sys, virtualBot, constants

class State:
    def __init__(self):
        self.ballsInHopper = 0

        self.phase = 1
        # phase 1 = wall follow then score
        # phase 2 = explore then score/press button
        # phase 4 = endgame
        
        self.topTowerAttempted = False
        self.ballFound = False
        self.buttonFound = False
        self.prevState = "start"
        self.stopTime = 0
        self.timeToPress = 0
        self.buttonPressed = False
        self.towerFound = False
        self.towerAligned = False
   
# need some kind of auto timeout

    def nextState(self, stopTime):

        # list of states:
        # start
        # wallFollow
        # getBalls
        # findTower
        # scoreTower
        # exploreButtonPriority
        # exploreBallPriority
        # pressButton
        # end
        
        stopTime = self.stopTime
        timeLeft = self.stopTime - time.time()

        if (self.timeToPress < 0 and self.buttonPressed):
            self.timeToPress = time.time() + constants.buttonDelay
        else:
            self.timeToPress = self.timeToPress - time.time()

        print " "
        print "ballsInHopper = ", self.ballsInHopper, "| timeLeft = ", timeLeft, "| timeToPress = ", self.timeToPress

        
        # end
        if (timeLeft <= 0):
            return "end"

        ##### phase 3
        elif(timeLeft < constants.endGame):
            if (self.ballsInHopper > 0):
                return "findTower"
            else:
                return "exploreBallPriority"
        ######

        ###### phases 1 and 2
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
                    # if we're at ball capacity
                    if (self.ballsInHopper >= constants.maxBalls):
                        self.phase = 2
                        self.timeToPress = 0
                        return "findTower"
                    else:
                        return "wallFollow"
                else:                               # we're in phase 2
                    # if we're at ball capacity
                    if (self.ballsInHopper >= constants.maxBalls):
                        return "findTower"
                    # if we're not at capacity, find more balls
                    else:
                        if (self.timeToPress < 0):
                            return "exploreButtonPriority"
                        else:
                            return "exploreBallPriority"

        elif(self.prevState == "findTower"):
            if (self.towerAligned):
                return "scoreTower"
            else:
                return "findTower"

        elif(self.prevState == "scoreTower"):
            if (self.ballsInHopper > 0):
                return "scoreTower"
            else:
                if (self.phase == 1):
                    self.phase = 2
                    self.timeToPress = 0
                    return "exploreButtonPriority"
                else:
                    if (self.timeToPress < 0):
                        return "exploreButtonPriority"
                    else:
                        return "exploreBallPriority"
        # exploring the filed- looking for button
        elif(self.prevState == "exploreButtonPriority"):
            if (self.buttonFound):
                return "pressButton"
            elif (self.ballFound):
                return "getBalls"
            else:
                return "exploreButtonPriority"
        # exploring the field- not looking for button
        elif(self.prevState == "exploreBallPriority"):
            if (self.ballFound):
                return "getBalls"
            else:
                return "exploreBallPriority"

        elif(self.prevState == "pressButton"):      # buttonPressed set to true in main
            if (self.buttonPressed):
                self.buttonPressed = False
                return "exploreBallPriority"
            else:
                return "pressButton"

        else:
            print "error"
            return "error"
