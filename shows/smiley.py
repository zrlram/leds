import color

import random

import looping_show
import tween

class Smiley(looping_show.LoopingShow):
    # Because we extend LoopingShow we must explicitly override is_show to be True
    is_show = True
    
    name = "Smiley"

    def __init__(self, sheep_sides):
        looping_show.LoopingShow.__init__(self, sheep_sides)
        self.range = self.geometry.RINGS_AROUND

        '''
	   .1'''''''1. 
	  1           1
	 1    11 11    1
	1     11 11     1
	1               1
	1   1       1   1
	 1   '11111'   1
	  1           1 
	   `1,,,,,,,1'

	%s/
        '''
        self.smiley = []
	row_0=[0,0,0,0.5,1,0.5,0.5,0.5,0.5,0.5,0.5,0.5,1,0.5,0,0,0]
	row_1=[0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0]
	row_2=[0,1,0,0,0,0,1,1,0,1,1,0,0,0,0,1,0,0]
	row_3=[1,0,0,0,0,0,1,1,0,1,1,0,0,0,0,0,1,0,0]
	row_4=[1,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,1,0,0]
	row_5=[1,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,1,0,0]
	row_6=[0,1,0,0,0,0.5,1,1,1,1,1,0.5,0,0,0,1,0,0]
	row_7=[0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0]
	row_8=[0,0,0,0.5,1,0.5,0.5,0.5,0.5,0.5,0.5,0.5,1,0.5,0,0]

        self.smiley.append([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
        self.smiley.append(row_8)
        self.smiley.append(row_7)
        self.smiley.append(row_6)
        self.smiley.append(row_5)
        self.smiley.append(row_4)
        self.smiley.append(row_3)
        self.smiley.append(row_2)
        self.smiley.append(row_1)
        self.smiley.append(row_0)
        for i in range(6):
            self.smiley.append([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])


    def update_at_progress(self, progress, new_loop, loop_instance):

        fg_bright = color.hsv(0.1, 0.5, 1.0)
        fg = color.hsv(0.2, 0.9, 1.0)
        bg = color.hsv(0.0, 0.0, 0.0)
        boost = 20

        where = progress
            
        color_state = tween.easeInQuad(0.98, 0.3, where)

        # 32/2 x 14 images
        # 16 over, 14 up
        height = 14
        width = 16
        image = self.smiley

        #print "LLL", len(self.picture), len(self.picture[0])

        for x in range(width):
            for y in range(height):

                if image[y][x] > 0:
                    c = fg
                    c = color.set_V(c, absolute=image[y][x] * color_state)  
                else:
                    c = bg

                # first side
                led = 0
                try:
                    led = self.range[len(self.range)-1-x][y]
                except:
                    #print "except:", x,y
                    continue
                self.geometry.set_pixel(led, c)
                
                # other side
                led = 0
                try:
                    led = self.range[len(self.range)/2-1-x][y]
                except:
                    #print "except:", x,y
                    continue
                self.geometry.set_pixel(led, c)

        self.geometry.draw()

__shows__ = [
              (Smiley.name, Smiley)
            ]
 
