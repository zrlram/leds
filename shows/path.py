import color, color2

import random

import looping_show
import tween
import morph

class Path(looping_show.LoopingShow):
    # Because we extend LoopingShow we must explicitly override is_show to be True
    is_show = True
    
    name = "Path"

    def __init__(self, sheep_sides):
        looping_show.LoopingShow.__init__(self, sheep_sides)
        self.range = self.geometry.RINGS_AROUND
        self.duration = 1.0
        self.path = [ (0,5), (1,6), (1,5), (2,7), (2,5), (3,8), (3,5), (4,9), (4,5), (5,10),
                      (5,5), (6,11), (6,5), (7,12), (7,5)
                    ]
        self.geometry.clear()

        start = color2.HSV(0.6,0.9,1.0)      # blue
        end = color2.HSV(0,0,1.0)   # white
        self.color_range = morph.transition_list(start, end, steps=9)


    def update_at_progress(self, progress, new_loop, loop_instance):

        sat = progress
        hue = (loop_instance / 20.0) % 1.0
        fg = color.hsv(hue, sat, 0.8)
        bg = color.hsv(0.0, 0.0, 0.0)

        # 32/2 x 14 images
        # 16 over, 14 up
        height = 14
        width = 16

        (x,y) = self.path[int(progress*len(self.path))]


        # Step 1: progressivly build up
        if loop_instance % 2 == 40:
            # to draw back side too
            for a in range(2):
                start = len(self.range) 
                if a == 0:
                    start = len(self.range) / 2

                try:
                    # regular image
                    led = self.range[start-1-x][y]
                    self.geometry.set_pixel(led, fg)
                    # mirror on y
                    led = self.range[start % len(self.range) + x][y]
                    self.geometry.set_pixel(led, fg)
                    # mirror on x
                    led = self.range[start-1-x][10-y]
                    self.geometry.set_pixel(led, fg)
                    # mirror on x and y
                    led = self.range[start % len(self.range) + x][10-y]
                    self.geometry.set_pixel(led, fg)
                except:
                    #print "except:", x,y
                    pass
            
        merses = [4, 4, 8, 8, 16, 16, 32, 32]
        mers = merses[loop_instance % len(merses)]

        if loop_instance % 2 == 0:
            # light up all the main meridians
            for four in range (mers):
                meridian = int(four*len(self.range)/mers)
                for idx, led in enumerate(self.range[meridian]):
                    
                    #l = abs(idx - 5)  / (len(self.range[meridian]) * 1.0) 
                    l = (abs(idx - 5) - int(progress * 9) ) % 9
                    #l = idx - 5 + (progress * len(self.range[meridian]))) / len (self.range[meridian])
                    if l >= int(progress*9):
                        hsv = self.color_range[l]
                        hsv = hsv.hsv
                        hsv = color.hsv(min(hsv[0],1.0), abs(min(hsv[1],1.0)), min(hsv[2],1.0))
                        self.geometry.set_pixel(led, hsv)

        if loop_instance % 2 == 1:
            # light up all the main meridians
            for four in range (mers):
                meridian = int(four*len(self.range)/mers)
                for idx, led in enumerate(self.range[meridian]):
                    
                    #l = abs(idx - 5)  / (len(self.range[meridian]) * 1.0) 
                    l = (abs(idx - 5) + int(progress * 9) ) % 9
                    #l = idx - 5 + (progress * len(self.range[meridian]))) / len (self.range[meridian])
                    if l < int(progress*9):
                        hsv = self.color_range[l]
                        hsv = hsv.hsv
                        hsv = color.hsv(min(hsv[0],1.0), abs(min(hsv[1],1.0)), min(hsv[2],1.0))
                        self.geometry.set_pixel(led, hsv)

        if loop_instance % 8== 0 and loop_instance > 4:
            # blend to black!
            for i in range(self.geometry.get_nof_pixels()):
                temp = self.geometry.pixels[i]
                col = color.set_V(temp, absolute = 1.0-progress)
                self.geometry.set_pixel(i, col)

        '''
        # Step 2: rotate
        elif loop_instance % 2 == 1 and new_loop:
            # read all - make a quick copy to not change in place
            
            pixels = []
            for idx in range(self.geometry.get_nof_pixels()):
                temp = self.geometry.pixels[idx]
                pixels.append((temp[0], temp[1],temp[2]))

            bright = self.geometry.get_brightness()
            self.geometry.set_brightness(1.0)

            for x in range(len(self.range)):
                for y in range(14):
                    try:
                        # read current value
                        led = self.range[x][y]
                        col = pixels[led]
                        # rotate x by 1
                        new_x = (x+1) % len(self.range)
                    
                        led = self.range[new_x][y]
                        #print str(col)
                        self.geometry.set_pixel(led, col)
                        self.geometry.draw()

                    except Exception as ex:
                        #import traceback
                        #traceback.print_exc()
                        continue
                

            self.geometry.set_brightness(bright)
        '''

        self.geometry.draw()

__shows__ = [
              (Path.name, Path)
            ]
 
