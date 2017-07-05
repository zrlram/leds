import color2
import random, tween
import looping_show

class RingTester(looping_show.LoopingShow):
    # Because we extend LoopingShow we must explicitly override is_show to be True
    is_show = True
    
    name = "Ring Tester"
    ok_for_random = False

    def __init__(self, sheep_sides):
        looping_show.LoopingShow.__init__(self, sheep_sides)
        self.duration = 2 
        self.mode = 2      
        self.range = []

        #self.was_selected_randomly()

    def update_parameters(self, state):
        # mode: 0 = self.mode=0 and HOR_RINGS, 3 = self.mode=0 and VERT_RINGS
        self.range = self.geometry.HOR_RINGS_TOP_DOWN
        r = "HOR_RINGS_TOP_DOWN"
        if self.mode == 1:
            self.range = self.geometry.VERT_RINGS
            r = "VERT_RINGS"

        if self.mode == 2:
            self.range = self.geometry.RINGS_AROUND
            r = "RINGS_AROUND"

        print "running %s in mode %s, range %s" % (self.name, state, r)

    def update_at_progress(self, progress, new_loop, loop_instance):

        v_range = tween.easeInQuad(0.1, 0.98, (self.cm.brightness + 1.0)/2.0)
        per_slice = v_range / 4
        # Color striped from top to bottom by slices
        for idx, sl in enumerate(self.range):
            hue = (idx * 1.1* per_slice)
            while hue > 1.0:
                hue -= 1.0
            while hue < 0.0:
                hue += 1.0

            hsv = (hue, 1.0, 1.0)
            rgbTuple = color2.hsvRYB_to_rgb(hsv)
            for i in sl:
                self.geometry.set_pixel(i, rgbTuple)

        self.geometry.draw()

__shows__ = [
              (RingTester.name, RingTester)
            ]
 
