import arduinoSimpleSerial as arduino
import time, eye

def run():

    #Waiting for button press on robot to denote start
    print 'connected! waiting for button press'
    # mode = 0
    # while mode == 0:
    #    ard.packetExchange(query=True)
    #    mode = ard.retrieve('M')[0]
    #    print mode
    #    time.sleep(.02) # check until mode is specified
    
    cyclop = eye.Eye(debug=True)
    
    while True:
        frame = cyclop.getFrame()
        (x,y), d = cyclop.findRedBall(frame)
        print (x,y)
        ard.motorCommand(0.3)
        ard.turnCommand(x)
        # cyclop.showImage(frame)
        ard.packetExchange()
        
    print 'mode ' + mode + ' initiated'

    
    pass

def kill():
    pass
    
if __name__ == '__main__': #called from the command line
    ard = arduino.Arduino()
    time.sleep(1) # wait for arduino to power up
    ard.connect(debug=True)

    run()
    kill()
