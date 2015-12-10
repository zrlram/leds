#!/usr/bin/env python

import opc

#client = opc.Client('localhost:7890')
client = opc.Client('192.168.30.158:7890')
#row = [40, 38, 35, 33, 30, 28, 24, 16, 9, 4, 0]  
#row = [40, 40, 40, 32, 32, 32, 24, 24, 16, 8, 0]  
#row = [40, 40, 32, 32, 24, 24, 24, 16, 16, 8, 0]   # 512, multiples of 8
#row = [40, 36, 32, 32, 28, 24, 20, 16, 16, 12, 0]   # 512, multiples of 4

# measured
#row = [40, 38, 32, 28, 20, 14, 10, 0]  
# 10' ball
row = [50, 48, 40, 35, 25, 18, 13, 10, 8, 0]


# the one I have been using all the time:
#row = [32, 32, 32, 32, 32, 32, 16, 16, 16, 8, 0]   # powers of 2
height = len(row)-1        # this is only half of the sphere
                         # -1 because the height is minues one! LOL

numLEDs = sum(row) * 2
print "num LEDs: ", numLEDs
pixels = [ (0,0,0) ] * numLEDs
# draw()

def set_pixel(pos, color):
    pixels[pos] = color

def draw():
    client.put_pixels(pixels)
