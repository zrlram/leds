from connection import pixels, draw

class Blue():

    name = "Testing - All Blue"
    ok_for_random = False

    def __init__(self, geometry):
        self.red = (255, 0, 0)

    def next_frame(self):

        for i,pixel in enumerate(pixels):
            pixels[i]= (55,55,200)

        pixels[0] = self.red
        draw()

        yield 2

__shows__ = [
              (Blue.name, Blue)
            ]

