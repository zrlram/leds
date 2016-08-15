import random

class Stars(object):

    name = "Stars"
    ok_for_random = False
    is_show = True
    show_type = "overlay"

    def __init__(self, geometry):

        self.frame_time = .10
        self.geometry = geometry
        

    def set_controls_model(self, cm):
        self.cm = cm

    def next_frame(self):   
        while (True):

            # Setup our colors
            colors = []

            #colors.append((255, 255,  27))
            #colors.append(( 64, 255, 218))
            #colors.append((245, 218,  64))
            #colors.append((255, 140, 140))

            # Default colors
            colors.append((0,0,255))
            colors.append((0,40,255))
            colors.append((255,255,255))
            colors.append((0,150,100))

            sparkle_thresh = 0.03 + ((self.cm.brightness + 1.0) / 2.0) * 0.010
            #sparkle_thresh = 0.005            

            for i in range(self.geometry.get_nof_pixels()):
                # Does it sparkle or not
                if random.random() < sparkle_thresh:
                    # Sparkle it
                    # It gets one of 4 inensities
                    clr = colors[random.randrange(len(colors))]
                    self.geometry.set_pixel(i, clr)

                #else:
                    # No sparkle. Set to background
                    # self.geometry.set_pixel(i, (20,0,0))

            self.geometry.draw()

            yield self.frame_time

__shows__ = [
              (Stars.name, Stars)
            ]

