class WebController(object):

    def __init__(self, cm):
        self.cm = cm


    def set_color(self, c_ix, color):
        
        color = (int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)) 
        self.cm.set_color_rgb(c_ix, color)

    def set_speed(self, speed):
        self.cm.speed_change_rel(speed)

    def set_brightness(self, brigthness):
        self.cm.set_brightness(brigthness)

    def set_max_runtime(self, runtime):
        self.cm.set_max_time(runtime)

    # a show can have a range slider to select any variable
    def set_custom_range_value(self, range, value):
        self.cm.set_custom_range_value(range, value)

    def set_custom_checkbox_value(self, checkbox, value):
        self.cm.set_custom_checkbox_value(checkbox, value)

    def set_config(self, key, value):
        self.cm.set_config(key, value)
