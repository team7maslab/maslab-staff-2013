import arduinoSimpleSerial as arduino
import virtualBot
import time, eye, random, sys, stateMachineSimplified, navigation, constants

def run(state, ard, nav, color):

    findColor = color
    
    #Waiting for button press on robot to denote start
    # need to add button press into the code
    print 'connected! waiting for button press'
    # mode = 0
    # while mode == 0:
    #    ard.packetExchange(query=True)
    #    mode = ard.retrieve('M')[0]
    #    print mode
    #    time.sleep(.02) # check until mode is specified

    stopTime = time.time() + constants.gameTime
    timeLeft = stopTime - time.time()
    state.stopTime = stopTime
    state.nextState(stopTime)
    
    cyclop = eye.Eye(debug=True)

    ## TODO - need interface for IRs- values should come in a tuple

    try:
        while True:
            currentState = state.nextState(stopTime)
            print currentState
            frame = cyclop.getFrame()

            # check to see if the game is over
            if (currentState == "end"):
                ard.kill()
                cyclop.kill()
                break

            ###### TODO - insert actual IR retrieval methods here
#            IRdata = ard.retrieve("I")
#            bumpData = ard.retrieve("U")
#            print IRdata

            # temporary placeholder for IR and bump values
            IRdata = (500, 500, 500)
            bumpVals = (0,0)

            # check for collsions
            if (currentState != "getBall" and currentState != "alignTower" and currentState != "scoreTower"):
                # check for collisions
                pass

            # TODO - uncomment once IRs and bumps are available
##            if (bumpVals[1] == 1 or bumpVals[2] == 1 or irVals[1] > 500 or irVals[2] > 500 or irVals[3] > 500):
##                self.searching = True
##                nav.backUpFromHit(ard)

            # wall following state
            if (currentState == "wallFollow"):
                # need to be able to get IR values
                nav.wallFollow(ard, IRdata)

                # check for balls
                (x,y), frame, radius = cyclop.findColor(frame, findColor)
                if (x != -1.0 and y != -1.0):
                    state.ballFound = True
                else:
                    state.ballFound = False

                state.prevState = "wallFollow"

            # get a found ball based on the values obtained from the camera
            elif (currentState == "getBalls"):
                (x,y), frame, radius  = cyclop.findColor(frame, findColor)
                if (x == -1.0 and y == -1.0):
                    state.prevState = "getBalls"
                    state.ballFound = False
                else:
                    nav.moveToX(ard, x)
                    state.prevState = "getBalls"
                print "x,y", x, y

            # find the tower
            elif (currentState == "findTower"):
                # if close enough, start alignment
                if (radius > constants.towerCloseThresh):
                    state.towerAligned = nav.align(ard, IRdata, bumpData)

                # if not close enough, get closer
                else:
                    (x,y), frame, radius = cyclop.findColor(frame, "purple")
                    if (radius > constants.towerFoundThresh):
                        nav.moveToX(ard, x)
                    else:
                        nav.explore(ard, IRdata)

            # score on the tower
            elif (currentState == "scoreTower"):
                ard.enemyCommand(1)
                time.sleep(5)
                ard.enemyCommand(0)
                state.ballsInHopper = 0
                state.towerFound = False
                state.towerAligned = False
                state.prevState = "scoreTower"

            # look for balls and the button, with priority on the button
            elif (currentState == "exploreButtonPriority"):
                (x,y), frame, radius = cyclop.findColor(frame, "cyan")
                if (x == -1.0 and y == -1.0):
                    state.buttonFound = False
                    nav.explore(ard, IRdata)                        
                else:
                    state.buttonFound = True

                if (state.buttonFound == False):
                    (x,y), frame, radius = cyclop.findColor(frame, findColor)
                    # if no ball is found- turn around
                    if (x == -1.0 and y == -1.0):
                        state.ballFound = False
                        nav.explore(ard, IRdata)                        
                    else:
                        state.ballFound = True

                state.prevState = "exploreButtonPriority"

            # look for balls
            elif (currentState == "exploreBallPriority"):
                (x,y), frame, radius = cyclop.findColor(frame, findColor)
                if (x == -1.0 and y == -1.0):
                    state.ballFound = False
                    nav.explore(ard, IRdata)
                        
                else:
                    state.ballFound = True

                state.prevState = "exploreBallPriority"

            elif (currentState == "pressButton"):
                ##################### alignment
                pass

            # scoring on the wall
            elif (currentState == "scoreWall"):

                (x,y), frame, radius = cyclop.findColor(frame, "yellow")
                nav.moveToX(ard, x)
                
                #### correct this to actually use IRs
                closeEnough = (radius > 45)

                if (closeEnough):
                    ard.enemyCommand(1)
                    time.sleep(5)
                    ard.enemyCommand(0)
            ## for debugging only
            time.sleep(0.5)
            cyclop.showImage(frame)
            
    except KeyboardInterrupt:
        cyclop.kill()

def kill():
    sys.exit(0)
    pass
    
if __name__ == '__main__': #called from the command line

    # connect to the Arduino
#    ard = arduino.Arduino()
#    ard.connect(debug=True)

    # connect to the virtualBot
    ard = virtualBot.VirtualBot()
    nav = navigation.Navigation()
    time.sleep(2) # wait for arduino to power up

    # turn on the helix and the intake roller
    ard.helixCommand(1)
    ard.intakeCommand(1)
    state = stateMachineSimplified.State()
    
    nav.backUpFromHit(ard)

    ## TODO - need the button press determine what color we are chasing
    run(state, ard, nav, "red")
    kill()
