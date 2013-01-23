import arduinoSimpleSerial as arduino
import time, eye, random, sys, stateMachine

def run(state, ard):

    findColor = "green"
    
    #Waiting for button press on robot to denote start
    # need to add button press into the code
    print 'connected! waiting for button press'
    # mode = 0
    # while mode == 0:
    #    ard.packetExchange(query=True)
    #    mode = ard.retrieve('M')[0]
    #    print mode
    #    time.sleep(.02) # check until mode is specified

    wallTOL = 70

    runTime = 180
    stopTime = time.time() + runTime
    timeLeft = stopTime - time.time()
    state.stopTime = stopTime
    state.nextState(stopTime)

    sleepTime = 0.2
    turnTime = 1/sleepTime
    turnDir = random.randrange(-10, 10, 1)
    
    cyclop = eye.Eye(debug=True)
    x = 0
    y = 0
    
    try:
        while True:

            currentState = state.nextState(stopTime)

            irVals = ard.retrieve("I")
            bumpVals = ard.retrieve("U")
            print irVals

            wallOnSide = "none"

            # check for collsions
            if (bumpVals[1] == 1 or bumpVals[2] == 1 or irVals[1] > 500 or irVals[2] > 500 or irVals[3] > 500):
                ard.motorCommand(-0.5)
                ard.turnCommand(-0.5)
                ard.packetExchange()
                ard.motorCommand(-0.5)
                ard.turnCommand(0.5)
                ard.packetExchange()
            
            if (currentState == "wallFollow"):
                # not near wall
                if (irVals[1] < 200 or irVals[2] < 200 or irVals[3] < 200):
                    wallOnSide = "none"
                    ard.motorCommand(0.5)
                    ard.packetExchange()

                # perpendicular to wall
                elif (irVals[1] > 200 or irVals[1] > 220 or irVals[1] > 200):
                    ard.motorCommand(-0.5)
                    ard.turnCommand(0.5)
                    ard.packetExchange()

                # we are parallel to a wall
                elif (irVals[1] > 250 and irVals[2] < 200):
                    wallOnSide = "left"
                    ard.motorCommand(0.5)
                    ard.packetExchange()
                    
                elif (irVals[3] > 250 and irVals[2] < 200):
                    wallOnSide = "right"
                    ard.motorCommand(0.5)
                    ard.packetExchange()

                elif (wallOnSide == "left" and (250-irVals[1]) > wallTOL):
                    ard.motorCommand(0.1)
                    ard.turnCommand(-0.2)
                    ard.packetExchange()
                    
                elif (wallOnSide == "right" and (250-irVals[3]) > wallTOL):
                    ard.motorCommand(0.1)
                    ard.turnCommand(0.2)
                    ard.packetExchange()
                                        
                # need some PID control here

                frame = cyclop.getFrame()
                if (findColor == "green"):
                    (x,y), frame = cyclop.findGreenBall(frame)
                else:
                    (x,y), frame = cyclop.findRedBall(frame)
                if (x != 0 and y != 0):
                    state.ballFound = True
                else:
                    state.ballFound = False

                state.prevState = "wallFollow"
                
            elif (currentState == "explore"):
                
                frame = cyclop.getFrame()
                if (findColor == "green"):
                    (x,y), frame = cyclop.findGreenBall(frame)
                else:
                    (x,y), frame = cyclop.findRedBall(frame)

                # if no ball is found
                if (x == 0 and y == 0):
                    state.ballFound = False
                    ard.motorCommand(0.5)
                    if (turnTime == 0):
                        turnTime = 1/sleepTime
                        turnDir = random.randrange(-10, 10, 1)/10.0
                    ard.turnCommand(turnDir)
                    turnTime -= 1

                else:
                    state.ballFound = True

                state.prevState = "explore"


            elif (currentState == "getBalls"):
                ard.motorCommand(0.5)
                ard.turnCommand(x)
                cyclop.showImage(frame)
                ard.packetExchange()
                time.sleep(sleepTime)
                state.prevState = "getBalls"
                
            elif (currentState == "scoreTower"):
                cyclop.findPurpleTower()

                ard.motorCommand(0.5)
                ard.turnCommand(x)
                cyclop.showImage(frame)
                ard.packetExchange()

                ########### use eye.py to figure out if the tower is close enough
                if (closeEnough):
                    armCommand(1)
                    time.sleep(5)
                    armCommand(0)
                state.prevState = "scoreTower"

            elif (currentState == "scoreWall"):

                cyclop.findYellowWall()
                ard.motorCommand(0.5)
                ard.turnCommand(x)
                cyclop.showImage(frame)
                ard.packetExchange()

                ########### use eye.py to figure out if the tower is close enough
                if (closeEnough):
                    enemyCommand(1)
                    time.sleep(5)
                    enemyCommand(0)
            
    except KeyboardInterrupt:
        cyclop.kill()
            
        print 'mode ' + mode + ' initiated'


def kill():
    sys.exit(0)
    pass
    
if __name__ == '__main__': #called from the command line

    ard = arduino.Arduino()
    time.sleep(1) # wait for arduino to power up
    ard.connect(debug=True)
    ard.helixCommand(1)
    ard.intakeCommand(1)
    state = stateMachine.State()
    
    run(state, ard)
    time.sleep(100)
    kill()
