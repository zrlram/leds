#!/usr/bin/env python 

# Open Pixel Control client: Every other light to solid white, others dark.

import sys
sys.path.append('..')
import opc

numPairs = 256
#client = opc.Client('192.168.30.158:7890')
client = opc.Client('localhost:7890')

black = [ (0,0,0), (0,0,0) ] * numPairs
white = [ (155,55,55), (55, 55, 200) ] * numPairs

# Fade to white
client.put_pixels(black)
client.put_pixels(white)
