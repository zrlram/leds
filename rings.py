import model
import time
import simplexnoise
from math import sin, cos, sqrt

speed = 0.002
wspeed = 0.01
scale = 0.1
ringScale = 3
wanderSpeed = 0.0005
dx = 0
dz = 0
dw = 0
hue = 0
saturation = 0
spacing = 0
centerx = 0
centery = 0
centerz = 0

def fractalNoise(x,y,z,w):
    # 4D fractal noise (fractional brownian motion)

    r = 0
    amp = 0.5
    for ocate in range(4): 
        r += (simplexnoise.raw_noise_4d(x, y, z, w) + 1) * amp
        amp /= 2
        x *= 2
        y *= 2
        z *= 2
        w *= 2

    return r

def noise(x, spin=0.01):
    return simplexnoise.raw_noise_2d(x, x * spin) * 0.5 + 0.5

def shader(p):
    x = p['point'][0]
    y = p['point'][1]
    z = p['point'][2]

    distx = x - centerx
    disty = y - centery
    distz = z - centerz

    dist = sqrt(distx**2 + disty**2 + distz**2)
    pulse = (sin(dz + dist * spacing) - 0.3) * 0.3
  
    n = fractalNoise(
        x * scale + dx + pulse,
        y * scale,
        z * scale + dz,
        dw
    ) - 0.95

    m = fractalNoise(
        x * scale + dx,
        y * scale,
        z * scale + dz,
        dw  + 10.0
    ) - 0.75

    # TBD: abs(n) is my doing, was just n
    return model.hsv(
        hue + 0.2 * m,
        saturation,
        min(max(pow(3.0 * abs(n), 1.5), 0), 0.9)
    )

def rings():

    now = time.time()       # millis

    angle = sin(now * 0.001)
    global hue
    hue = now * 1.0

    global saturation, spacing
    saturation = min(max(pow(1.15 * noise(now * 0.000122), 2.5), 0), 1)
    spacing = noise(now * 0.000124) * ringScale

    # Rotate movement in the XZ plane
    global dx, dz, dw
    dx += cos(angle) * speed
    dz += sin(angle) * speed

    # Random wander along the W axis
    dw += (noise(now * 0.00002) - 0.5) * wspeed

    global centerx, centery, centerz
    centerx = (noise(now * wanderSpeed, 0.9) - 0.5) * 1.25
    centery = (noise(now * wanderSpeed, 1.4) - 0.5) * 1.25
    centerz = (noise(now * wanderSpeed, 1.7) - 0.5) * 1.25

    mod = model.load_model('../openpixelcontrol/layouts/my_sphere.json')
    model.map_pixels(shader, mod)

iterations = 1000
for i in range(iterations):
    rings()
    time.sleep(0.1)
