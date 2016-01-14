#!/usr/bin/env python 
import sys

sys.path.append('..')
sys.path.append('.')
import opc

numLEDs = 500
#client = opc.Client('192.168.30.158:7890')
client = opc.Client('localhost:7890')

black = [ (0,0,0) ] * numLEDs

client.put_pixels(black)
