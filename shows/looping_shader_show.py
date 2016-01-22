import looping_show

class LoopingShaderShow(looping_show.LoopingShow):

    name = "Looping Shader Show"                 # show should overwrite this

    def __init__(self, geometry, shader):
        looping_show.LoopingShow.__init__(self, geometry)
        self.shader = shader
        self.shader_registered = False

    def start(self):

        if not self.geometry.get_shaders():
            print "Registering Shader: %s" % self.shader
            self.geometry.register_shader(self.shader)
            self.shader_registered = True

    def next_frame(self):

        gen = looping_show.LoopingShow.next_frame(self)
        while True:
            value = gen.next()
            try:
                self.geometry.map_pixels()
            except IndexError:
                self.start()   # we might not have a shader registered!
                self.geometry.map_pixels()     # try again
                
            yield value

