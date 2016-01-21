class WebController(object):

    def __init__(self, cm):
        self.cm = cm


    def set_color(self, c_ix, data):
        self.cm.set_color_rgb(c_ix, data)


