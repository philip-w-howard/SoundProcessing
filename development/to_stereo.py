import numpy as np
import wave
import soundfile as sf
import os

if __name__ == '__main__':
    filename = input("source sound file: ")
    output_name = input("Output sound file: ")

    data, samplerate = sf.read(filename)

    stereo = []
    for sample in data:
        stereo.append([sample,sample])

    sf.write(output_name, stereo, samplerate, 'PCM_16')

