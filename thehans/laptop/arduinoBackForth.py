# arduinoBackForth.py
import arduinoSimpleSerial as ss

ard = ss.Arduino()
ard.connect(debug=True)

ard.motorCommand(0.9)
#ard.turnCommand(-0.98)
ard.packetExchange()
##print ard.retrieve('M')

ard.motorCommand(-0.9)
ard.packetExchange()

ard.motorCommand(0)
ard.packetExchange()

ard.motorCommand(0.5)
ard.packetExchange()

ard.motorCommand(0)
ard.packetExchange()
