import looping_show
import color as col

class Blue(looping_show.LoopingShow):

    name = "Testing - All Blue"

    red = (255, 0, 0)
    blue = (50, 50, 255)

    # dict with name of control and type - the name defines the change method
    # implement the function :  control_<name>_changed(self, __parameters__)
    controls = { 'color': 'color' , 'rainbow': 'checkbox'}

    def __init__(self, geometry):
        looping_show.LoopingShow.__init__(self, geometry)

        self.color = Blue.blue
        self.geometry = geometry
        self.rainbow = 1

        self.duration = 4

    def set_controls_model(self, cm):
        self.cm = cm

    def control_color_changed(self, c_ix):
        if c_ix == 0:       # use the primarty color
            self.color = self.cm.chosen_colors[c_ix]

    def custom_checkbox_value_changed(self, checkbox):
        self.rainbow = self.cm.checkbox[checkbox]

    def update_at_progress(self, progress, new_loop, loop_instance):

        color = self.color
        if self.rainbow:
            color = col.rainbow[int(progress*len(col.rainbow))]
        for i in range(self.geometry.get_nof_pixels()):
            self.geometry.set_pixel(i, color)

        self.geometry.set_pixel(0, Blue.red)
        self.geometry.draw()


__shows__ = [
              (Blue.name, Blue)
            ]

