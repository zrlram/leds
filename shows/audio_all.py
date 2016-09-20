import looping_show
import color as col
import audio

class AudioAll(looping_show.LoopingShow):

    ok_for_random = False

    name = "Audio Ball"
    #max -10.9559531292 84.0577667883
    #min -27.7098972444 40.331492511

    def __init__(self, geometry):
        looping_show.LoopingShow.__init__(self, geometry)

        self.geometry = geometry
	self.audio = audio.Audio()

    def set_controls_model(self, cm):
        self.cm = cm

    def update_at_progress(self, progress, new_loop, loop_instance):

	(loud, pitch) = self.audio.audio_input()
        color = col.hsv(pitch,pitch,loud)
        #color = col.hsv(0.5,1,loud)

        # draw
        for i in range(self.geometry.get_nof_pixels()):
            self.geometry.set_pixel(i, color)

        self.geometry.draw()


__shows__ = [
              (AudioAll.name, AudioAll)
            ]

