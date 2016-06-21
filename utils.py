from connection import numLEDs, height, row
from math import pi

def get_angles(position):

    negative = False
    if position >= sum(row):     # numLeds/2 is not half the sphere!
        position = position - sum(row)
        negative = True

    up = 0
    over = 0
    remainder = 0
    for go_up in range(0, height):
        remainder += row[go_up]
        if remainder > position:
            up = go_up 
            over = position - (remainder - row[go_up])
            break

    phi = ((pi/2) / height) * up
    theta = ( 2*pi / row[up] ) * over
    if negative:
        phi = - phi - ( pi/2 / height )

    # print "phi, theta, up, over", phi, theta, up, over

    return (phi, theta)

def get_position(up, over):
    if up == 0: up = 1

    row_index = abs(up) -1

    if (over < 0): over = row[row_index] + over
    if (over > row[row_index]): over = row[row_index]
    if up > height: up = height
    
    ups = 0
    for a in range(row_index):
        ups = ups + row[a]
    position = ups + over

    # lower half:
    if (up<0): position = position + sum(row) 
    if (position >= numLEDs): 
        print "exception", up, over, position
        raise Exception
        position = numLEDs-1

    #print position, up, over
    return position 


def pixel(theta, phi):
    # LEDs are wired from equator up (40 -> 38 -> ... -> 4)

    # do some boundary checking on the angles
    #
    # theta:  0, 2pi -- over
    # phi: -pi/2, pi/2 -- up
    # phi = 0 is strange because we don't have an equator
    #         we could convention that to light up up=+1
    #
   
    up = int( round( phi / (pi/2) * (height) ) )    # -pi/2 --> pi/2 
        # up == 0: equator! (which does not exist) up == height: top - the one with 0 LEDs
    if up == 0: up = 1

    row_index = abs(up) - 1
    over = int( round( (row[row_index] * theta) / (2*pi) ) )
    # in some cases, we get over the boundary because of rounding
    # e.g., theta = 6.14, row[row_index]=20

    return get_position(up, over)

def pixel_faded(theta, phi, color):

    #print "theta:", theta, "phi:", phi

    # take care of negative phi:
    negative = False
    if phi<0: 
        negative = True
        phi = abs(phi)

    up = phi / (pi/2) * height     # -pi/2 --> pi/2 
    bottom = int(floor(up))
    top = int(ceil(up))
    if phi==0:
        bottom = -1
        top = 1

    # work on top row first
    row_index = abs(top) - 1
    if row_index<0: row_index=0
    over = (row[row_index] * theta) / (2*pi)
    # floating point imprecisions are sucky
    left = ceil(float("{0:.4f}".format(over)))
    right = floor(float("{0:.4f}".format(over)))
    if left >= row[row_index]: 
        #print over, up, "harakiri"
        left = row[row_index]-1
        return

    max_dist_over = 2*pi / row[0]
    max_dist_up = pi/2 / height

    # top right LED
    #print up, row[row_index], row_index
    dist_over = abs(right*2*pi/row[row_index] - theta) / max_dist_over
    dist_up = (top*pi/2/height - phi) / max_dist_up
    dist = sqrt(dist_over**2 + dist_up**2)
    if phi==0:
        dist = 0.5
    col = rgb_intensity(color, 1-dist)

    #print "TOP RIGHT", "up", up, "over", over
    #print "dist_over:", dist_over, "dist_up", dist_up, "dist", dist
    #print "row[row_index]:", row[row_index]
    #print "color" , color
    if negative: top = - top
    pixels[get_position(top, int(right))] = col

    # top left LED
    dist_over = abs(left*2*pi/row[row_index] - theta) / max_dist_over
    dist = sqrt(dist_over**2 + dist_up**2)
    if phi==0:
        dist = 0.5
    col = rgb_intensity(color, 1-dist)
    #print color, 1-dist

    #print "TOP LEFT", "up", up, "over", over
    #print "dist_over:", dist_over, "dist_up", dist_up, "dist", dist
    #print "color" , color
    pixels[get_position(top, int(left))] = col

    # work on bottom 
    row_index = abs(bottom) - 1
    if row_index<0: row_index=0
    over = (row[row_index] * theta) / (2*pi)
    # floating point imprecisions are sucky
    left = ceil(float("{0:.4f}".format(over)))
    right = floor(float("{0:.4f}".format(over)))
    if left >= row[row_index]: 
        #print over, up, "harakiri"
        left = row[row_index]-1

    # bottom right LED
    #print "B", up, row[row_index], row_index
    dist_over = abs(right*2*pi/row[row_index] - theta) / max_dist_over
    dist_up = (bottom*pi/2/height - phi) / max_dist_up
    dist = sqrt(dist_over**2 + dist_up**2)
    if phi==0:
        dist = 0.5
    col = rgb_intensity(color, 1-dist)

    #print "BOT RIGHT", "up", up, "over", over
    #print "dist_over:", dist_over, "dist_up", dist_up, "dist", dist
    #print "color" , color
    if negative: bottom = - bottom
    pixels[get_position(bottom, int(right))] = col

    # top left LED
    dist_over = abs(left*2*pi/row[row_index] - theta) / max_dist_over
    dist = sqrt(dist_over**2 + dist_up**2)
    if phi==0:
        dist = 0.5
    col = rgb_intensity(color, 1-dist)

    #print "BOT LEFT", "up", up, "over", over
    #print "dist_over:", dist_over, "dist_up", dist_up, "dist", dist
    #print "color" , color
    pixels[get_position(bottom, int(left))] = col


