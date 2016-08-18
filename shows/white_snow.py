#
# White Snow
#
# Show draws vertically failing trails
# 
# Snow color is always white
# Background is black
# 

from random import randint
from model import VERT_RINGS

import looping_show
from color import morph_color
            
class WhiteSnow(looping_show.LoopingShow):

    is_show = True

    name = "White Snow"

    def __init__(self, geometry):

        looping_show.LoopingShow.__init__(self, geometry)

        self.paths = [] # List that holds paths objects
        self.geometry = geometry
        self.max_paths = 6
        self.decay = 1.0 / 3
        self.background  = (0,0,0) # Always Black
        self.foreground = (255,255,255)  # Always White
        
        self.duration = 1
        self.last_update = 0
        
    """
    def set_param(self, name, val):
        # name will be 'colorR', 'colorG', 'colorB'
        rgb255 = int(val * 0xff)
        if name == 'colorR':
            self.max_paths = (rgb255 * 8 / 255) + 2
        elif name == 'colorG':
            self.decay = 1.0 / ((rgb255 * 4) + 1)  
    """
                    
    def update_at_progress(self, progress, new_loop, loop_instance):
            
        if len(self.paths) < self.max_paths:
            over = randint(0, len(VERT_RINGS) - 1)
            new_path = Path(self.geometry, VERT_RINGS[over], self.decay)
            self.paths.append(new_path)
        
        # Set background cells

        #self.sheep.set_all_cells(self.background)                       
        
        # Draw paths
            
        if (new_loop): self.last_update = 0
        if (progress - self.last_update) > 0.05:
            for p in self.paths:
                p.draw_path(self.foreground, self.background)
                p.move_path()
            self.last_update = progress        

        for p in self.paths:
            if p.path_alive() == False:
                self.paths.remove(p)

                

        self.geometry.draw()
    
class Fader(object):
    def __init__(self, model, pixel_number, decay):
        self.geometry = model
        self.pixel = pixel_number
        self.decay = decay
        self.life = 1.0
    
    def draw_fader(self, fore_color, back_color):
        adj_color = morph_color(back_color, fore_color, self.life)
        self.geometry.set_pixel(self.pixel, adj_color)
    
    def age_fader(self):
        self.life -= self.decay
        if self.life > 0:
            return True # Still alive
        else:
            return False    # Life less than zero -> Kill

class Path(object):
    def __init__(self, geometry, over, decay):
        self.geometry = geometry
        self.faders = []    # List that holds fader objects
        self.down = 0                # how far down did we fall already
        self.decay = decay
        self.over = over                # where the snow will fall
        self.length = len(self.over)   # how many rows there are total
        
        new_fader = Fader(self.geometry, self.over[0], self.decay)
        self.faders.append(new_fader)

    
    def draw_path(self, foreground, background):
        for f in self.faders:
            f.draw_fader(foreground, background)
        for f in self.faders:
            if f.age_fader() == False:
                self.faders.remove(f)
    
    def path_alive(self):
        if len(self.faders) > 0:
            return True
        else:
            return False
            
    def move_path(self):

        if self.down < (self.length - 1):
            self.down += 1
            new_fader = Fader(self.geometry, self.over[self.down], self.decay)
            self.faders.append(new_fader)

            
            
__shows__ = [
              (WhiteSnow.name, WhiteSnow)
            ]
