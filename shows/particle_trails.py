import model
import time
from color import hsv
from math import sin, cos

class ParticleTrails(object):

    name = "Particle Trails"

    def __init__(self, geometry):
        self.geometry=geometry
        self.speed = 0.05
        # register a shader here
        model.register_shader(model.shader)

    def next_frame(self):

        while True:
            now = 0.003 * time.time() * 1000     # millis
            numParticles = 20
            particles = []

            for i in range(numParticles):
                s = float(i) / numParticles

                radius = 0.2 + 1.5 * s
                theta = now + 0.04 * i
                x = radius * cos(theta)
                y = radius * sin(theta + 10.0 * sin(theta * 0.15))
                hue = now * 0.01 + s * 0.2

                particles.append({
                    "point": [x, 0, y],
                    'intensity': 0.2 * s,
                    'falloff': 60,
                    'color': hsv(hue, 0.5, 0.8)
                })

            model.map_particles(particles, self.geometry)
        
            yield self.speed


__shows__ = [
              (ParticleTrails.name, ParticleTrails)
            ]


