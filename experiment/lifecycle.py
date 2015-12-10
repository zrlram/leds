import model
import time
from random import random
from math import sin, cos, pi

mod = model.load_model('../openpixelcontrol/layouts/my_sphere.json')

totalLife = 50  # how long to keep the dots there
numParticles = 10
zoom = 0.998
intensity = -1.2

backgroundHue = random()

# Start out with just a background
particles = [] 

def newBloomTimer():
    return random() * 100               # how often and fast new things show

def randomPoint():
    #A random point somewhere relevant on our model
    return [
        4 * (random() - 0.5),
        1 * (random() - 0.5),
        4 * (random() - 0.5)
    ]

# Create other nascent particles that 'bloom' once a timer runs out
for i in range(numParticles):
    particles.append({
        'point': (0, 0, 0),
        'intensity': 0,
        'falloff': 20,          # how wide the glow / faded area
        'color': model.hsv(random(), 0.6, 0.8),
        'bloomTimer': newBloomTimer()
    })

def lifecycle():

    # Update background color
    global backgroundHue
    backgroundHue = (backgroundHue + 0.0002) % 1

    particles[0]['color'] = model.hsv(backgroundHue, 0.8, 0.2)

    # Update particle state
    for i, p in enumerate(particles):

        if (p.get('bloomTimer')>0):
            # Particle is blooming
            particles[i]['bloomTimer'] -= 1
            if (p['bloomTimer'] <= 0):
                # Done blooming. Start life cycle
                particles[i]['lifeTimer'] = totalLife
                particles[i]['intensity'] = 1
                #particles[i]['falloff'] = 0
                particles[i]['point'] = randomPoint()
                particles[i]['bloomTimer'] = None

        if (p.get('lifeTimer')>0):
            # Particle is alive. Update intensity.
            # Particles go through a life cycle with positive and negative intensity
            particles[i]['intensity'] = intensity * sin(p['lifeTimer'] * 2 * pi / totalLife)

            # Collapse into the center
            particles[i]['point'][0] = p['point'][0] * zoom
            particles[i]['point'][1] = p['point'][1] * zoom
            particles[i]['point'][2] = p['point'][2] * zoom

            particles[i]['lifeTimer'] -= 1

            if (p['lifeTimer'] <= 0):
                # Particle is dead. Go back to blooming.
                particles[i]['bloomTimer'] = newBloomTimer()
                particles[i]['lifeTimer'] = None

    model.map_particles(particles, mod)

iterations = 10000
for i in range(iterations):
    lifecycle()
    time.sleep(0.05)
