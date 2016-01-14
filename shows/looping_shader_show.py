import looping_show

class LoopingShaderShow(looping_show.LoopingShow):

    name = "Looping Shader Show"                 # show should overwrite this

    shader_registered = False

    def __init__(self, geometry, shader):
        looping_show.LoopingShow.__init__(self, geometry)
        self.shader = shader

    def next_frame(self):

        if not self.shader_registered:
            print "Registering Shader: %s" % self.shader
            self.geometry.register_shader(self.shader)
            self.shader_registered = True

        while True:
            value = looping_show.LoopingShow.next_frame(self).next()
            self.geometry.map_pixels()
            yield value

