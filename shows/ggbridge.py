import color

import random

import looping_show
import tween
from math import sin

class GGBridge(looping_show.LoopingShow):
    # Because we extend LoopingShow we must explicitly override is_show to be True
    is_show = True
    
    name = "GGBridge"

    def __init__(self, sheep_sides):
        looping_show.LoopingShow.__init__(self, sheep_sides)
        self.range = self.geometry.RINGS_AROUND
        self.duration = 4.0

        self.GGBridge = []
	row_y=[0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0]
	row_x=[0,0,0,0,0,0,0,4,3,4,0,0,0,0,0,0,0]
	row_0=[0,0,0,0,0,0,4,3,3,3,4,0,0,0,0,0,0]
	row_1=[0,0,0,0,1,0,0,4,3,4,0,0,1,0,0,0,0]
	row_2=[0,0,0,1,1,1,0,0,4,0,0,1,1,1,0,0,0]
	row_3=[0,0,1,0,1,0,1,0,0,0,1,0,1,0,1,0,0]
	row_4=[0,1,0,0,1,0,0,1,0,1,0,0,1,0,0,1,0]
	row_5=[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]       # bridge
	row_6=[0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0]
	row_7=[0,5,5,0,1,5,0,5,0,5,5,0,1,5,0,5,0]
	row_8=[2,2,2,2,1,2,2,2,2,2,2,2,1,2,2,2,2]       # water

        self.GGBridge.append(row_8)
        self.GGBridge.append(row_7)
        self.GGBridge.append(row_6)
        self.GGBridge.append(row_5)
        self.GGBridge.append(row_4)
        self.GGBridge.append(row_3)
        self.GGBridge.append(row_2)
        self.GGBridge.append(row_1)
        self.GGBridge.append(row_0)
        self.GGBridge.append(row_x)
        self.GGBridge.append(row_y)
        for i in range(3):
            self.GGBridge.append([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])

	self.geometry.clear()

    def update_at_progress(self, progress, new_loop, loop_instance):

        blue = color.hsv(0.6,0.9,1.0)
        red = color.hsv(0, 1.0, 1.0)   
        yellow = color.hsv(0.2, 0.7, 1.0)
        bg = color.hsv(0.0, 0.0, 0.0)

        where = progress
            
        # 32/2 x 14 images
        # 16 over, 14 up
        height = 14
        width = 16
        image = self.GGBridge     # life is generally happy

        #print "LLL", len(self.picture), len(self.picture[0])

        for x in range(width):
            for y in range(height):

                wave_random = (x-random.randint(0,1)) % width
                if image[y][x] == 3:        # sun
                    c = yellow
                elif image[y][x] == 4:        # sun
                    c = yellow
                    sun = abs(0.5 * sin(loop_instance + progress))
                    c = color.set_V(c, absolute=sun)  
                elif image[y][x] == 1:      # bridge
                    c = red                        
                elif image[y][x] == 2:      # ocean
                    c = blue                     
                elif image[y][wave_random] == 5:      # waves
                    c = blue                     
                    wave_height = abs(0.4 * sin((loop_instance + progress)*8))
                    c = color.set_V(c, absolute=(wave_height)) 
                else:
                    c = bg

                # first side
                led = 0
                try:
                    led = self.range[x][y]
                except:
                    #print "except:", x,y
                    continue
                self.geometry.set_pixel(led, c)
                
                # other side
                led = 0
                try:
                    led = self.range[len(self.range)/2+x][y]
                except:
                    #print "except:", x,y
                    continue
                self.geometry.set_pixel(led, c)

        self.geometry.draw()

__shows__ = [
              (GGBridge.name, GGBridge)
            ]
 
