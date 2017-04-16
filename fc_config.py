import socket
import struct

'''
Usage:
ipython fc_config.py
set_noInterp()
# set it back
noInterp = 0
update()
'''


noDither = 0 #check("Disable dithering")
noInterp = 0 #check("Disable interpolation")
manualLED = 0 #check("Built-in LED under manual control")
ledOnOff = 0 #check("Built-in LED manual on/off")

def setFirmwareConfig(data):

    s = socket.socket()
    s.connect(('localhost', 7890))
    s.send(struct.pack(">BBHHH", 0, 0xFF, len(data) + 4, 0x0001, 0x0002) + data)
    print "sent", struct.pack(">BBHHH", 0, 0xFF, len(data) + 4, 0x0001, 0x0002) + data

def update():
    setFirmwareConfig(chr(
        noDither |
        (noInterp << 1) |
        (manualLED << 2) |
        (ledOnOff << 3) ))

def set_noDither():
    global noDither
    noDither = 1
    update()

def set_noInterp():
    global noInterp
    noInterp = 1
    update()

def set_manualLED():
    global manualLED
    manualLED = 1
    update()

def set_ledOnOff():
    global ledOnOff
    ledOnOff = 1
    update()
