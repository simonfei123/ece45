import tkinter
import sounddevice as sd
import time
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import numpy as np
from scipy import signal

def plot(y, x = None):
    # https://www.geeksforgeeks.org/how-to-embed-matplotlib-charts-in-tkinter-gui/
  
    # the figure that will contain the plot
    fig = Figure(figsize = (5, 5),
                 dpi = 100)
  
    # adding the subplot
    plot1 = fig.add_subplot(111)
  
    # plotting the graph
    if(x is None):
        plot1.plot(y)
    else:
        plot1.plot(x,y)
  
    # creating the Tkinter canvas
    # containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig,
                               master = window)  
    canvas.draw()
  
    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().pack()
  
    # creating the Matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas,
                                   window)
    toolbar.update()
  
    # placing the toolbar on the Tkinter window
    canvas.get_tk_widget().pack()

def wave_gen(wave_type='sine', duration=5.0, amplitude = 0.3, frequency = 440, phase = 0, duty = 0.5, width=1):
    # Samples per second
    sps = 44100
    if wave_type=='sine':
        each_sample_number = np.arange(duration * sps)
        waveform = np.sin(2 * np.pi * (each_sample_number - 2*np.pi*phase) * frequency / sps)
        waveform = waveform * amplitude
        return waveform
    if wave_type=='square':
        each_sample_number = np.arange(duration * sps)
        waveform = signal.square(2 * np.pi * (each_sample_number - 2*np.pi*phase) * frequency / sps, duty=duty)
        waveform = waveform * amplitude
        return waveform
    if wave_type=='sawtooth':
        each_sample_number = np.arange(duration * sps)
        waveform = signal.sawtooth(2 * np.pi * (each_sample_number - 2*np.pi*phase) * frequency / sps, width=width)
        waveform = waveform * amplitude
        return waveform

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = signal.butter(order, [low, high], btype='bandpass')
    return b, a

def butter_bandstop(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = signal.butter(order, [low, high], btype='bandstop')
    return b, a

def butter_highpass(lowcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    b, a = signal.butter(order, low, btype='highpass')
    return b, a

def butter_lowpass(highcut, fs, order=5):
    nyq = 0.5 * fs
    high = highcut / nyq
    b, a = signal.butter(order, high, btype='lowpass')
    return b, a

def filt(orig_signal, filt_type='bandpass', low = 10, high = 9000, order=5, multiplier = 4):
    # Samples per second
    sps = 44100
    if filt_type=='bandpass':
        b, a = butter_bandpass(low, high, sps, order=order)
        y = signal.lfilter(b, a, orig_signal)
        return y
    if filt_type=='bandstop':
        b, a = butter_bandstop(low, high, sps, order=order)
        y = signal.lfilter(b, a, orig_signal)
        return y
    if filt_type=='highpass':
        b, a = butter_highpass(low, sps, order=order)
        y = signal.lfilter(b, a, orig_signal)
        return y
    if filt_type=='lowpass':
        b, a = butter_lowpass(high, sps, order=order)
        y = signal.lfilter(b, a, orig_signal)
        return y
    if filt_type=='bandamp':
        orig_psd = np.fft.fft(orig_signal)
        filt_psd = orig_psd.copy()
        n_freqs = len(orig_psd)
        count_freqs = np.arange(n_freqs)
        T = n_freqs/sps
        freqs = count_freqs/T
        for i, freq in enumerate(freqs):
            if np.abs(freq) >= low and np.abs(freq) <= high:
                filt_psd[i] = filt_psd[i] * multiplier
        filt_signal = np.fft.ifft(filt_psd)
        filt_2_psd = np.fft.fft(filt_signal.real)
        # plot(np.abs(orig_psd),freqs)
        # plot(np.abs(filt_psd),freqs)
        # plot(np.abs(filt_2_psd),freqs)
        return filt_signal.real


def play(waveform):
    # Samples per second
    sps = 44100

    sd.play(waveform, sps)


window = tkinter.Tk()
waveform = wave_gen('sine')
waveform = filt(waveform,'bandamp')

# button that displays the plot
plot_button = tkinter.Button(master = window, 
                     command = lambda:play(waveform),
                     height = 2, 
                     width = 10,
                     text = "Play")
  
# place the button 
# in main window
plot_button.pack()
plot(waveform)

window.mainloop()