# navigation.py

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

    def goFoward (arduino, time):
        ard.motorCommand(constants.defaultSpeed)
        time.sleep(time)
