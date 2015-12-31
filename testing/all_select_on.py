#!/usr/bin/env python 

# Open Pixel Control client: Every other light to solid white, others dark.

import sys
sys.path.append('..')
sys.path.append('.')
import opc

numLEDs = 512
#client = opc.Client('192.168.30.158:7890')
client = opc.Client('localhost:7890')

black = [ (0,0,0) ] * numLEDs
red = (255,0,0)

on = [ (55, 55, 200) ] * numLEDs
on[0] = red

# make the first pixel red though!
client.put_pixels(black)
client.put_pixels(on)

while 1:
    pixel = raw_input("Enter Pixel number: ")   # Python 2.x
    on[int(pixel)] = red
    client.put_pixels(on)

