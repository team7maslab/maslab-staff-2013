import arduinoSimpleSerial as ss
import time

ard = ss.Arduino()
time.sleep(1) # wait for arduino to power up
ard.connect(debug=True)

while True:
    ard.packetExchange()
    ard.serialRead()
    ard.retrieve('I')
    print(ard.receivedDict)
