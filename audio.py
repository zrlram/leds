import pyaudio
import numpy as np
import math
import time
import scipy
import struct
from matplotlib.mlab import find
import scipy.fftpack
from scipy import pi, signal
from scipy.fftpack import fft,rfft,rfftfreq,fftfreq

SAMPLE_RATE = 44100
BUFFER_SIZE = 2**11     

MIN_HUE = 200   # Aqua
MAX_HUE = 0     # Red

def limit(val, vmin, vmax):
    """
    Clip values that fall outside vmin & vmax
    """
    if val < vmin: return vmin
    if val > vmax: return vmax
    return val

def mapval(val, minin, maxin, minout, maxout):
    """
    Linear value mapping between in and out
    """
    norm = (val-minin)/(maxin-minin)
    return norm*(maxout-minout) + minout
    
def thresh(val, threshold):
    """
    A bit hard to describe, but this will return 0 
    when val is below the threshold, and will
    linearly map val to anything higher than threshold.
    The effect being that above the threshold, louder
    signals will have more of an effect.
    """
    val -= threshold
    if val < 0: val = 0
    val *= (1.0/threshold)
    return val

def get_fft(data):
    """
    Run the sample through a FFT, and normalize
    """
    FFT = fft(data)
    freqs = fftfreq(BUFFER_SIZE*2, 1.0/SAMPLE_RATE)
    #y = 20*scipy.log10(abs(FFT))/ 100

    y = abs(FFT[0:len(FFT)/2])/1000
    y = scipy.log(y) - 2
    return (freqs,y)
    
class Audio():

    p = None

    # With ideas from https://github.com/jorticus/audiovis/blob/master/audiovis.py
    # Loudness detect:
    CHANNEL = 6     # frequency channel of the FFT to use (see console output to decide)
    GAIN = 1.5       # audio gain (multiplier)
    THRESHOLD = 0.15 # audio trigger threshold)
    ATTACK = 0.004  # amount of rowdz increase with loudness
    DECAY = 0.003   # amount of rowdz decay
    MODULATION = 0.0        # amount of loudness flickering modulation
    MIN_BRIGHTNESS = 0.5    # minimum brightness

    def __init__(self):

        # init audio

        # sometimes input_device_index is 2?
        Audio.p = pyaudio.PyAudio()
        self.open_stream()
        self.noisiness = 0       # Noisiness level
        self.max_bright = 1

    def open_stream(self):
        self.stream = Audio.p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=SAMPLE_RATE,
                        #input_device_index = 2,
                        input=True,
                        output=False,
                        frames_per_buffer=BUFFER_SIZE)

    def clear(self):
        #print "clear"
        self.stream.stop_stream()
        self.stream.close()

    def calculate_levels(self, data, chunk, samplerate):
        # Use FFT to calculate volume for each frequency
        global MAX

        import numpy
        # Convert raw sound data to Numpy array
        #fmt = "%dH"%(len(data)/2)
        #data2 = struct.unpack(fmt, data)
        #data2 = numpy.array(data2, dtype='h')
        data2 = data

        # Apply FFT
        fourier = numpy.fft.fft(data2)
        ffty = numpy.abs(fourier[0:len(fourier)/2])/1000
        ffty1=ffty[:len(ffty)/2]
        ffty2=ffty[len(ffty)/2::]+2
        ffty2=ffty2[::-1]
        ffty=ffty1+ffty2
        ffty=numpy.log(ffty)-2
        
        fourier = list(ffty)[4:-4]
        fourier = fourier[:len(fourier)/2]
        
        size = len(fourier)

        # Add up for 6 lights
        levels = [sum(fourier[i:(i+size/6)]) for i in xrange(0, size, size/6)][:6]
        #print levels
        return levels


    def audio_input(self):
        # read audio value 
        #foo = self.stream.get_read_available()

        data = ""
        try:
            while self.stream.get_read_available<=BUFFER_SIZE:
                time.sleep(0.05)
            buf = self.stream.read(BUFFER_SIZE, exception_on_overflow=False)
            data = scipy.array(struct.unpack("%dh"%(BUFFER_SIZE),buf))
        except Exception as e:
            self.open_stream()
            #print "available", self.stream.get_read_available()
            #pass


        
        # Generate FFT
        freqs,y = get_fft(data)

        # Normalize
        y = y / 5

        # Average into chunks of N
        N = 25
        yy = [scipy.average(y[n:n+N]) for n in range(0, len(y), N)]
        yy = yy[:len(yy)/2] # Discard half of the samples, as they are mirrored


        # Loudness detection
        loudness = thresh(yy[Audio.CHANNEL] * Audio.GAIN, Audio.THRESHOLD)

        # Noisiness meter
        self.noisiness -= Audio.DECAY
        self.noisiness += loudness * Audio.ATTACK
        self.noisiness = limit(self.noisiness, 0.0, 1.0)

        # Brightness modulation
        modulation = Audio.MODULATION * limit(self.noisiness, 0.0, 1.0)
        brightness = limit(Audio.MIN_BRIGHTNESS + (loudness * modulation), 0.0, 1.0)

        # Hue modulation (power relationship)
        mapping = (10 ** limit(self.noisiness, 0.0, 1.0)) / 10.0
        mapping = mapping * 1.1 - 0.11
        hue = mapval(mapping, 0.0, 1.0, MIN_HUE, MAX_HUE)
        
        peak=np.average(np.abs(data))*2
        #bars="#"*int(50*peak/2**16)
        #print("%05d %s"%(peak,bars))
        #print "peak", peak
        hue = mapval(peak, 0, 22000, 0, 360) 
        #print hue

        import audioop
        rms = audioop.rms(data, 2) 
        rms = rms / 14400.0
        rms = rms * 3
        if rms > 1.0: rms = 1.0

        # Do FFT
        levels = self.calculate_levels(data, BUFFER_SIZE , SAMPLE_RATE)

        # Make it look better and send to serial
        scale = 100
        exponent = 7
        for level in levels:
                level = max(min(level / scale, 1.0), 0.0)
                level = level**exponent 
                #level = int(level * 255)
                #ser.write(chr(level))
                #if level == 1.0: level =0

        #return (brightness, hue/360.0)
        #return (brightness, hue/360.0,yy )
        return (rms, level, yy)

