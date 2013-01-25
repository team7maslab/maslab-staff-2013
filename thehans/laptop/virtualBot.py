# virtualBot.py
# tests robot behaviors for MASLab 2013
# clones most of arduinoSimpleSerial.py methods into a form that doesn't interact with Arduino

import random, math

class VirtualBot:

    def __init__ (self):
        self.returnVal = ""

    def packetExchange(self, query = False):
        returnVal += ";"
        print self.returnVal
        self.returnVal = ""

    def motorCommand(self, speed):
        if speed >= 0:
            self.returnVal += ("F" + str(int(min(math.fabs(speed*10),9))))
        else:
            self.returnVal += ("B" + str(int(min(math.fabs(speed*10),9))))

    def turnCommand(self, heading):
        if heading >= 0:
            self.returnVal += ("R" + str(int(min(math.fabs(heading*10),9))))
        else:
            self.returnVal += ("L" + str(int(min(math.fabs(heading*10),9))))

    def helixCommand(self, mode):
        self.returnVal += ("H" + str(mode))

    def intakeCommand(self, mode):
        self.returnVal += ("G" + str(mode))

    def armCommand(self, mode):
        self.returnVal += ("A" + str(mode))

    def enemyCommand(self, mode):
        self.returnVal += ("E" + str(mode))

    def armCommand(self, mode):
        self.returnVal += ("A" + str(mode))

    def startCommand(self, mode):
        self.helixCommand(1)
        self.intakeCommand(1)
        self.armCommand(0)
        self.enemyCommand(0)

    def kill(self):
        self.helixCommand(0)
        self.intakeCommand(0)
        self.armCommand(0)
        self.enemyCommand(0)
        self.motorCommand(0)
        self.turnCommand(0)
        print "end"
