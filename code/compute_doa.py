# Correlation code
import math
import numpy as np
import correlation as corr
import gcc_phat
import respeaker
import soundfiles

##################################################
# compute a correlation where large numbers (1) are good.
def compute_doa(dist, corr_1_3, corr_2_4, rate=16000):
    sound = 34300 # cm/sec
    
    delta_1_3 = corr_1_3 * sound / rate
    delta_2_4 = corr_2_4 * sound / rate
    delta_1_3 /= dist
    delta_2_4 /= dist

    if math.fabs(delta_1_3) > 1.3 or math.fabs(delta_2_4) > 1.3:
        print("Deltas out of range", delta_1_3, delta_2_4)
        return -1
    if math.fabs(delta_1_3) > 1 :
        delta_1_3 /= math.fabs(delta_1_3)
        
    if math.fabs(delta_2_4) > 1:
        delta_2_4 /= math.fabs(delta_2_4)
    
    print(f'Deltas: {delta_1_3:5.3f} {delta_2_4:5.3f}', end=' ')
    
    angle_1_3 = math.degrees( math.acos(delta_1_3) )
    angle_2_4 = math.degrees( math.acos(delta_2_4) )
    
    if angle_2_4 >= 0:
        angle_1 = angle_1_3 - 45
    else:
        angle_1 = -angle_1_3 + 135
        
    if angle_1_3 >= 0:
        angle_2 = -angle_2_4 + 135
    else:
        angle_2 = angle_2_4 - 135
        
    if angle_1 < 0:
        angle_1 += 360
    
    if angle_2 < 0:
        angle_2 += 360
        
    print(f'Angles: {angle_1_3:5.1f} {angle_2_4:5.1f} {angle_1:5.1f} {angle_2:5.1f}', end=' ')

    return angle_1
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
    
    data = soundfiles.rec_audio(0.5, device, channels, sample_rate)
    #write_file('raw.wav', data, sample_rate)

    #trimmed = soundfiles.get_interesting(data, 0.8, samples_sep)
    #if trimmed.shape[0] < 1000:
    #    print("No signal")
    #    return
    #else:
    #    print("size: ", data.shape[0], trimmed.shape[0])

    trimmed = data
    one = trimmed[:, 1]
    two = trimmed[:, 2]
    three = trimmed[:, 3]
    four = trimmed[:, 4]

    avg = np.average(one * one)
    if avg < 1.0e-6:
        print("No signal")
        return
    #print("Average:", avg)

    #write_file('trimmed.wav', trimmed, sample_rate)
    #write_channels('trimmed.wav', one, three, sample_rate)

    #print("Trimmed length: ", len(trimmed))    

#    noisy_left = add_noise(left, 0.1)
#    noisy_right = add_noise(right, 0.1)   
#    compute_correlations(noisy_left, noisy_right, samples_sep)
#    for ii in range(0,5):
#        print(f'({ii})', end=" ")
#        for jj in range(ii+1, 6):
#            corr = \
#                compute_correlations(trimmed[:, ii], trimmed[:, jj], samples_sep)
#
#            print(f'{corr[1]:3d}', end=" ")


#    print(f'{doa():4d}')
#    zero_two = compute_correlations(trimmed[:, 0], trimmed[:, 1], samples_sep)
#    zero_three = compute_correlations(trimmed[:, 0], trimmed[:, 1], samples_sep)
#    zero_four = compute_correlations(trimmed[:, 0], trimmed[:, 1], samples_sep)
#    zero_five = compute_correlations(trimmed[:, 0], trimmed[:, 1], samples_sep)
    
    
                
    one_two = corr.compute_correlations(one, two, samples_sep)        
    one_three = corr.compute_correlations(one, three, samples_sep)
    one_four = corr.compute_correlations(one, four, samples_sep)
    two_three = corr.compute_correlations(two, three, samples_sep)       
    two_four = corr.compute_correlations(two, four, samples_sep)
    three_four= corr.compute_correlations(three, four, samples_sep)

    gcc_1_2,c = gcc_phat.gcc_phat(one, two)
    gcc_1_3,c = gcc_phat.gcc_phat(one, three)
    gcc_2_4,c = gcc_phat.gcc_phat(two, four)

    angle = compute_doa(6.42, gcc_1_3, gcc_2_4)
    if angle >= 0:
        print(f'{one_two[1]:3d} {gcc_1_2:7.3f} {one_three[1]:3d} {gcc_1_3:7.3f}' ,
          f'{two_four[1]:3d} {gcc_2_4:7.3f} {respeaker.doa():4d}',
          f'{angle:5.1f}')
#    print(f'{one_two[1]:3d} {one_three[1]:3d} {one_four[1]:3d} {two_three[1]:3d}',
#          f'{two_four[1]:3d} {three_four[1]:3d} {respeaker.doa():4d}')
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
    device, rate = respeaker.pick_device()
    print('Running on device', device, 'at', rate, 'samples/sec')
    
    #correlate_from_file()
    while True:
        correlate_from_microphone(device, rate)
