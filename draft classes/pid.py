# pid.py
# PID controller for velocity and angle control

import constants, timer

class pid:
    def __init__(self):
        self.prevError = 0
        self.errorSum = 0
        self.tStep = constants.pidTimeStep

    def control(state, input, sensor):
        if (state == "speed"):
            TOL = constants.speedTOL
        elif (state == "angle"):
            TOL = angleTOL
        # should probably use these TOL values somehow

        error = input - sensor
        self.errorSum = self.errorSum + error

        # need to get stuff from timer thread, need to make this
        if (state == "speed" or state == "angle"):
            errorInt = self.errorSum * (timer.pidStepsElapsed)  # integral error
            errorDiff = (self.prevError - error)/tStep          # differential error
        else:
            errorInt = 0
            errorDiff = 0

        setInput = input + Kp * error + Ki * errorInt - Kd * errorDiff

        self.prevError = error

        return setInput
