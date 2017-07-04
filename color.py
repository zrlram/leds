import colorsys
import tween
import color2

# red, orange, yellow, green, blue, indigo, violet
rainbow_simple =  [(255,0,0), (255,127,0), (255,255,0), (0,255,0),
            (0,0,255), (75,0,130), (139,0,255)]

rainbow = [ (127, 0, 255), (97, 46, 253), (67, 92, 250), (37, 134, 245), 
            (7, 171, 237), (142, 253, 171), (172, 245, 153), (202, 228, 134), 
            (232, 203, 113), (255, 171, 92), (255, 134, 69), (255, 92, 46), 
            (255, 46, 23), (255, 0, 0)]

'''
def create_rainbow():

    # create a rainbow color table
    m = cm.ScalarMappable(cmap=cm.rainbow)
    # 18 colors
    rainbow_scale = [x for x in m.to_rgba(np.linspace(0,1,18))]
    for el in rainbow_scale:
        print(tuple([int(x*255) for x in el][:3]))
        rainbow.append(tuple([int(x*255) for x in el][:3]))
'''

def hsv(h,s,v):

    assert (h<=1.0) and (h>=0)
    assert (s<=1.0) and (s>=0)
    assert (v<=1.0) and (v>=0)
    #print h,s,v,colorsys.hsv_to_rgb(h,s,v)[:3], tuple([int(x*255) for x in colorsys.hsv_to_rgb(h,s,v)][:3])
    #import traceback
    #traceback.print_exc()
    return tuple([int(x*255) for x in colorsys.hsv_to_rgb(h,s,v)][:3])

def rgb_to_hsv(rgb):
    "convert a rgb[0-255] tuple to hsv[0.0-1.0]"
    f = float(255)
    return colorsys.rgb_to_hsv(rgb[0]/f, rgb[1]/f, rgb[2]/f)

def get_H(rgb):
    f = float(255)
    return colorsys.rgb_to_hsv(rgb[0]/f, rgb[1]/f, rgb[2]/f)[0]

def set_H(rgb, factor=1.0, absolute=None):
    f = float(255)
    _hsv = colorsys.rgb_to_hsv(rgb[0]/f, rgb[1]/f, rgb[2]/f)

    if factor!=1.0:
        h = _hsv[0] * factor
    elif absolute:
        h = absolute
    else:
        h = _hsv[0]
        
    return hsv(h, _hsv[1], _hsv[2])

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

def rainbow_(progress, step, brightness, numSlices=18):
    # step chooses which color of the rainbow
    # progress is the blender parameter from 0 to 1

    v_range = tween.easeInQuad(0.1, 0.98, (brightness + 1.0)/2.0)
    per_slice = v_range / numSlices
            
    hue = progress - (step % numSlices * per_slice) 
    while hue > 1.0:
        hue -= 1.0
    while hue < 0.0:
        hue += 1.0

    hsv = (hue, 1.0, 1.0)

    rgbTuple = color2.hsvRYB_to_rgb(hsv)
    return (int(rgbTuple[0]), int(rgbTuple[1]), int(rgbTuple[2]))

