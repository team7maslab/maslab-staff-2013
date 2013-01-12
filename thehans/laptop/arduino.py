import serial, subprocess, struct, numpy as np

debug = True
BAUD = 57600
port = None

names = ['/dev/ttyACM0', '/dev/ttyACM1', '/dev/tty.usbmodem621','COM4','COM5']
for name in names:
    try:
        port = serial.Serial(name, BAUD, timeout=.01)
        if port != name[-1]:
            subprocess.call(['stty', '-F', name, '-clocal'])
        break
    except:
        continue

print 'connected to port ' + str(port)

def format_bytes(bytes):
    return ' '.join([hex(ord(b)) for b in bytes])
  
def raw_command(response_fmt, data_fmt, *data):
    """Send a command to the arduino and receive a response."""
    port.flushInput()
    output = struct.pack('>' + data_fmt, *data)
    if debug: print('Sending {0}'.format(format_bytes(output)))
    port.write(output)
    response_data = port.read(struct.calcsize(response_fmt))
    if debug: print('Received {0}'.format(format_bytes(response_data)))
    try:
        return struct.unpack('>' + response_fmt, response_data)
    except:
        if debug: print("Invalid response")
        return None

def get_analog(channel):
    """Ask for an analog reading."""
    return raw_command('B', 'Bb', 2, channel)[0]

def is_alive():
    """Check whether the arduino is responding to commands."""
    pass
def get_start_mode():
    """Returns either IDLE, REGULAR, or AGGRESIVE."""
    pass

def get_voltage():
    pass



