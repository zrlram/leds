import time
from color import hsv
from math import sin, cos
import looping_shader_show
from collections import OrderedDict

class ParticleTrails(looping_shader_show.LoopingShaderShow):

    name = "Particle Trails"

    #controls = OrderedDict()
    #controls.update({ 'move': 'checkbox'})
    #controls.update({ 'Trail Length': [0.1, 1, 0.5, 0.01]})

    def __init__(self, geometry):
        looping_shader_show.LoopingShaderShow.__init__(self, geometry, self.shader)
        self._particles = []
        self.numParticles = 20

    def shader(self, p):
        r = 0
        g = 0
        b = 0

        if not self._particles:
            return

        for particle in self._particles:
            dx = (p['point'][0] - particle['point'][0]) or 0
            dy = (p['point'][1] - particle['point'][1]) or 0
            dz = (p['point'][2] - particle['point'][2]) or 0
            dist2 = dx**2 + dy**2 + dz**2

            intensity = particle['intensity'] / (1+particle['falloff'] * dist2)

            r += particle['color'][0] * intensity
            g += particle['color'][1] * intensity
            b += particle['color'][2] * intensity

        return (int(r),int(g),int(b))


    def update_at_progress(self, progress, new_loop, loop_instance):

        now = 0.002 * time.time() * 1000     # millis

        particles = []
        for i in range(self.numParticles):
            s = float(i) / self.numParticles

            radius = 0.2 + 1.5 * s
            theta = now + 0.04 * i
            x = radius * cos(theta)
            y = radius * sin(theta + 10.0 * sin(theta * 0.15))
            hue = (now * 0.01 + s * 0.2) % 1 

            particles.append({
                "point": [x, 0, y],
                'intensity': 0.2 * s,
                'falloff': 50,
                'color': hsv(hue, 0.8, 0.9)
            })

        self._particles = particles
        

__shows__ = [
              (ParticleTrails.name, ParticleTrails)
            ]


