from math import floor
from matplotlib.pyplot import cm
import numpy as np

rainbow = []

def create_rainbow():

    # create a rainbow color table
    m = cm.ScalarMappable(cmap=cm.rainbow)
    # 18 colors
    rainbow_scale = [x for x in m.to_rgba(np.linspace(0,1,18))]
    for el in rainbow_scale:
        rainbow.append(tuple([int(x*256) for x in el][:3]))

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

