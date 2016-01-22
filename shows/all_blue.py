class Blue():

    name = "Testing - All Blue"
    ok_for_random = False

    red = (255, 0, 0)
    black = (0, 0, 0)

    # dict with name of control and type - the name defines the change method
    # implement the function :  control_<name>_changed(self, __parameters__)
    controls = { 'color': 'color' }

    def __init__(self, geometry):
        self.color = Blue.black
        self.geometry = geometry

    def set_controls_model(self, cm):
        self.cm = cm

    def control_color_changed(self, c_ix):
        if c_ix == 0:       # use the primarty color
            self.color = self.cm.chosen_colors[c_ix]

    def next_frame(self):

        while True:
            for i in range(self.geometry.get_nof_pixels()):
                self.geometry.set_pixel(i, self.color)

            self.geometry.set_pixel(0, Blue.red)
            self.geometry.draw()

            yield 2 

__shows__ = [
              (Blue.name, Blue)
            ]

