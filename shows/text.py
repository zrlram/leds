import color
import color2

import random
import time

import looping_show
import tween
from font import font

class Text(looping_show.LoopingShow):
    # Because we extend LoopingShow we must explicitly override is_show to be True
    is_show = True
    
    name = "Text"

    def __init__(self, sheep_sides):
        looping_show.LoopingShow.__init__(self, sheep_sides)
        self.range = self.geometry.RINGS_AROUND
        self.width = 0

        self.duration = 0.2

        self.geometry.clear()

    def update_parameters(self, state):

        if state % 3 == 0:
            text = "HELLO RAFFY "
        if state % 3 == 1:
            text = "DMV  "
        if state % 3 == 2:
            text = "VIP  "

        self.text_pixels = self.pixelate (text)

        print "running %s with text %s" % (self.name, self.text)

    def pixelate(self, text):

        matrix = []
        for letter in text:
            l = self.digit_matrix(letter)

            for column in l:
                matrix.append(column)

            matrix.append([[0] * 5])          # spacer
            
        return matrix


    def digit_matrix(self,digit):

        over = 0
        dots = []

        char = ord(digit) 
        for height in range(5):
            character = font[char*5+height] 
            #print ord(digit), character

            byte = character & 0xff
            # a column in a character
            column = []
            for bit in reversed(range(1,6)):
                      
                if byte & 1 == 1:
                    column.append(1)
                else:
                    column.append(0)
                            
                byte = byte >> 1

            dots.append(list(reversed(column)))

        # print "c", char, dots

        return dots

    def digit(self,digit):

        over = 0
        dots = []

        char = ord(digit) 
        for height in range(5):
            character = font[char*5+height] 
            #print ord(digit), character

            byte = character & 0xff
            # a column in a character
            for bit in reversed(range(1,6)):
                      
                if byte & 1 == 1:
                    up = bit + 1
                    if up <= 0:             # SORRY - 0 does not exist
                        up = up -1
                    # print up, over
                    dots.append((over,up))
                            
                byte = byte >> 1
            over = over + 1

        return dots
                        
    def rotate(self, how_much):

        # read all - make a quick copy to not change in place

        bright = self.geometry.get_brightness()
        self.geometry.set_brightness(1.0)

        pixels = []
        for idx in range(self.geometry.get_nof_pixels()):
            temp = self.geometry.pixels[idx]
            pixels.append((temp[0], temp[1],temp[2]))

        self.geometry.clear()
        for x in range(len(self.range)):
            for y in range(14):
                try:
                    # read current value
                    led = self.range[x][y]
                    col = pixels[led]
                    # rotate x by 'how_much' 
                    # new_x = (x-how_much) % len(self.range)
                    new_x = (x-1)               # will be done "how_much" times
                    if new_x < 0: continue      # drop end
                
                    led = self.range[new_x][y]
                    #print str(col)
                    self.geometry.set_pixel(led, col)

                except Exception as ex:
                    #import traceback
                    #traceback.print_exc()
                    continue

        self.geometry.draw()

        self.geometry.set_brightness(bright)

    def update_at_progress(self, progress, new_loop, loop_instance):

        bg = color.hsv(0.0, 0.0, 0.0)

	hue = (loop_instance / 20.0) % 1.0
	if hue > 1.0:
	    hue -= 1.0
	hsv = (hue, 1.0, 1.0)

	rgbTuple = color2.hsvRYB_to_rgb(hsv)
	fg = (int(rgbTuple[0]), int(rgbTuple[1]), int(rgbTuple[2]))

        if new_loop:

            column = self.text_pixels[loop_instance % len(self.text_pixels)]

            # twirl me - one more time - by how much the current letter is wide plus 1 for the space
            self.rotate(1)

            for y,el in enumerate(column):
                led = self.range[len(self.range)-1][y+3]    # only one column written
                if el==1:
                    self.geometry.set_pixel(led, fg)
                else:
                    self.geometry.set_pixel(led, bg)

            self.geometry.draw()

__shows__ = [
              (Text.name, Text)
            ]
 
