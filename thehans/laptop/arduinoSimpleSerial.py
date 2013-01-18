import serial, time, math, glob

class Arduino:

    port = None
    
    def __init__(self):
        self.dataSent = False
        self.outputDict = {}
        self.receivedDict = {}
        self.dataFMT = {'M':(1,1),'K':(2,2)}
        self.debug = False
        self.packetCount = 0
        
    # Start the connection and the thread that communicates with the arduino
    def run(self):
        self.portOpened = self.connect()
        self.checkPorts()

    # Create the serial connection to the arduino
    def connect(self, debug=False):
        self.debug = debug
        if self.debug: print "Connecting..."
        names = ['COM5','COM6','COM11','/dev/ttyACM0', '/dev/ttyACM1']
        for name in names:
            try:
                # Try to create the serial connection
                self.port=serial.Serial(name, baudrate=9600, timeout=0.5)
                if self.port.isOpen():
                    time.sleep(2) # Wait for Arduino to initialize
                    print "Connected on " + name
                    return True
            except:
                if self.debug: print "Arduino not connected on " + name
        if self.debug: print "Failed to connect."
        exit()
        return False

    # Sends the data from the computer, and reads the response
    def packetExchange(self, query=False):
        while not self.dataSent:
            self.packetCount += 1
            if query == True:
                output = "Q;"
            else:
                output = self.formatTransmitData()
            if self.debug: print "Transmitting Data: " + output

            ##debug:
            # output = 'M'
            
            self.port.write(output)
            self.serialRead()
            if self.debug: print "Received Data: " + str(self.receivedDict)
            
            self.dataSent = True

        self.dataSent = False
        self.flushDictionary()

    # Converts the dictionary of data into the laptop-arduino protocol
    def formatTransmitData(self):
        data = ""
        for key, value in self.outputDict.iteritems():
            data += key + str(value)
        data = data + ";"
        return data

    # Read the serial and store the results as a dictionary
    def serialRead(self, size=1):
        dataEnded = False
        self.receivedDict = {}
        storage = ""
        while not dataEnded:
            inp = self.port.read(size)
            tempData = []
            if inp in self.dataFMT.keys():
                numItems,length  = self.dataFMT[inp]
                for i in range(numItems):
                    tempData.append(self.port.read(length))
                self.receivedDict[inp] = tempData
            self.receivedDict['PK'] = self.packetCount
            if inp == ";" or inp == "":
                dataEnded = True
        return inp

    # Motor controls
    def motorCommand(self, speed):
        """Set the drive motors.  Speeds range from -1.0 to 1.0"""
        if speed >= 0:
            self.outputDict['F'] = int(max(speed*10,9))
        else:
            self.outputDict['B'] = int(max(math.fabs(speed*10),9))

    # Turn controls     
    def turnCommand(self, heading):
        """Turn in a direction. Headings range from -1.0 to 1.0"""
        if heading >= 0:
            self.outputDict['R'] = int(max(heading*10, 9))
        else:
            self.outputDict['L'] = int(max(math.fabs(heading*10),9))

    # Helix controls
    def helixCommand(self, mode):
        """0 is off, 1 is on"""
        self.outputDict['H'] = int(mode)
        
    # Intake controls
    def intakeCommand(self, mode):
        """0 is off, 1 is on"""
        self.outputDict['G'] = int(mode)

    # Arm controls
    def armCommand(self, mode):
        """0 is the arm up, 1 is the arm down"""
        self.outputDict['A'] = int(mode)

    # Enemy hopper roller controls
    def enemyCommand(self, mode):
        """0 is off, 1 is on"""
        self.outputDict['E'] = int(mode)
        
    # Starts the Helix and Intake Roller
    def startCommand(self):
        """Starts the main robot functions"""
        self.helixCommand(1)
        self.intakeCommand(1)
        self.armCommand(0)
        self.enemyCommand(0)
                
    # Dumps the dictionary that holds the values to be output     
    def flushDictionary(self):
        """Empties the dictionary of values to be transmitted"""
        self.outputDict = {}

    # Request for a value from the Arduino, returns value based on receivedDict
    def retrieve(self, key):
        """Retrieves the value for an Arduino input, based on dataFMT"""
        if key == 'PK':
            return self.receivedDict['PK']
        else:
            values = self.receivedDict[key]
            for i in range(len(values)):
                values[i] = int(values[i])
            return values

   
##ard = Arduino()
##ard.connect(debug=True)
##
##ard.motorCommand(0.9)
##ard.turnCommand(-0.98)
##ard.packetExchange()
##print ard.retrieve('M')
