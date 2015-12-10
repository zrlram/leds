import model
import time
from math import sin, cos

mod = model.load_model('../openpixelcontrol/layouts/my_sphere.json')

def trails():

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
            'color': model.hsv(hue, 0.5, 0.8)
        })

    model.map_particles(particles, mod)

iterations = 10000
for i in range(iterations):
    trails()
    #time.sleep(0.01)
