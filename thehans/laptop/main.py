import arduino, time

time.sleep(1) # wait for arduino to power up
# assert arduino.is_alive(), "Arduino not Detected"
# assert arduino.get_voltage() > 8, "battery not present or voltage low"

def run():
    print 'ready! waiting for button press'
    while arduino.get_start_mode() == 'IDLE':
        time.sleep(.02) # check until mode is specified
    pass

def kill():
    pass
    
if __name__ == '__main__': #called from the command line
    run()
    kill()
