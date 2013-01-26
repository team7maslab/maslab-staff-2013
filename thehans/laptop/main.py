import arduinoSimpleSerial as arduino
import virtualBot
import time, eye, random, sys, stateMachine, navigation, constants

def run(state, ard, nav):

    findColor = "red and green"
    
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

#    stopTime = time.time() + constants.gameTime
    stopTime = time.time() + 35
    timeLeft = stopTime - time.time()
    state.stopTime = stopTime
    state.nextState(stopTime)

    # need to calibrate for full turn
    turnEncCount = 120
    
    cyclop = eye.Eye(debug=True)
   
    try:
        while True:

            currentState = state.nextState(stopTime)
            print currentState
            frame = cyclop.getFrame()

            if (currentState == "end"):
                ard.kill()
                break

            ###### insert actual IR retrieval methods here
#            irVals = ard.retrieve("I")
#            bumpVals = ard.retrieve("U")
#            print irVals

            wallOnSide = "none"

            # check for collsions


##            if (bumpVals[1] == 1 or bumpVals[2] == 1 or irVals[1] > 500 or irVals[2] > 500 or irVals[3] > 500):
##                nav.backUpFromHit(ard)


##                ard.motorCommand(-0.5)
##                ard.turnCommand(-0.5)
##                ard.packetExchange()
##                ard.motorCommand(-0.5)
##                ard.turnCommand(0.5)
##                ard.packetExchange()
            
            if (currentState == "wallFollow"):
                # need to be able to get IR values
                navigation.wallFollow(ard)
                
                (x,y), frame, radius = cyclop.findColor(frame, findColor)
                if (x != -1.0 and y != -1.0):
                    state.ballFound = True
                else:
                    state.ballFound = False

                state.prevState = "wallFollow"
                
            elif (currentState == "explore"):
                
                (x,y), frame, radius = cyclop.findColor(frame, findColor)

                # if no ball is found- turn around
                ##### need to make this go to furthest area
                if (x == -1.0 and y == -1.0):
                    state.ballFound = False
                    ard.turnCommand(constants.ninetyDegTurn)
                    time.sleep(0.1)
                    turnEncCount += 1
                    if (turnEncCount == 120):
                        ard.motorCommand(constants.defaultSpeed)
                        time.sleep(2)
                        turnEncCount = 0

                else:
                    state.ballFound = True

                state.prevState = "explore"


            elif (currentState == "getBalls"):
                (x,y), frame, radius  = cyclop.findColor(frame, findColor)
                if (x == -1.0 and y == -1.0):
                    state.prevState = "getBalls"
                    state.ballFound = False
                else:
                    ard.motorCommand(constants.defaultSpeed)
                    ard.turnCommand(x)
                    ard.packetExchange()
                    time.sleep(1)
                    state.prevState = "getBalls"
                print "x,y", x, y
                
            elif (currentState == "scoreTower"):
                (x,y), frame, radius = cyclop.findColor(frame, "purple")

                ard.motorCommand(constants.defaultSpeed)
                ard.turnCommand(x)
                ard.packetExchange()

                #### correct this to actually use IRs
                closeEnough = (radius > 45)

                if (closeEnough):
                    armCommand(1)
                    time.sleep(5)
                    armCommand(0)
                state.prevState = "scoreTower"

            elif (currentState == "scoreWall"):

                (x,y), frame, radius = cyclop.findColor(frame, "yellow")
                ard.motorCommand(constants.defaultSpeed)
                ard.turnCommand(x)
                ard.packetExchange()

                #### correct this to actually use IRs
                closeEnough = (radius > 45)

                if (closeEnough):
                    ard.enemyCommand(1)
                    time.sleep(5)
                    ard.enemyCommand(0)
            ## for debugging only
#            time.sleep(500)
            cyclop.showImage(frame)
            
    except KeyboardInterrupt:
        cyclop.kill()
            
        print 'mode ' + mode + ' initiated'


def kill():
    sys.exit(0)
    pass
    
if __name__ == '__main__': #called from the command line

#    ard = arduino.Arduino()
#    ard.connect(debug=True)
    ard = virtualBot.VirtualBot()   # testing w/ virtualbot
    nav = navigation.Navigation()
    time.sleep(2) # wait for arduino to power up

    ard.helixCommand(1)
    ard.intakeCommand(1)
    state = stateMachine.State()
    
    nav.backUpFromHit(ard)    
    run(state, ard, nav)
    kill()
