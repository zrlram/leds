#!/usr/bin/env python 

# Open Pixel Control client: Every other light to solid white, others dark.

import sys, time, getopt
sys.path.append('..')
sys.path.append('.')
import opc

numLEDs = 512
#client = opc.Client('192.168.30.158:7890')
client = opc.Client('localhost:7890')

all_black = [ (0,0,0) ] * numLEDs
red = (255,0,0)
yellow = (255,255,0)
black = (0,0,0)
blue = (55,55,200)

on = [ (55, 55, 200) ] * numLEDs
on[0] = red

# make the first pixel red though!
client.put_pixels(all_black)
client.put_pixels(on)

pixel = 128
try:
	opts, args = getopt.getopt(sys.argv[1:],"p:")
except getopt.GetoptError:
	print 'all_run_aroudn.py -p <nof_pixels>'
	sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
	print 'all_run_aroudn.py -p <nof_pixels>'
	sys.exit()
    elif opt in ("-p"):
	pixel = int(arg)

if pixel == 0: 
	pixel = int(raw_input("How many pixel active?"))

print "Playing with %s pixels" % pixel
on[0] = red

while 1:
    for a in range(0, pixel):
        on[a] = yellow
        client.put_pixels(on)
        time.sleep(0.2)
        on[a] = blue
        client.put_pixels(on)
        print a


