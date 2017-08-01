import color

import random

import looping_show
import tween

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
        if loop_instance % 2 == 0:
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


        # Step 3: progressively erase again
        elif loop_instance % 3 == 2:
            pass

        self.geometry.draw()

__shows__ = [
              (Path.name, Path)
            ]
 
