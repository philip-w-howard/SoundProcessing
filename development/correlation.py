# Correlation code
import numpy as np
import soundfile as sf
import sounddevice as sd

##################################################
def rec_audio(duration, device, channels, sample_rate):
    print("Recording audio")
    data = sd.rec(int(duration*sample_rate), samplerate=sample_rate,
                  channels=channels, device=device)

    sd.wait()

    print("Done recording")
    
    return data;

##################################################
def write_file(filename, data, samplerate):
    print("Writing sound file: " + filename)
    sf.write(filename, data, samplerate, 'PCM_16')
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
def correlate(left, right):
    avg_l = np.average(left);
    avg_r = np.average(right);

    diff_l = left - avg_l
    diff_r = right - avg_r;

    sum1 = np.sum( diff_l * diff_r)

    square_l = diff_l * diff_l
    square_r = diff_r * diff_r
    
    sum2 = np.sum(square_l)
    sum3 = np.sum(square_r)

    ccv = sum1/(np.sqrt(sum2) * np.sqrt(sum3))

    return ccv
    
##################################################
def correlate_least_squares(left, right):
    diff = left - right
    square = diff * diff   
    return np.sum(square)

##################################################
def add_noise(sound, loudness):
    noise = np.random.normal(0, loudness, sound.shape)
    return sound + noise

##################################################
def compute_correlations(left, right, samples_sep):
    for shift in range(-(samples_sep // 2), samples_sep // 2 + 1):
        left_shift = np.roll(left, shift)
        ccv = correlate(left_shift, right)
        least_sq = correlate_least_squares(left_shift, right)
        
        print("Shift: ", shift, " correlation: ", ccv, " least squares: ", least_sq)

##################################################
def correlate_from_microphone():
    sample_rate = 44100      # samples / sec
    speed_of_sound = 34300.0 # cm/sec
    distance = 28.0          # cm separation between microphones
    max_separation = sample_rate / speed_of_sound * distance # samples between microphones
    samples_sep = int(max_separation) + 1

#    data, sample_rate = read_file("voicerecorder.m4a")
#    print("Size: ", len(data), " sample rate: ", sample_rate)
    data = rec_audio(2.0, 1, 2, sample_rate)
    write_file('raw.wav', data, sample_rate)

    trimmed = get_interesting(data, 0.4, samples_sep)
    write_file('trimmed.wav', trimmed, sample_rate)

    print("Trimmed length: ", len(trimmed))    

    left = trimmed[:, 0]
    right = trimmed[:, 1]

#    noisy_left = add_noise(left, 0.1)
#    noisy_right = add_noise(right, 0.1)   
#    compute_correlations(noisy_left, noisy_right, samples_sep)
    compute_correlations(left, right, samples_sep)
        
##################################################
def correlate_from_file():
    filename = input("Enter filename: ")
    max_offset = input("Max offset: ")

    max_offset = int(max_offset)

    data, rate = sf.read(filename)
    left = data[:, 0]
    right = data[:, 1]
    
    compute_correlations(left, right, 2*max_offset)
##################################################
if __name__ == '__main__':
    correlate_from_file()
