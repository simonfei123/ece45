# ECE45 Final Project -- Audio Synthesizer
## Getting Started
`pip install` the all the packagages imported in `main.py`
run `python main.py`

## Basic Usage
- Select the initial waveform to be generated
- Add in any number of filters, amplitude modulations, amplitude envelopes, and pitch envelopes after the initial waveform
- Play the resulting sound by clicking Play

## Waveform Generator Types
- Sine Wave
- Square Wave
    - duty : the duty cycle of the square wave
- Sawtooth
    - width : the percent width of the rising edge relative to the cycle

## Filter Types
- lowpass
    - high : the high-cut point of the filter
- highpass
    - low : the low-cut point of the filter
- bandpass
    - high : the high-cut point of the filter
    - low : the low-cut point of the filter
- bandstop
    - high : the high-pass point of the filter
    - low : the low-pass point of the filter
- band amplification/dampening
    - high : the high-cut point of the filter
    - low : the low-cut point of the filter
    - multiplier : multiplier for the band-selected region

## TODOs:
- GUI elements for the adding additional filters, amplitude modulations, etc
- Visualizing gain of filters
- Allow custom input audio
- ...