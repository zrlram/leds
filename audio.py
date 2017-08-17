import pyaudio
import numpy as np
import time
import scipy
import struct
#import scipy.fftpack
from scipy.fftpack import fft,fftfreq

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

def fft_lava(audio_stream):
	def real_fft(im):
		im = np.abs(np.fft.fft(im))
		re = im[0:len(im)/2]
		re[1:] += im[len(im)/2 + 1:][::-1]
		return re
	for l, r in audio_stream:
		yield real_fft(l) + real_fft(r)

def scale_samples(fft_stream, numleds):
	for notes in fft_stream:
		yield notes[0:numleds]

def schur(array_stream, multipliers):
	for array in array_stream:
		yield array*multipliers

def rolling_scale_to_max(stream, falloff):
	avg_peak = 0.0
	for array in stream:
		peak = np.max(array)
		if peak > avg_peak:
			avg_peak = peak # Output never exceeds 1
		else:
			avg_peak *= falloff
			avg_peak += peak * (1-falloff)
		if avg_peak == 0:
			yield array
		else:
			yield array / avg_peak

def rolling_smooth(array_stream, falloff):
	smooth = array_stream.next()
	yield smooth
	for array in array_stream:
		smooth *= falloff
		smooth += array * (1 - falloff)
		yield smooth

def exaggerate(array_stream, exponent):
	for array in array_stream:
		yield array ** exponent

def add_white_noise(array_stream, amount):
	for array in array_stream:
		if sum(array) != 0:
			yield array + amount
		else:
			yield array

def human_hearing_multiplier(freq):
	points = {0:-10, 50:-8, 100:-4, 200:0, 500:2, 1000:0, \
				2000:2, 5000:4, 10000:-4, 15000:0, 20000:-4}
	freqs = sorted(points.keys())
	for i in range(len(freqs)-1):
		if freq >= freqs[i] and freq < freqs[i+1]:
			x1 = float(freqs[i])
			x2 = float(freqs[i+1])
			break
	y1, y2 = points[x1], points[x2]
	decibels = ((x2-freq)*y1 + (freq-x1)*y2)/(x2-x1)
	return 10.0**(decibels/10.0)

# Convert the audio data to numbers, num_samples at a time.
def read_audio(audio_stream, num_samples):
	while True:
		# Read all the input data. 
		samples = audio_stream.read(num_samples, exception_on_overflow=False)
		# Convert input data to numbers
		samples = np.fromstring(samples, dtype=np.int16).astype(np.float)
		samples_l = samples[::2]        # get every second element
		samples_r = samples[1::2]       # and the other ones
		yield (samples_l, samples_r)


class Audio():

    p = None
    stream = None

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
	try:
		Audio.stream = Audio.p.open(format=pyaudio.paInt16,
			channels=1,
			rate=SAMPLE_RATE,
			input_device_index = 2,
			input=True,
			output=False,
			frames_per_buffer=BUFFER_SIZE)
	except:
		self.clear()
		Audio.stream = Audio.p.open(format=pyaudio.paInt16,
			channels=1,
			rate=SAMPLE_RATE,
			input_device_index = 2,
			input=True,
			output=False,
			frames_per_buffer=BUFFER_SIZE)


    def clear(self):
        print "Audio clear"
        Audio.stream.stop_stream()
        Audio.stream.close()
	Audio.p.terminate()

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

    def lava_audio(self, num_leds = 32):

        # num_leds  -- number of buckets to squeece colors into
        buf_size = 512 # BUFFER_SIZE
	frequencies = [float(SAMPLE_RATE*i)/buf_size for i in range(num_leds)]
	human_ear_multipliers = np.array([human_hearing_multiplier(f) for f in frequencies])
        audio_stream = read_audio (Audio.stream, num_samples=512)
	notes = fft_lava(audio_stream)
	notes = scale_samples(notes, num_leds)
	notes = add_white_noise(notes, amount=8000)
	notes = schur(notes, human_ear_multipliers)
	notes = rolling_scale_to_max(notes, falloff=.98) # Range: 0-1
	notes = exaggerate(notes, exponent=2)
	notes = rolling_smooth(notes, falloff=.7)
        return notes        

    def audio_input(self):

        data = ""
        try:
            while Audio.stream.get_read_available<=BUFFER_SIZE:
                time.sleep(0.05)
            # reads stereo 
            buf = read_audio (Audio.stream, num_samples=BUFFER_SIZE)
            #buf = Audio.stream.read(BUFFER_SIZE, exception_on_overflow=False)
            #data = scipy.array(struct.unpack("%dh"%(BUFFER_SIZE),buf))
        except Exception as e:
            self.open_stream()
            #print "available", Audio.stream.get_read_available()

        # deal with the generator and the stereo input
        data = buf.next()[0].astype(int)

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
        scale = 25
        exponent = 7 
        new_levels = []
        for level in levels:
                level = abs(level)
	        level = max(min(level / scale, 1.0), 0.0)
                level = level**exponent 
                new_levels.append(level)
                #level = int(level * 255)
                #ser.write(chr(level))
                #if level == 1.0: level =0
        level = max ( new_levels ) 
  
        #return (brightness, hue/360.0)
        #return (brightness, hue/360.0,yy )
        return (rms, level, yy)

