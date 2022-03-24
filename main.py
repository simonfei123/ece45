import tkinter
from turtle import width
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
        # filt_2_psd = np.fft.fft(filt_signal.real)
        # plot(np.abs(orig_psd),freqs)
        # plot(np.abs(filt_psd),freqs)
        # plot(np.abs(filt_2_psd),freqs)
        return filt_signal.real

def amplitude_modulation(orig_signal, new_freq):
    sps = 44100
    duration = len(orig_signal) / sps
    modulating_signal = wave_gen('sine', duration=duration, frequency=new_freq)
    modulating_signal *= orig_signal
    return modulating_signal

def amplitude_envelope(orig_signal):
    analytic_signal = signal.hilbert(orig_signal)
    amplitude_envelope = np.abs(analytic_signal)
    return amplitude_envelope

def pitch_envelope(orig_signal):
    fs = 44100
    analytic_signal = signal.hilbert(orig_signal)
    instantaneous_phase = np.unwrap(np.angle(analytic_signal))
    instantaneous_frequency = (np.diff(instantaneous_phase) / (2.0*np.pi) * fs)
    return instantaneous_frequency

def play(wave,frequency,duration,amplitude,duty,width):
    # Samples per second
    sps = 44100
    if wave==1:
        waveform = wave_gen('sine', duration=duration, frequency=frequency, amplitude=amplitude)
    if wave==2:
        waveform = wave_gen('square', duration=duration, frequency=frequency, amplitude=amplitude, duty=duty)
    if wave==3:
        waveform = wave_gen('sawtooth', duration=duration, frequency=frequency, amplitude=amplitude, width=width)
    # waveform = filt(waveform,'bandamp')
    sd.play(waveform, sps)

def new_options(window):
    lb = tkinter.Listbox(window)
    lb.insert(0, 'filter')
    lb.insert(1, 'amplitude modulation')
    lb.insert(2, 'amplitude envelope')
    lb.insert(3, 'pitch envelope')
    lb.grid()
    button = tkinter.Button(master = window, 
                     height = 2, 
                     width = 10,
                     text = "Add")
    button.grid()
    def item_selected(event):
        selected_indices = lb.curselection()
        print(selected_indices)
    lb.bind('<<ListboxSelect>>', item_selected)



window = tkinter.Tk()
menu = tkinter.Menu(window)
window.config(menu=menu)
filemenu = tkinter.Menu(menu)
menu.add_cascade(label='File', menu=filemenu)
filemenu.add_command(label='New', command=lambda:new_options(window))
filemenu.add_command(label='Exit', command=window.quit)

wave = tkinter.IntVar()
wave.set(1)
tkinter.Radiobutton(window, text='Sinewave', variable=wave, value=1).grid(row=0,column=0)
tkinter.Radiobutton(window, text='Squarewave', variable=wave, value=2).grid(row=0,column=1)
tkinter.Radiobutton(window, text='Sawtooth', variable=wave, value=3).grid(row=0,column=2)

frequency = tkinter.IntVar()
frequency.set(440)
duration = tkinter.DoubleVar()
duration.set(5)
amplitude = tkinter.DoubleVar()
amplitude.set(0.3)
duty = tkinter.DoubleVar()
duty.set(0.5)
width = tkinter.DoubleVar()
width.set(1)
tkinter.Label(window, text='frequency: ').grid(row=1, column=0)
tkinter.Scale(window, from_=0, to=5000, variable=frequency, orient=tkinter.HORIZONTAL, length=300).grid(row=1, column=1, columnspan=3)
tkinter.Label(window, text='duration: ').grid(row=2, column=0)
tkinter.Scale(window, from_=0, to=50, resolution=0.1, variable=duration, orient=tkinter.HORIZONTAL, length=300).grid(row=2, column=1, columnspan=3)
tkinter.Label(window, text='amplitude: ').grid(row=3, column=0)
tkinter.Scale(window, from_=0, to=1, resolution=0.01, variable=amplitude, orient=tkinter.HORIZONTAL, length=300).grid(row=3, column=1, columnspan=3)
tkinter.Label(window, text='duty: ').grid(row=4, column=0)
tkinter.Scale(window, from_=0, to=1, resolution=0.01, variable=duty, orient=tkinter.HORIZONTAL, length=300).grid(row=4, column=1, columnspan=3)
tkinter.Label(window, text='width: ').grid(row=5, column=0)
tkinter.Scale(window, from_=0, to=1, resolution=0.01, variable=width, orient=tkinter.HORIZONTAL, length=300).grid(row=5, column=1, columnspan=3)



# button that displays the plot
play_button = tkinter.Button(master = window, 
                     command = lambda:play(wave.get(),frequency.get(),duration.get(),amplitude.get(),duty.get(),width.get()),
                     height = 2, 
                     width = 10,
                     text = "Play")
  
# place the button 
# in main window
# play_button.pack(side=tkinter.BOTTOM)
play_button.grid(row=0,column=3)
# plot(waveform)

window.mainloop()