import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter
from scipy.io import wavfile
from scipy.fft import fft



def butter_lowpass(audio, cutoff, fs, order=1):
    num, den = butter(order, cutoff, btype="low", analog=False, output="ba", fs=fs)
    audio_filtered = lfilter(num, den, audio)
    return audio_filtered



def butter_highpass(audio, cutoff, fs, order=1):
    num, den = butter(order, cutoff, btype="high", analog=False, output="ba", fs=fs)
    audio_filtered = lfilter(num, den, audio)
    return audio_filtered



def plot_audio_time_domain(audio, sample_rate):

    channels = audio.shape[1] if audio.ndim > 1 else 1
    time = np.linspace(0., len(audio) / sample_rate, len(audio))

    plt.figure(figsize=(15, 5))
    for i in range(channels):
        plt.subplot(2, 1, i+1)
        plt.plot(time, audio[:, i])
        plt.title('Channel %d' % (i+1))
        plt.xlabel('Time [s]')
        plt.ylabel('Amplitude')
    plt.tight_layout()
    plt.show()



def plot_audio_freq_domain(audio, sample_rate):
    channels = audio.shape[1] if audio.ndim > 1 else 1
    plt.figure(figsize=(15, 5))
    for i in range(channels):
        channel_data = audio[:, i]
        
        #FFT
        yf = fft(channel_data)
        xf = np.linspace(0, sample_rate//2, len(channel_data)//2)
        
        idx_range = np.where(xf<=10000)
        xf_zoom = xf[idx_range]
        yf_zoom = yf[idx_range]
        plt.subplot(2, 1, i+1)
        plt.plot(xf_zoom, 2.0/len(channel_data) * np.abs(yf_zoom))
        
        plt.title('Frequency Domain of Channel %d' % (i+1))
        plt.xlabel('Frequency [Hz]')
        plt.ylabel('Amplitude')
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    sample_rate, audio = wavfile.read(r"C:\Users\LinhNguyen\Desktop\BA_Code\580527__tosha73__big-city-noise-15072021.wav")
    y_low = butter_lowpass(audio, 200, sample_rate, 5)
    plot_audio_time_domain(audio, sample_rate)
    plot_audio_time_domain(y_low, sample_rate)
    plot_audio_freq_domain(audio, sample_rate)
    plot_audio_freq_domain(y_low, sample_rate)



