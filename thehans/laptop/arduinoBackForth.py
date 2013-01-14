# arduinoBackForth.py
import arduinoSimpleSerial as ss

ard = ss.Arduino()
ard.connect(debug=True)

ard.motorCommand(0.1)
ard.turnCommand(-0.98)
ard.packetExchange()
##print ard.retrieve('M')

