# states.py
# implementation of the state machine

import constants, time, arduino, sensor, ballHandling

class IState:
    def next_state(self):
        raise NotImplementedError

class stateMachine:
    def __init__(self):
        self.vision = sensor.vision()
        self.move = movement.run()
        self.handler = ballHandling.run()
    def runSM(self):
        self.state = ExploreState(self)
        while True:
            # vision code should be detecting balls

            self.state = self.state.next_state()

if __name__ == "__main__":
    sm = stateMachine()
    sm.runSM()

class exploreState(IState):
    def __init__(self, sm):
        self.sm = sm
    def next_state(self):
        if ### vision finds a ball ###:
            if ### vision says ball is close enough ###:
                self.sm.handler.capture()
            else:
            return toBallState()
        else:
            self.sm.move.findTarget("ball")
        
