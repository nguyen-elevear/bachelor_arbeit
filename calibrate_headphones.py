import pyfar as pf


headphone_output = pf.io.read_audio("output.wav")
headphone_input = pf.io.read_audio("input.wav")

hptf = pf.dsp.deconvolve(headphone_output, headphone_input, (20, 20000))

