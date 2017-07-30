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
        self.duration = 1.0

        self.picture = []
        row_1=[0,0,1,1,0,0,0,1,1,0,0,0,0,0,0,0]
        row_2=[0,1,1,1,1,0,1,1,1,1,0,0,0,0,0,0]
        row_3=[0,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0]
        row_4=[0,0,1,1,1,1,1,1,1,0,0,0,0,0,0,0]
        row_5=[0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0]
        row_6=[0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0]
        row_7=[0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0]
        self.picture.append([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
        self.picture.append([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
        self.picture.append(row_7)
        self.picture.append(row_6)
        self.picture.append(row_5)
        self.picture.append(row_4)
        self.picture.append(row_3)
        self.picture.append(row_2)
        self.picture.append(row_1)
        for i in range(7):
            self.picture.append([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
            
        self.heart_big = []
        row_0=[0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0]
        row_1=[0,1,1,1,0,0,0,1,1,1,0,0,0,0,0,0]
        row_2=[1,1,1,1,1,0,1,1,1,1,1,0,0,0,0,0]
        row_3=[1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0]
        row_4=[0,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0]
        row_5=[0,0,1,1,1,1,1,1,1,0,0,0,0,0,0,0]
        row_6=[0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0]
        row_7=[0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0]
        row_8=[0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0]
        row_9=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.heart_big.append(row_9)
        self.heart_big.append(row_8)
        self.heart_big.append(row_7)
        self.heart_big.append(row_6)
        self.heart_big.append(row_5)
        self.heart_big.append(row_4)
        self.heart_big.append(row_3)
        self.heart_big.append(row_2)
        self.heart_big.append(row_1)
        self.heart_big.append(row_0)
        for i in range(6):
            self.heart_big.append([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])


    def update_at_progress(self, progress, new_loop, loop_instance):

        fg_bright = color.hsv(0.1, 0.5, 1.0)
        fg = color.hsv(0.0, 1.0, 1.0)
        bg = color.hsv(0.0, 0.0, 0.0)

        color_state = tween.easeInQuad(0.98, 0.3, progress)

        # 32/2 x 14 images
        # 16 over, 14 up
        height = 14
        width = 16
        image = self.picture 
        if progress < 0.5:
            image = self.heart_big

        #print "LLL", len(self.picture), len(self.picture[0])

        for x in range(width):
            for y in range(height):

                if image[y][x] == 1:
                    c = fg
                    diff = (self.heart_big[y][x] - self.picture[y][x]) * 0.5
                    if diff<=0: diff = 1.0
                    c = color.set_V(c, absolute=color_state * diff)  # in the second image
                                                                     # we set the value to 0.5 
                                                                     # that way the outer heart
                                                                     # fades out
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
              (Mapping.name, Mapping)
            ]
 
