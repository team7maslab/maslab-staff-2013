# virtualBot.py
# tests robot behaviors for MASLab 2013

import random

class VirtualBot:
    motion = "stopped"
    arm = "up"
    enemyRoller = "off"
    ourBallsLeft = 8
    theirBallsLeft = 4
    maxBalls = 12

    def collision(self):
        collideProb = random.randrange(1,10)
        if (collideProb > 7):
            print "collision"
            print "avoiding..."
            return True
        else:
            return False

    def ballFound(self):
        findProb = ((self.ourBallsLeft+self.theirBallsLeft)/self.maxBalls)*0.5
        if (random.random() < findProb):
            print "found a ball"
            return True
        else:
            return False

    def getBalls(self):
        ourBalls = min(random.randrange(0,3), self.ourBallsLeft)
        theirBalls = min(random.randrange(0,2), self.theirBallsLeft)

        self.ourBallsLeft -= ourBalls
        self.theirBallsLeft -= theirBalls
        self.maxBalls -= (ourBalls + theirBalls)
        
        print "got ", ourBalls, "of our balls"
        print "got ", theirBalls, "of their balls"
        return [ourBalls, theirBalls]

    def scoreTower(self):
        print "scoring at tower"

    def scoreWall(self):
        print "scoring at wall"
