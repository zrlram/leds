import color

import random

import looping_show
import tween

class Mapping(looping_show.LoopingShow):
    # Because we extend LoopingShow we must explicitly override is_show to be True
    is_show = True
    
    name = "Mapping"

    def __init__(self, sheep_sides):
        looping_show.LoopingShow.__init__(self, sheep_sides)
        self.range = self.geometry.RINGS_AROUND

        self.picture = []
        row_1=[0,0,1,1,0,0,0,1,1,0,0,0,0,0,0,0]
        row_2=[0,1,1,1,1,0,1,1,1,1,0,0,0,0,0,0]
        row_3=[0,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0]
        row_4=[0,0,1,1,1,1,1,1,1,0,0,0,0,0,0,0]
        row_5=[0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0]
        row_6=[0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0]
        row_7=[0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0]
        self.picture.append(row_7)
        self.picture.append(row_6)
        self.picture.append(row_5)
        self.picture.append(row_4)
        self.picture.append(row_3)
        self.picture.append(row_2)
        self.picture.append(row_1)
        for i in range(7):
            self.picture.append([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
            

    def update_at_progress(self, progress, new_loop, loop_instance):

        fg = color.hsv(1.0, 0.8, 0.8)
        bg = color.hsv(0.0, 0.0, 0.0)

        # 32/2 x 14 images
        # 16 over, 14 up
        height = 14
        width = 16

        #print "LLL", len(self.picture), len(self.picture[0])

        for x in range(width):
            for y in range(height):

                if self.picture[y][x] == 1:
                    c = fg
                else:
                    c = bg
                led = 0
                try:
                    led = self.range[len(self.range)-1-x][y]
                except:
                    #print "except:", x,y
                    continue
                self.geometry.set_pixel(led, c)

        self.geometry.draw()

__shows__ = [
              (Mapping.name, Mapping)
            ]
 
