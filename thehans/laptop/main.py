import arduinoSimpleSerial as arduino
import time, eye, random, sys

def run():

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

    sleepTime = 0.2
    turnTime = 1/sleepTime
    turnDir = random.randrange(-10, 10, 1)
    
    cyclop = eye.Eye(debug=True)
    try:
        while True:
            frame = cyclop.getFrame()
            if (findColor == "green"):
                (x,y), frame = cyclop.findGreenBall(frame)
            else:
                (x,y), frame = cyclop.findRedBall(frame)
            
    #        print (x,y)

            if (x == 0 and y == 0):      # no ball found
                # wander until you find a ball
                # change directions every second
                ard.motorCommand(0.5)
                if (turnTime == 0):
                    turnTime = 1/sleepTime
                    turnDir = random.randrange(-10, 10, 1)/10.0
                ard.turnCommand(turnDir)
                turnTime -= 1

                
            ard.motorCommand(0.5)
            ard.turnCommand(x)
            cyclop.showImage(frame)
            ard.packetExchange()
            time.sleep(sleepTime)
    except KeyboardInterrupt:
        cyclop.kill()
            
        print 'mode ' + mode + ' initiated'

    pass

def kill():
    sys.exit(0)
    pass
    
if __name__ == '__main__': #called from the command line


    ard = arduino.Arduino()
    time.sleep(1) # wait for arduino to power up
    ard.connect(debug=True)

    run()
    time.sleep(100)
    kill()
