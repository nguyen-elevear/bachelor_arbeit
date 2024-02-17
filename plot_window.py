import pyfar as pf
import numpy as np
signal = pf.Signal(np.ones(100), 44100)
for shape in ['symmetric', 'symmetric_zero', 'left', 'right']:
    signal_windowed = pf.dsp.time_window(
        signal, interval=[25,45], shape=shape)
    ax = pf.plot.time(signal_windowed, label=shape)
ax.legend(loc='right')