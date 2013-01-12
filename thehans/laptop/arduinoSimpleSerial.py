import serial, subprocess, struct, numpy as np

debug = True
BAUD = 9600
port = None

def connect():
        global port
        print "Connecting"
        # Loop through possible values of ACMX, and try to connect on each one
        for i in [5]:
            try:
                # Try to create the serial connection
                port=serial.Serial(port='COM{0}'.format(i), baudrate=9600, timeout=0.5)
                if port.isOpen():
                    time.sleep(2) # Wait for Arduino to initialize
                    print "Connected"
                    return True
            except:
                # Some debugging prints
                print "Arduino not connected on COM{0}".format(i)
        print "Failed to connect"
        return False

def serialRead(size=1):
    inp = port.read(size)
    if (len(inp) < size):
        return chr(0)
        #while (inp == "/"):
        #    while inp != "\\":
        #        sys.stdout.write(inp)
        #        inp = self.port.read()
        #    inp = self.port.read(size)
    return inp

def raw_command():
    global port
    """Send a command to the arduino and receive a response."""
    connect()
    while True:
        port.write("M")
    
    done = False
    killbot = False
    
    while not killbot:

        output = ""
        output += 'M'
        port.write("M")
        print port
        
        # while not done:
            # Read in the mode
            # print "Reading mode"
            # mode = serialRead()
            # print mode
            # if (mode == chr(0)):
                # print "Timeout"
                # break
            # if (mode == ';'):
                # done = True
    
def get_analog(channel):
    """Ask for an analog reading."""
    pass

def is_alive():
    """Check whether the arduino is responding to commands."""
    pass
def get_start_mode():
    """Returns either IDLE, REGULAR, or AGGRESIVE."""
    pass

def get_voltage():
    """Returns voltage on Robot"""
    pass

connect()
while True:
    port.write("M")

