# use sounddevice to record from the microphone into a numpy array

import sounddevice as sd
import numpy as np
import wave
import soundfile as sf

def rec_audio(duration, device, channels, sample_rate):
    print("Recording audio")
    data = sd.rec(int(duration*sample_rate), samplerate=sample_rate,
                  channels=channels, device=device)

    sd.wait()

    print("Done recording")
    
    return data;

def write_file(filename, data, samplerate):
    print("Writing sound file: " + filename)
    sf.write(filename, data, samplerate, 'PCM_16')
    print("Done")

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
    
if __name__ == '__main__':
    sample_rate = 44100      # samples / sec
    sample_rate = 16000
    duration = 2.0
    device = 15
    channels = 6
    
    speed_of_sound = 34300.0 # cm/sec
    distance = 5.0           # cm separation between microphones
    max_separation = sample_rate / speed_of_sound * distance # samples between microphones
    samples_sep = int(max_separation) + 1
    
    print("samples of separation: ", max_separation)
    
    data = rec_audio(duration, device, channels, sample_rate)
    write_file('raw.wav', data, sample_rate)

    trimmed = get_interesting(data, 0.4, samples_sep)
    write_file('trimmed.wav', trimmed, sample_rate)
    
