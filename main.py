import tkinter
import sounddevice as sd
import time
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import numpy as np

def plot(y):
    # https://www.geeksforgeeks.org/how-to-embed-matplotlib-charts-in-tkinter-gui/
  
    # the figure that will contain the plot
    fig = Figure(figsize = (5, 5),
                 dpi = 100)
  
    # adding the subplot
    plot1 = fig.add_subplot(111)
  
    # plotting the graph
    plot1.plot(y)
  
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

def gen_sine():
    # Samples per second
    sps = 44100

    # Frequency / pitch
    freq_hz = 440.0

    # Duration
    duration_s = 5.0

    # Attenuation so the sound is reasonable
    atten = 0.3

    # NumpPy magic to calculate the waveform
    each_sample_number = np.arange(duration_s * sps)
    waveform = np.sin(2 * np.pi * each_sample_number * freq_hz / sps)
    waveform_quiet = waveform * atten
    return waveform_quiet

def play(waveform):
    # Samples per second
    sps = 44100

    sd.play(waveform, sps)


window = tkinter.Tk()
waveform = gen_sine()

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