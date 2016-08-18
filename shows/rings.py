import time
import simplexnoise
from math import sin, cos, sqrt
from color import hsv
import looping_shader_show
from collections import OrderedDict

class Rings(looping_shader_show.LoopingShaderShow):

    name = "Rings"
    ok_for_random = False

    #controls = OrderedDict()
    #controls.update({'scale': [0,1,0.1,0.1]})
    #controls.update({'ringScale': [0,5,2,0.25]})

    def __init__(self, geometry):
        looping_shader_show.LoopingShaderShow.__init__(self, geometry, 
            self.shader)
        #self.scale = 0.1
        self.scale = 0.02
        #self.ringScale = 3.0
        self.ringScale = 1.0
        self.speed = 0.002
        self.wspeed = 0.01
        self.wanderSpeed = 0.00005
        self.dx = 0
        self.dz = 0
        self.dw = 0
        self.hue = 0
        self.saturation = 0
        self.spacing = 0
        self.centerx = 0
        self.centery = 0
        self.centerz = 0

    def custom_range_value_changed(self, range):
        if range==0:
            self.scale = self.cm.ranges[range]
        if range==1:
            self.ringScale = self.cm.ranges[range]

    @staticmethod
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

    @staticmethod
    def noise(x, spin=0.01):
        return simplexnoise.raw_noise_2d(x, x * spin) * 0.5 + 0.5

    def shader(self, p):
        x = p['point'][0]
        y = p['point'][1]
        #z = p['point'][2] 
        z = p['point'][2] + 1

        distx = x - self.centerx
        disty = y - self.centery
        distz = z - self.centerz

        dist = sqrt(distx**2 + disty**2 + distz**2)
        pulse = (sin(self.dz + dist * self.spacing) - 0.3) * 0.3
      
        n = Rings.fractalNoise(
            x * self.scale + self.dx + pulse,
            y * self.scale,
            z * self.scale + self.dz,
            self.dw
        ) - 0.95

        m = Rings.fractalNoise(
            x * self.scale + self.dx,
            y * self.scale,
            z * self.scale + self.dz,
            self.dw  + 10.0
        ) - 0.75

        # TBD: abs(n) is my doing, was just n
        return hsv(
            (self.hue + 0.2 * m) %1,
            self.saturation,
            min(max(pow(3.0 * abs(n), 1.5), 0), 0.9)
        )

    def update_at_progress(self, progress, new_loop, loop_instance):

        now = time.time() * 1000      # millis
        #now = 1471552007.07 * 1000

        angle = sin(now * 0.001)
        self.hue = now * 1.0

        self.saturation = min(max(pow(1.15 * Rings.noise(now * 0.000122), 2.5), 0), 1)
        self.spacing = Rings.noise(now * 0.000124) * self.ringScale

        # Rotate movement in the XZ plane
        self.dx += cos(angle) * self.speed
        self.dz += sin(angle) * self.speed

        # Random wander along the W axis
        self.dw += (Rings.noise(now * 0.00002) - 0.5) * self.wspeed

        self.centerx = (Rings.noise(now * self.wanderSpeed, 0.9) - 0.5) * 1.25
        self.centery = (Rings.noise(now * self.wanderSpeed, 1.4) - 0.5) * 1.25
        self.centerz = (Rings.noise(now * self.wanderSpeed, 1.7) - 0.5) * 1.25


__shows__ = [
              (Rings.name, Rings)
            ]

