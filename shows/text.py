import color

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

        self.duration = 0.5

        self.text_pixels = self.pixelate ("HELLO RAFFY ")

        self.geometry.clear()

    def pixelate(self, text):

        matrix = []
        for letter in text:
            path = self.digit(letter)

            # calculate width of current character to delete after
            if self.text[letter] == " ":
                width = 1      # for space
            else:
                width = max([x for (x,y) in path]) + 1

            for col in range(width):
                column = [0,0,0,0,0]         # letter height
                for (x,y) in path:
                    column[x] = 1
                matrix.append(column)
            
            print matrix



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

        fg_bright = color.hsv(0.1, 0.5, 0.2)
        fg = color.hsv(0.5, 0.4, 1.0)
        bg = color.hsv(0.0, 0.0, 0.0)

        if new_loop:
            #path = self.digit(str(loop_instance % 10))
            letter = loop_instance%len(self.text)
            path = self.digit(self.text[letter])

            # remember how wide old character is to delete after rotate
            # necessary after one rotation
            old_width = self.width

            return 
            print "letter, width, old_width", self.text[letter], self.width, old_width

            # twirl me - one more time - by how much the current letter is wide plus 1 for the space
            for iter in range(self.width + 1):
                self.rotate(1)
                time.sleep(0.2)

            start = len(self.range) - self.width
            old_start = len(self.range) - old_width

            # clear letter area - needed after a full rotation
            for x in range(old_width):
                for y in range(1,7):
                    led = self.range[old_start+x][y+1]
                    self.geometry.set_pixel(led, fg_bright)

            # write in the negative area for rotational - drop purposes
            print path
            for (x,y) in path:
                led = self.range[start+x][y+1]
                self.geometry.set_pixel(led, fg)


            self.geometry.draw()

__shows__ = [
              (Text.name, Text)
            ]
 
