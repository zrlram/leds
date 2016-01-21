class WebController(object):

    def __init__(self, cm):
        self.cm = cm


    def set_color(self, c_ix, color):
        self.cm.set_color_rgb(c_ix, color)

    def set_speed(self, speed):
        self.cm.speed_change_rel(speed)

    def set_brightness(self, brigthness):
        self.cm.set_brightness(brigthness)

    def set_max_runtime(self, runtime):
        self.cm.set_max_time(runtime)
