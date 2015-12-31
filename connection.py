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
#row = [46, 46, 36, 31, 21, 16, 12, 12, 8, 0]
# optimized 10'
#row = [50, 50, 42, 35, 25, 18, 13, 10, 8, 0]
# measured 10' - ideally
#row = [46, 44, 44, 40, 36, 32, 28, 22, 16, 8]
# measured 10' - tinkered
row = [44, 44, 40, 36, 32, 28, 20, 12]

# the one I have been using all the time:
#row = [32, 32, 32, 32, 32, 32, 16, 16, 16, 8, 0]   # powers of 2
height = len(row) + 1        # this is only half of the sphere
                         # +1 because the height is plus one! 8 rows, but 9 is the top. Like there are 9 gaps with 8 poles in a fence ;)

# bottom only has 7 rows
numLEDs = sum(row) * 2 - 12
print "num LEDs: ", numLEDs
pixels = [ (0,0,0) ] * numLEDs
# draw()

def set_pixel(pos, color):
    pixels[pos] = color

def draw():
    client.put_pixels(pixels)
