import looping_show
import color as col
import pyaudio
import numpy as np
import analyse
import time
import math
from matplotlib.mlab import find
import matplotlib.pyplot as plt

class Audio(looping_show.LoopingShow):

    name = "Audio Ball"
    #max -10.9559531292 84.0577667883
    #min -27.7098972444 40.331492511
    audio_maxLoud = -30
    audio_minLoud = -30
    audio_maxPitch = 6000
    audio_minPitch = 500

    def __init__(self, geometry):
        looping_show.LoopingShow.__init__(self, geometry)

        self.geometry = geometry

        # init audio
        p = pyaudio.PyAudio()

        # sometimes input_device_index is 2?
        self.stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=44100,
                        input_device_index = 2,
                        input=True,
                        frames_per_buffer=1024)


    def clear(self):
        print "clear"
        self.stream.stop_stream()
        self.stream.close()

    def set_controls_model(self, cm):
        self.cm = cm

    '''
        http://stackoverflow.com/questions/9082431/frequency-analysis-in-python
        Using zero-crossing in the time domain to look for the pitch. No FFT!
    '''
    def get_pitch(self, signal):
        crossing = [math.copysign(1.0, s) for s in signal]
        index = find(np.diff(crossing))
        return round(len(index) * 44100 / (2*np.prod(len(signal))))

    '''  
        http://dsp.stackexchange.com/questions/16438/why-fft-does-not-retrieve-original-amplitude-when-increasing-signal-length 
    '''
    def get_fft(self, y, fs):
        """ Get the FFT of a given signal and corresponding frequency bins.

        Parameters:
            y  - signal
            fs - sampling frequency
        Returns:
            (mag, freq) - tuple of spectrum magitude and corresponding frequencies
        """
        n  = len(y)      # Get the signal length
        dt = 1/float(fs) # Get time resolution

        fft_output = np.fft.rfft(y)     # Perform real fft
        rfreqs = np.fft.rfftfreq(n, dt) # Calculate frequency bins
        fft_mag = np.abs(fft_output)    # Take only magnitude of spectrum       - abs

        # Normalize the amplitude by number of bins and multiply by 2
        # because we removed second half of spectrum above the Nyqist frequency 
        # and energy must be preserved
        fft_mag = fft_mag * 2 / n           

        return np.array(fft_mag), np.array(rfreqs)

    def update_at_progress(self, progress, new_loop, loop_instance):

        # read audio value 
        #foo = self.stream.get_read_available()

        data = None
        while not data:
            try:
                while self.stream.get_read_available<1024:
                    time.sleep(0.05)
                data = self.stream.read(1024)
                samps = np.fromstring(data, dtype=np.int16)
                loud = analyse.loudness(samps)
                # This pitch sucks:
                # self.pitch = analyse.musical_detect_pitch(samps) or self.pitch
                pitch = self.get_pitch(samps)
            except Exception as e:
                #print e
                #print "available", self.stream.get_read_available()
                pass

        ''' TBD if we want more details, not just pitch and loud
        (mag, freq) = self.get_fft(samps, 44100)
        print freq, mag
        # next step is to take some frequencies and map them to RGB ... maybe visualize the output first. Woudl be nice to have X
        '''

        # print "pitch",pitch, "loud", loud

        if loud < Audio.audio_minLoud:
            Audio.audio_minLoud = loud
        if loud > Audio.audio_maxLoud:
            Audio.audio_maxLoud = loud
        #Audio.audio_minLoud = min(Audio.audio_minLoud, loud) 
        #Audio.audio_maxLoud = max(Audio.audio_maxLoud, loud)
        Audio.audio_minPitch = min(Audio.audio_minPitch, pitch) 
        Audio.audio_maxPitch = max(Audio.audio_maxPitch, pitch)

        #print "max",Audio.audio_maxLoud, Audio.audio_maxPitch
        #print "min",Audio.audio_minLoud, Audio.audio_minPitch

        #if Audio.audio_minLoud==Audio.audio_maxLoud:
        #    Audio.audio_minLoud+=0.01
        if Audio.audio_minPitch==Audio.audio_maxPitch:
            Audio.audio_minPitch+=0.01

        # normalize   

        # http://stats.stackexchange.com/questions/70801/how-to-normalize-data-to-0-1-range
        # min' and max' are new range
        # newvalue= (max'-min')/(max-min)*(value-min)+min') 
        loud = (loud - Audio.audio_minLoud) / (Audio.audio_maxLoud - Audio.audio_minLoud) 
        pitch = (pitch - Audio.audio_minPitch) / (Audio.audio_maxPitch - Audio.audio_minPitch) 

        loud = max(0,min(loud,1))

        # DEBUG: print "l",round(loud , 1), "p",round(pitch, 1), "minL:", Audio.audio_minLoud, Audio.audio_maxLoud

        # color
        color = col.hsv(pitch,pitch,loud)
        #color = col.hsv(0.5,1,loud)

        # draw
        for i in range(self.geometry.get_nof_pixels()):
            self.geometry.set_pixel(i, color)

        self.geometry.draw()


__shows__ = [
              (Audio.name, Audio)
            ]

