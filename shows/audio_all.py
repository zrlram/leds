import looping_show
import color as col
import audio

class AudioAll(looping_show.LoopingShow):

    ok_for_random = False

    name = "Audio Ball"

    def __init__(self, geometry):
        looping_show.LoopingShow.__init__(self, geometry)

	self.audio = audio.Audio()
        self.duration = 1

    def update_at_progress(self, progress, new_loop, loop_instance):

	(loud, pitch, yy) = self.audio.audio_input()
        #print int(loud * 100)  
        #print "p",pitch
        color = col.hsv(pitch,1.0,loud)

        # draw
        for i in range(self.geometry.get_nof_pixels()):
            self.geometry.set_pixel(i, color)

        self.geometry.draw()


__shows__ = [
              (AudioAll.name, AudioAll)
            ]

