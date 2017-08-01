import opc
import json
import copy
import operator
from color import set_brightness_multiplier
import multiprocessing 
from ctypes import c_ubyte
from math import ceil, sin, cos


class Model(object):

    def __init__(self, model_file):
        self.model = None
        self.load_model(model_file)    # sets self.model

        self.shaders = []            # list of shader functions to be called
        self._brightness = 1.0

        self.numLEDs = len(self.model)
        print "LEDs: ", self.numLEDs
        self.client = opc.Client('192.168.56.150:7890')
        #self.client = opc.Client('localhost:7890')
        self.pixels = multiprocessing.Array((c_ubyte * 3), self.numLEDs, lock=False)

        self.position = {}  # coords -> position
        for i, entry in enumerate(self.model):
            self.position[str(entry)] = i

    def set_pixel(self, pos, color):
        self.pixels[pos] = color

    def get_pixel(self, pos):
        return self.pixels[pos] 

    def draw(self):
        self.client.put_pixels(self.pixels)

    def register_shader(self,shader):
        self.shaders.append(shader)

    def reset_shaders(self):
        self.shaders = []

    def get_shaders(self):
        return self.shaders
    
    def worker(self, start, end):
	if end>len(self.pixels)-1: end=len(self.pixels)-1
	if len(self.shaders)<1: return
        for i in range(start, end):
            led = self.model[i]          # x,y,z of pixel
            if led == [0.0,0.0,0.0]: continue  # speed up for missing pixels
            # can rotate here!
            #led['point'][0] = 
            #led['point'][1] = 
            #led['point'][0] = led['point'][1]*sin(0.3)+led['point'][0]*cos(0.3)
            self.pixels[i] = self.shaders[0](led)
            for shader in self.shaders[1:]:
                values = shader(led) 
                self.pixels[i] = tuple(map(operator.add, self.pixels[i], values))
            if self._brightness != 1.0:
                # adjust brightness
                self.pixels[i] = set_brightness_multiplier(self.pixels[i], self._brightness)

    def map_pixels(self):
        # set all pixels by mapping each element of the "model" through 
        # "fn" and setting the corresponding pixel value. The "fn" function 
        # returns a tuple of three 8-bit RGB values.
    
        # print "active shaders: %s" % self.shaders

        nprocs = 2
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

        self.draw()

    def get_brightness(self):
        return self._brightness 

    def set_brightness(self, val):
        self._brightness = val

    def clear(self):
        black = (0,0,0)

        for i, led in enumerate(self.pixels):
            self.pixels[i] = black
       
        # draw()        # -- this will be called implicitly

    def load_model(self, filename):

        with open(filename) as data_file:    
            data = json.load(data_file)
        print "Loading model: %s" % filename

        self.model = [x['point'] for x in data]          # making it a bit easier

    def set_pixel(self, pixel, color):
        # safety
        if pixel >= self.numLEDs:
            return
        if self._brightness != 1.0:
            self.pixels[pixel] = set_brightness_multiplier(color, self._brightness)
        else:
            self.pixels[pixel] = color
    
    def get_nof_pixels(self):
        return len(self.pixels)
