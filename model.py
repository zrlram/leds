import json
from connection import pixels, draw
import operator

class Model(object):

    def __init__(self, model_file):
        self.model = None
        self.load_model(model_file)

        self.shaders = []            # list of shader functions to be called

    def register_shader(self,shader):
        self.shaders.append(shader)

    def reset_shaders(self):
        self.shaders = []

    def map_pixels(self):
        # set all pixels by mapping each element of the "model" through 
        # "fn" and setting the corresponding pixel value. The "fn" function 
        # returns a tuple of three 8-bit RGB values.
    
        # print "active shaders: %s" % self.shaders
        
        for i, led in enumerate(self.model):
            # first one sets the base, others are 'add'-ed in
            pixels[i] = self.shaders[0](led)
            for shader in self.shaders[1:]:
                values = shader(led) 
                pixels[i] = tuple(map(operator.add, pixels[i], values))

        draw()

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
        pixels[pixel] = color


