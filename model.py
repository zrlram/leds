import json
from connection import pixels, draw
from math import floor
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
    register_shader(shader)
    map_pixels(model)

def load_model(filename):

    with open(filename) as data_file:    
        data = json.load(data_file)
    return data

def hsv(h,s,v,):
    # convert HSV colors to RGB
    # Normal hsv range is in [0,1], RGB is in [0,255]
    # Hue values will wrap

    h = (h % 1) *6
    if (h < 0): h+=6
    
    i = int(floor(h))
    f = h - i
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    r = int([v, q, p, p, t, v][i] * 255)
    g = int([t, v, v, q, p, p][i] * 255)
    b = int([p, p, t, v, v, q][i] * 255)

    # cut to 0-255 range
    r = max(0, min(r, 255))
    g = max(0, min(g, 255))
    b = max(0, min(b, 255))
    
    return (r, g, b)