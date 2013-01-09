# sensors.py
# used for getting sensor data

import arduino, constants

class sensor:
    def __init__(self, camera): # takes camera feed
        self.ard = arduino.Arduino()
        self.irFront = arduino.AnalogInput(ard, constants.irF)
        self.irLeft = arduino.AnalogInput(ard, constants.irL)
        self.irRight = arduino.AnalogInput(ard, constants.irR)
        
    def getIR(irPos):
        irVal = 0
        if (irPos == "front"):
            irVal = self.irFront.getValue()
        elif (irPos == "left"):
            irVal = self.irLeft.getValue()
        elif (irPos == "right"):
            irVal = self.irRight.getValue()
        return irVal
            
