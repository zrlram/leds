import looping_show
import color as col
import pyaudio
import numpy
import analyse

class Audio(looping_show.LoopingShow):

    name = "Audio Ball"
    audio_maxLoud = 1
    audio_minLoud = -40
    audio_maxPitch = 120        # ???
    audio_minPitch = 0          # ???

    def __init__(self, geometry):
        looping_show.LoopingShow.__init__(self, geometry)

        self.geometry = geometry

        # init audio
        p = pyaudio.PyAudio()

        self.stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=44100,
                        input_device_index = 2,
                        input=True,
                        frames_per_buffer=1024)


        # stream.stop_stream()
        # stream.close()
        # p.terminate()

    def set_controls_model(self, cm):
        self.cm = cm

    def update_at_progress(self, progress, new_loop, loop_instance):

        # read audio value 
	pitch = None
	loud = None
        while not pitch or not loud:
            try:
                data = self.stream.read(256)
		samps = numpy.fromstring(data, dtype=numpy.int16)
		loud = analyse.loudness(samps)
		pitch = analyse.musical_detect_pitch(samps)
            except:
                pass


        # normalize   

        # http://stats.stackexchange.com/questions/70801/how-to-normalize-data-to-0-1-range
        # min' and max' are new range
        # newvalue= (max'-min')/(max-min)*(value-min)+min')
        loud = (loud - Audio.audio_minLoud) / (Audio.audio_maxLoud - Audio.audio_minLoud) 
        pitch = (pitch - Audio.audio_minPitch) / (Audio.audio_maxPitch - Audio.audio_minPitch) 

	print loud, pitch

        # color
        color = col.hsv(pitch,loud,loud)

        # draw
        for i in range(self.geometry.get_nof_pixels()):
            self.geometry.set_pixel(i, color)

        self.geometry.draw()


__shows__ = [
              (Audio.name, Audio)
            ]

