# pid.py
# PID controller for velocity and angle control

import constants

class pid:
    def __init__(self):
        # something something something

    def control(state, input, sensor):
        if (state == "speed"):
            TOL = constants.speedTOL
        elif (state == "angle"):
            TOL = angleTOL
        # compare input to (sensor-input)
        
