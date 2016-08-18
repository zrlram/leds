import json
import copy
from connection import pixels, draw, row, numLEDs
import operator
from color import set_brightness_multiplier
import multiprocessing 
from math import ceil, sin, cos

HALF_POINT = sum(row) - 1

HOR_RINGS_TOP_DOWN = []
# top
count = 0
for h in range(len(row)-1, -1, -1):
    r = []
    for element in range(HALF_POINT-count,HALF_POINT-count-row[h],-1):
        r.append(element)
    HOR_RINGS_TOP_DOWN.append(r)
    count += row[h]
# bottom
for h in range(0, len(row)-1):
    r = []
    for element in range(count,count+row[h]):
        r.append(element)
    HOR_RINGS_TOP_DOWN.append(r)
    count += row[h]

HOR_RINGS_MIDDLE_OUT = []
count = 0
for h in range(0, len(row)):
    r = []
    for element in range(count,count+row[h]):
        r.append(element)
    # bottom
    if h < 7:
        for element in range(HALF_POINT+count+1,HALF_POINT+count+1+row[h]):
            r.append(element)
    HOR_RINGS_MIDDLE_OUT.append(r)
    count += row[h]

offsets = []
offsets.append([1,1,1,1,1,1,0,0]) # 1
offsets.append([1,1,1,1,0,0,1,1]) # 2
offsets.append([1,1,1,0,1,1,0,0]) # 3
offsets.append([1,1,1,1,1,1,1,0]) # 4
offsets.append([1,1,1,1,1,0,0,0]) # 5
offsets.append([1,1,0,1,0,1,1,1]) # 6
offsets.append([1,1,1,1,1,0,0,0]) # 7
offsets.append([1,1,1,1,1,1,1,0]) # 8
offsets.append([1,1,1,0,1,1,0,0]) # 9
offsets.append([1,1,1,1,0,0,1,1]) # 10
offsets.append([1,1,1,1,1,1,0,0]) # 1
#offsets.append([0,0,0,0,0,0,0,0]) # 0

VERT_RINGS = []
#row = [0, 44, 44, 40, 36, 32, 28, 20]
temp = []
temp.append(0)
for i,el in enumerate(row[:-1]):
    temp.append(temp[i]+row[i])
t = copy.copy(temp)
temp.reverse()
for y in t:   # bottom
    addition = min(y+(numLEDs+12)/2, 499)
    temp.append(addition)

VERT_RINGS.append(temp)   # first vert_line

for round in range(0,4):        # 0 to 4
    for x,el in enumerate(offsets):
        # sorry, please forgive me!
        el2 = copy.copy(el)
        el3 = copy.copy(el)
        el3.reverse()        # need to invert top part
        el3.extend(el2)    # add index to itself for top and bottom
        new_ring = VERT_RINGS[x+round*len(offsets)]

        new_vert = list(map(operator.add, el3, VERT_RINGS[x+round*len(offsets)]))

        VERT_RINGS.append(new_vert)

#print VERT_RINGS

class Model(object):

    def __init__(self, model_file):
        self.model = None
        self.load_model(model_file)

        self.shaders = []            # list of shader functions to be called
        self._brightness = 1.0

        self.numLEDs = numLEDs

    def register_shader(self,shader):
        self.shaders.append(shader)

    def reset_shaders(self):
        self.shaders = []

    def get_shaders(self):
        return self.shaders
    
    def worker(self, start, end):
	if end>len(pixels)-1: end=len(pixels)-1
	if len(self.shaders)<1: return
        for i in range(start, end):
            led = self.model[i]
            # can rotate here!
            #led['point'][0] = 
            #led['point'][1] = 
            #led['point'][0] = led['point'][1]*sin(0.3)+led['point'][0]*cos(0.3)
            pixels[i] = self.shaders[0](led)
            for shader in self.shaders[1:]:
                values = shader(led) 
                pixels[i] = tuple(map(operator.add, pixels[i], values))
            if self._brightness != 1.0:
                # adjust brightness
                pixels[i] = set_brightness_multiplier(pixels[i], self._brightness)

    def map_pixels(self):
        # set all pixels by mapping each element of the "model" through 
        # "fn" and setting the corresponding pixel value. The "fn" function 
        # returns a tuple of three 8-bit RGB values.
    
        # print "active shaders: %s" % self.shaders

        nprocs = 8
        chunksize = int(ceil(len(self.model) / float(nprocs)))

        # multiple_results = [pool.apply_async(os.getpid, ()) for i in range(4)]
        # print [res.get(timeout=1) for res in multiple_results]

        procs = []
        for i in range(nprocs):
            p = multiprocessing.Process(
                target=self.worker,
                args=(chunksize * i,chunksize * (i + 1)))
            procs.append(p)
            p.start()

        draw()

    def set_brightness(self, val):
        self._brightness = val

    def clear(self):
        black = (0,0,0)

        for i, led in enumerate(pixels):
            pixels[i] = black
       
        # draw()        # -- this will be called implicitly

    def load_model(self, filename):

        with open(filename) as data_file:    
            data = json.load(data_file)
        print "Loading model: %s" % filename

        self.model = data

    def set_pixel(self, pixel, color):
        # safety
        if pixel >= numLEDs:
            return
        if self._brightness != 1.0:
            pixels[pixel] = set_brightness_multiplier(color, self._brightness)
        else:
            pixels[pixel] = color
    
    def draw(self):
        draw()      

    def get_nof_pixels(self):
        return len(pixels)
