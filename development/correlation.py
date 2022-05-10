# Correlation code
from usb_4_mic_array.tuning import Tuning
import usb.core
import usb.util
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
    max_ccv = -100000
    max_ccv_index = -1
    min_sq = 10000000
    min_sq_index = -1
    
    for shift in range(-samples_sep, samples_sep + 1):
        left_shift = np.roll(left, shift)
        ccv = correlate(left_shift, right)
        if abs(ccv) > max_ccv:
            max_ccv = abs(ccv)
            max_ccv_index = shift
            
        least_sq = correlate_least_squares(left_shift, right)
        if least_sq < min_sq:
            min_sq = least_sq
            min_sq_index = shift
        
        # print("Shift: ", shift, " correlation: ", ccv, " least squares: ", least_sq)

    #print("range: ", -samples_sep, samples_sep)
    #print("Max ccv:", max_ccv, max_ccv_index)
    #print("Min sq:", min_sq, min_sq_index)

    return [max_ccv, max_ccv_index, min_sq, min_sq_index]
        
##################################################
def pick_device():
    devices = sd.query_devices()
    for ii in range(len(devices)):
        device = devices[ii]
        if 'ReSpeaker' in device['name'] and  device['max_input_channels'] == 6:
            return ii, device['default_samplerate']

    return -1

##################################################
def doa():
    dev = usb.core.find(idVendor=0x2886, idProduct=0x0018)
 
    if dev:
        Mic_tuning = Tuning(dev)
        return Mic_tuning.direction

    return -1

##################################################
def correlate_from_microphone(device, sample_rate):
    #sample_rate = 44100      # samples / sec
    #sample_rate = 16000
    channels = 6
    speed_of_sound = 34300.0 # cm/sec
    distance = 6.5          # cm separation between microphones
    distance = 20
    max_separation = sample_rate / speed_of_sound * distance # samples between microphones
    samples_sep = int(max_separation) + 1

    ##############
    # samples_sep = 50
    ##############
    
#    data, sample_rate = read_file("voicerecorder.m4a")
#    print("device", device, "channels", channels, "rate", sample_rate)
    
    data = rec_audio(0.5, device, channels, sample_rate)
    #write_file('raw.wav', data, sample_rate)

    #trimmed = get_interesting(data, 0.4, samples_sep)
    trimmed = data
    one = trimmed[:, 1]
    two = trimmed[:, 2]
    three = trimmed[:, 3]
    four = trimmed[:, 4]

    #write_file('trimmed.wav', trimmed, sample_rate)
    #write_channels('trimmed.wav', one, three, sample_rate)

    #print("Trimmed length: ", len(trimmed))    

#    noisy_left = add_noise(left, 0.1)
#    noisy_right = add_noise(right, 0.1)   
#    compute_correlations(noisy_left, noisy_right, samples_sep)
    one_two = compute_correlations(one, two, samples_sep)        
    one_three = compute_correlations(one, three, samples_sep)
    one_four = compute_correlations(one, four, samples_sep)
    two_three = compute_correlations(two, three, samples_sep)       
    two_four = compute_correlations(two, four, samples_sep)
    three_four= compute_correlations(three, four, samples_sep)

    print(f'{one_two[1]:3d} {one_three[1]:3d} {one_four[1]:3d} {two_three[1]:3d}',
          f'{two_four[1]:3d} {three_four[1]:3d} {doa():4d}')
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
    device, rate = pick_device()
    print('Running on device', device, 'at', rate, 'samples/sec')
    
    #correlate_from_file()
    while True:
        correlate_from_microphone(device, rate)
