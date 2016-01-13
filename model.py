import json
from connection import pixels, draw
import operator

shaders = []            # list of shader functions to be called

def register_shader(shader):
    shaders.append(shader)

def reset_shaders():
    global shaders
    shaders = []

def map_pixels(model):
    # set all pixels by mapping each element of the "model" through 
    # "fn" and setting the corresponding pixel value. The "fn" function 
    # returns a tuple of three 8-bit RGB values.
    
    for i, led in enumerate(model):
        # first one sets the base, others are 'add'-ed in
        pixels[i] = shaders[0](led)
        for shader in shaders[1:]:
            values = shader(led) 
            pixels[i] = tuple(map(operator.add, pixels[i], values))

    draw()

_particles = None

def shader(p):
    r = 0
    g = 0
    b = 0

    for particle in _particles:
        dx = (p['point'][0] - particle['point'][0]) or 0
        dy = (p['point'][1] - particle['point'][1]) or 0
        dz = (p['point'][2] - particle['point'][2]) or 0
        dist2 = dx**2 + dy**2 + dz**2

        intensity = particle['intensity'] / (1+particle['falloff'] * dist2)

        r += particle['color'][0] * intensity
        r += particle['color'][1] * intensity
        r += particle['color'][2] * intensity

    return (int(r),int(g),int(b))

def map_particles(particles, model):
    global _particles
    _particles = particles
    # do this in the init() of the show: register_shader(shader)
    map_pixels(model)

def load_model(filename):

    with open(filename) as data_file:    
        data = json.load(data_file)
    print "Loading model: %s" % filename
    return data

