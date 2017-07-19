from color2 import hsv_to_rgb, RGB
import color
import time
from randomcolor import random_color
import morph
import audio
from math import ceil, sin

import looping_show

# Make the components of a color add up to 1
def normalize_colors(color_stream):
	for colors in color_stream:
		yield [(r/(r+g+b), g/(r+g+b), b/(r+g+b)) for r,g,b in colors]

# Makes a list of colors. Each LED's color function is offset by 1 second 
def generate_colors(num_leds):
        from colorsys import hsv_to_rgb
	while True:
		t = time.time()
		values = [waveform(t, n) for n in range(num_leds)]
		colors = [hsv_to_rgb(y, 1, 1) for y in values]
		yield colors

def g_0(t, n):
	return sin(.1*n + sin(t*.27)*4)
def g_1(t, n):
	return sin(.3*n + sin(t*.17)*3)

waveforms = [g_0, g_1]

def waveform(t, n):
	total = sum([g(t,n) for g in waveforms]) / len(waveforms) # -1 to 1
	total += 1.0 # 0 to 2
	total /= 2.0 # 0 to 1
	return total

# Multiply each LED's color by its magnitude and a scalar
def multiply_colors(color_stream, magnitude_stream, scalar):
        colors = color_stream.next()
        mags = magnitude_stream.next()
        def scale((r,g,b), magnitude):
                magnitude = scalar * magnitude
                return (r*magnitude),(g*magnitude),(b*magnitude)
        yield [scale(color,mag) for color,mag in zip(colors,mags)]

# Max the colors out at the cap value and turn them to integers
def cap_colors(color_stream, cap):
	for colors in color_stream:
		for i in range(len(colors)):
			r,g,b = colors[i]
			if r+g+b > cap:
				total = r+g+b
				r = float(r) / total * cap
				g = float(g) / total * cap
				b = float(b) / total * cap
			r,g,b = int(r),int(g),int(b)
			colors[i] = r,g,b
			assert(r+g+b <= 255)
		yield colors



class AreasAudio(looping_show.LoopingShow):

    name = "Areas Audio"

    def __init__(self, geometry):
        looping_show.LoopingShow.__init__(self, geometry)

        self.background = RGB(0,0,0)
        self.mode = 3

        self.round = 0
        self.duration = 0.05

	self.audio = audio.Audio()

        if self.mode == 0:
            self._list = self.geometry.HOR_RINGS_MIDDLE_OUT
        elif self.mode in (1, 2, 3):
            self._list = self.geometry.RINGS_AROUND

        self.num_leds = len(self._list)   
        self.colors = normalize_colors(generate_colors(self.num_leds))

        self.clear()

    def clear(self):
        c = hsv_to_rgb(self.background.hsv)
        for i in range(self.geometry.numLEDs):
            self.geometry.set_pixel(i, c)

        self.geometry.draw()

    def custom_range_value_changed(self, range):
        self.mode = self.cm.ranges[range]
        print "setting mode to", self.mode

    def update_at_progress(self, progress, new_loop, loop_instance):

        if not new_loop:
            return

        loud = 0.0
        pitch = 0.0
        yy = []
        if self.mode !=3:
            (loud, pitch, yy) = self.audio.audio_input()
            if pitch == 0.0 or pitch == 1.1: return

        #pitch = yy[3]

        #print pitch, loud
        to_light = int(pitch * len(self._list))

        # horizontal rings up / down based on pitch, color intensity = loud, color = pitch
        if self.mode == 0:
	    loud = min(loud * 20, 1.0)
            for i in range(0, len(self._list)):

                #print to_light, len(self._list[i])
		#to_light = min(to_light, len(self._list[i]))
                if i <= to_light:
                    #c = color.hsv(pitch,loud*5%1.0,loud)
                    c = color.hsv(pitch,1.0,loud)
                else:
                    c = self.background.hsv

                # all around
                for k in self._list[i]:
                    self.geometry.set_pixel(k, c)


        # each ring is a differnt frequency and they are all lit up the ame amount based on the overall pitch
        elif self.mode ==1:
            #self.round += 1
            #self.round %= max(self.geometry.row)
            if pitch == 1.0: to_light = len(self._list) / 2
            #print pitch, to_light
            for round, l in enumerate(self._list):
                #print yy[round % len(l)]
                #print len (yy), len(l)
                for i, k in enumerate(l):
                    if i <= to_light/2:
                        # TBD: PICK a color from a decent palette!!
                        # Use tween?
                        if len(l)<len(yy): index = round % len(l)
                        else: index = round % len(yy)
                        #c = color.hsv(abs(yy[index]) / 1.1, 1.0, loud)
                        c = color.hsv(abs(yy[index]) / 1.1, 1.0, min(loud*30, 1.0))
                    else:
                        c = (0,0,0)
                    self.geometry.set_pixel(k, c)

        # each ring is a different frequency and length is dependent on the extent of that frequency
        elif self.mode == 2:

            # TBD: Maybe have some kind of a correction matrix for yy
            # basically correction = [0.5, 0.4, 0.5]
            # then yy = yy - correction 
            # code, see mapping in model

            if pitch == 1.0: pitch = 0.5

            for round, l in enumerate(self._list):
                to_light = (abs(yy[round % len(yy)]) / 2.5) * len(self._list)
                # print "r", round, round % len(yy), yy[round % len(yy)]
                for i, k in enumerate(l):
                    if i <= to_light:
                        c = color.rainbow_(1, round, loud)
                    else:
                        c = (0,0,0)
                    self.geometry.set_pixel(k, c)

        elif self.mode == 3:

            # from: http://yager.io/LEDStrip/LED.html
            # TBD - there is noise - turn off music and it flickers a lot
            notes = self.audio.lava_audio(self.num_leds)
            colors = multiply_colors(self.colors, notes, scalar = 255.0)
	    colors = cap_colors(colors, cap = 255.0)
            # returns 32 (r,g,b) values)
            color_list = colors.next()

            for round, l in enumerate(self._list):
                for i, k in enumerate(l):
                    c = color_list[round % self.num_leds]
                    self.geometry.set_pixel(k, c)

        self.geometry.draw()

__shows__ = [
              (AreasAudio.name, AreasAudio)
            ]

