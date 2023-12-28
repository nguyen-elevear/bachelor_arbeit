import soundfile as sf
import pyloudnorm as pyln 


def modify_loudness(files, norm_loudness):
    for type, filepath in files.items():
        data, sample_rate = sf.read(filepath)

        # measure the loudness first 
        meter = pyln.Meter(sample_rate) # create BS.1770 meter
        loudness = meter.integrated_loudness(data)
        print(loudness)
        #loudness normalize audio to -40 dB LUFS
        loudness_normalized_audio = pyln.normalize.loudness(data, loudness, norm_loudness)

        # Writing a WAV file
        sf.write(f'/Users/nptlinh/Desktop/BA-Code/test_set/{type}_{norm_loudness}.wav', loudness_normalized_audio, sample_rate)



files = {
    "airplane": "/Users/nptlinh/Desktop/BA-Code/test_set/Inside_Aircraft2_binaural ( 0.00-30.00 s).wav",
    "train": "/Users/nptlinh/Desktop/BA-Code/test_set/Inside_Train_Noise1_binaural ( 0.00-30.00 s).wav",
    "car": "/Users/nptlinh/Desktop/BA-Code/test_set/Midsize_Car1_100Kmh_binaural ( 0.00-30.00 s).wav",
    "nature_creek": "/Users/nptlinh/Desktop/BA-Code/test_set/Nature2_Creek_binaural ( 0.00-30.00 s).wav",
    "public": "/Users/nptlinh/Desktop/BA-Code/test_set/Pub_Noise_Binaural_V2.wav",
    "open_field": "/Users/nptlinh/Desktop/BA-Code/test_set/Nature3_Open_Field_Noise_binaural ( 0.00-30.00 s).wav",
    "sine": "/Users/nptlinh/Desktop/BA-Code/test_set/sine.wav"
}

modify_loudness(files, -32)