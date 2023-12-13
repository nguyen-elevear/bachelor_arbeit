import soundfile as sf
import pyloudnorm as pyln 

data, sample_rate = sf.read("/Users/nptlinh/Desktop/BA-Code/test_set/sine_white.wav")

# measure the loudness first 
meter = pyln.Meter(sample_rate) # create BS.1770 meter
loudness = meter.integrated_loudness(data)
print(loudness)
# loudness normalize audio to -12 dB LUFS
loudness_normalized_audio = pyln.normalize.loudness(data, loudness, -23.0)

# Writing a WAV file
sf.write('/Users/nptlinh/Desktop/BA-Code/test_set/sine.wav', loudness_normalized_audio, sample_rate)