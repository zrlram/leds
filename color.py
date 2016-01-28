from math import floor
from matplotlib.pyplot import cm
import numpy as np
import colorsys

rainbow = []

def create_rainbow():

    # create a rainbow color table
    m = cm.ScalarMappable(cmap=cm.rainbow)
    # 18 colors
    rainbow_scale = [x for x in m.to_rgba(np.linspace(0,1,18))]
    for el in rainbow_scale:
        rainbow.append(tuple([int(x*256) for x in el][:3]))

def hsv(h,s,v):
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

def rgb_to_hsv(rgb):
    "convert a rgb[0-255] tuple to hsv[0.0-1.0]"
    f = float(255)
    return colorsys.rgb_to_hsv(rgb[0]/f, rgb[1]/f, rgb[2]/f)

def set_V(rgb, factor=1.0, absolute=None):
    f = float(255)
    _hsv = colorsys.rgb_to_hsv(rgb[0]/f, rgb[1]/f, rgb[2]/f)

    if factor!=1.0:
        v = _hsv[2] * factor
    elif absolute:
        v = absolute
    else:
        v = _hsv[2]
        
    return hsv(_hsv[0], _hsv[1], v)
    
def get_V(rgb):
    f = float(255)
    return colorsys.rgb_to_hsv(rgb[0]/f, rgb[1]/f, rgb[2]/f)[2]

def set_brightness_multiplier(rgb, factor):
    # multipies the brightness with factor and returns an rgb again
    f = float(255)
    _hsv = colorsys.rgb_to_hsv(rgb[0]/f, rgb[1]/f, rgb[2]/f)
    return hsv(_hsv[0], _hsv[1], _hsv[2] * factor)

def morph_color(color1, color2, fract):
    # Interpolates between colors. Fract = 1 is all color 2

    c1 = rgb_to_hsv(color1)
    c2 = rgb_to_hsv(color2)

    morph_h = c1[0] + ((c2[0] - c1[0]) * fract)
    morph_s = c1[1] + ((c2[1] - c1[1]) * fract)
    morph_v = c1[2] + ((c2[2] - c1[2]) * fract)

    return hsv(morph_h, morph_s, morph_v)

