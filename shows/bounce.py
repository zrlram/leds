#
# White Bounce
#
# Show draws 3 balls that bounce horizontally
# 
# Background is black
#
# Balls are white
#
# 

from random import randint
from color2 import RGB, HSV, hsv_to_rgb
            
# Interpolates between colors. Fract = 1 is all color 2
def morph_color(color1, color2, fract):
        morph_h = color1.h + ((color2.h - color1.h) * fract)
        morph_s = color1.s + ((color2.s - color1.s) * fract)
        morph_v = color1.v + ((color2.v - color1.v) * fract)
        
        return HSV(morph_h, morph_s, morph_v)
        
class Fader(object):
        def __init__(self, geometry, cell, decay):
                self.geometry = geometry
                self.cell = cell
                self.decay = decay
                self.life = 1.0
        
        def draw_fader(self, fore_color, back_color):
                adj_color = morph_color(back_color, fore_color, self.life)
                adj_color = hsv_to_rgb(adj_color.hsv)

                self.geometry.set_pixel(self.cell, adj_color)
                #self.geometry.draw()
        
        def age_fader(self):
                self.life -= self.decay
                if self.life > 0:
                        return True     # Still alive
                else:
                        return False    # Life less than zero -> Kill

class Path(object):
        def __init__(self, geometry, trajectory, decay):
                self.geometry = geometry
                self.faders = []        # List that holds fader objects
                self.pos = 0    # Where along the sheep
                self.dir = 1    # 1 or -1 for left or right
                self.decay = decay
                self.trajectory = trajectory                            
        
        def set_decay(self, decay):
                self.decay = decay

        def draw_path(self, foreground, background):
                for f in self.faders:
                        f.draw_fader(foreground, background)
                for f in self.faders:
                        if f.age_fader() == False:
                                self.faders.remove(f)
        
        def move_path(self):
                self.pos += self.dir
                if self.pos <= 0 or self.pos >= len(self.trajectory) - 1:
                        self.dir *= -1  # Flip direction: bounce

                new_fader = Fader(self.geometry, self.trajectory[self.pos], self.decay)
                self.faders.append(new_fader)
                
                if randint(1,30) == 1:
                        self.decay = 1.0 / randint(2,8) # Change trail length
                
class WhiteBounce(object):

        name = "Bounce"

        def __init__(self, geometry):
                self.decay = 1.0 / 8
                self.geometry = geometry
                self.paths = [] # List that holds paths objects

                trajs = len(self.geometry.VERT_RINGS)
                self.trajectories = (self.geometry.VERT_RINGS[2], self.geometry.VERT_RINGS[int(trajs/4)],
                                     self.geometry.VERT_RINGS[int(3*trajs/4)], self.geometry.VERT_RINGS[trajs-2])
                self.background  = RGB(0,0,0) # Always Black
                self.foreground = RGB(255,255,255)      # White
                
                # Set up 3 balls on low, medium, and high levels
                
                num_of_bouncers = 8
                for i in range(num_of_bouncers):
                        new_path = Path(self.geometry, self.trajectories[i % len(self.trajectories)], self.decay)
                        self.paths.append(new_path)
                        
                self.speed = 0.1
                
        def set_param(self, name, val):
                # name will be 'colorR', 'colorG', 'colorB'
                rgb255 = int(val * 0xff)
                if name == 'colorR':
                        self.decay = 1.0 / (((rgb255 * 8) / 255) + 2) 
                        for p in self.paths:
                                p.set_decay(self.decay)
                                
        def next_frame(self):   
                                        
                while (True):
                        
                        # Set background cells
                        
                        c = hsv_to_rgb(self.background.hsv)
                        for i in range(self.geometry.get_nof_pixels()):
                            self.geometry.set_pixel(i, c)
                        
                        # Draw paths
                        for p in self.paths:
                                p.draw_path(self.foreground, self.background)
                                p.move_path()

                        self.geometry.draw()

                        h = (self.foreground.h + 0.1) %1
                        self.foreground = HSV(h,1.0,1.0)
                        
                        yield self.speed

__shows__ = [
              (WhiteBounce.name, WhiteBounce)
            ]
