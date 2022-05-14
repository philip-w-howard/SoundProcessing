# routines for reading/writing sound files 
# and for recording from a sound device

import numpy as np
import soundfile as sf
import sounddevice as sd

##################################################
def rec_audio(duration, device, channels, sample_rate):
#    print("Recording audio")
    data = sd.rec(int(duration*sample_rate), samplerate=sample_rate,
                  channels=channels, device=device)

    sd.wait()

#    print("Done recording")
    
    return data;

##################################################
def write_file(filename, data, samplerate):
    print("Writing sound file: " + filename)
    sf.write(filename, data, samplerate, 'PCM_16')
    print("Done")

##################################################
def write_channels(filename, left, right, samplerate):
    print("Writing sound file: " + filename)
    clip_len = len(left)
    sample = np.empty( (clip_len, 2) )
    sample[:,0] = left
    sample[:,1] = right
    sf.write(filename, sample, samplerate, 'PCM_16')
    print("Done")

##################################################
def read_file(filename):
    data, samplerate = sf.read(filename)
    return data, samplerate

##################################################
def get_interesting(sound, threshold, border):
    max = sound.max()
    threshold *= max

    #find the bounds
    index = 0
    start = -1
    end = sound.shape[0]
    
    for value in sound:
        if value.max() >= threshold:
            if start == -1:
                start = index
            end = index
        index += 1

    start -= border
    if start < 0:
        start = 0
    end += border
    if end > sound.shape[0]:
        end = sound.shape[0] - 1

    return sound[start:end]

##################################################
def add_noise(sound, loudness):
    noise = np.random.normal(0, loudness, sound.shape)
    return sound + noise
