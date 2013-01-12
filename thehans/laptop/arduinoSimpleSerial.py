import sys
import serial, time
sys.path.append("../../lib")

class Arduino:

    def __init__(self):
        self.killedReceived = False

    # Start the connection and the thread that communicates with the arduino
    def run(self):
        self.portOpened = self.connect()
        self.checkPorts()

    # Create the serial connection to the arduino
    def connect(self):
        print "Connecting"
        names = ['COM5','COM10']
        for name in names:
            try:
                # Try to create the serial connection
                self.port=serial.Serial(name, baudrate=9600, timeout=0.5)
                if self.port.isOpen():
                    time.sleep(2) # Wait for Arduino to initialize
                    print "Connected on " + name
                    return True
            except:
                print "Arduino not connected on " + name
        print "Failed to connect"
        return False

    def sendData(self):
        while not self.killedReceived:
            output = 'M'
            self.port.write(output)
            finishedReceiving = False
            while not finishedReceiving:
                t = self.serialRead()
                if t == ';':
                    finishedReceiving = True
                    exit()
                    
    def serialRead(self, size=1):
        inp = self.port.read(size)
        print inp
        if (len(inp) < size):
            return chr(0)
        #while (inp == "/"):
        #    while inp != "\\":
        #        sys.stdout.write(inp)
        #        inp = self.port.read()
        #    inp = self.port.read(size)
        return inp


ard = Arduino()
ard.connect()
ard.sendData()


