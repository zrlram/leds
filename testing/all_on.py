#!/usr/bin/env python 

import sys
sys.path.append('..')
sys.path.append('.')
import opc

numLEDs = 512       # just use all pins on all channels
#client = opc.Client('192.168.30.158:7890')
client = opc.Client('localhost:7890')

black = [ (0,0,0) ] * numLEDs
red = (255,0,0)

on = [ (55, 55, 200) ] * numLEDs
on[0] = red

# reset first
client.put_pixels(black)
# make the first pixel red and set others to blue
client.put_pixels(on)
