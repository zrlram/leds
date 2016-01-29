import time
from color import hsv
from math import sin, cos
import looping_shader_show

class ParticleTrails(looping_shader_show.LoopingShaderShow):

    name = "Particle Trails"

    def __init__(self, geometry):
        looping_shader_show.LoopingShaderShow.__init__(self, geometry, self.shader)
        self._particles = None

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
            r += particle['color'][1] * intensity
            r += particle['color'][2] * intensity

        return (int(r),int(g),int(b))


    def update_at_progress(self, progress, new_loop, loop_instance):

        now = 0.003 * time.time() * 1000     # millis
        numParticles = 20
        particles = []

        for i in range(numParticles):
            s = float(i) / numParticles

            radius = 0.2 + 1.5 * s
            theta = now + 0.04 * i
            x = radius * cos(theta)
            y = radius * sin(theta + 10.0 * sin(theta * 0.15))
            hue = (now * 0.01 + s * 0.2) % 1 

            particles.append({
                "point": [x, 0, y],
                'intensity': 0.2 * s,
                'falloff': 60,
                'color': hsv(hue, 0.5, 0.8)
            })

        self._particles = particles
        

__shows__ = [
              (ParticleTrails.name, ParticleTrails)
            ]


