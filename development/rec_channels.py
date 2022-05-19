from usb_4_mic_array.tuning import Tuning
import usb.core
import usb.util
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
def pick_device():
    devices = sd.query_devices()
    for ii in range(len(devices)):
        device = devices[ii]
        if 'ReSpeaker' in device['name'] and  device['max_input_channels'] == 6:
            return ii, int(device['default_samplerate'])

    return -1

##################################################
def write_file(filename, left, right, samplerate):
    data = np.empty( (len(left), 2) )
    data[:,0] = left
    data[:,1] = right
    print("Writing sound file: ", filename, 'rate', samplerate)
    sf.write(filename, data, samplerate, 'PCM_16')
    print("Done")
##################################################
if __name__ == '__main__':
    device, rate = pick_device()
    print('Running on device', device, 'at', rate, 'samples/sec')
    
    data = rec_audio(5.0, device, 6, rate)

    write_file("respeaker_1_2.wav", data[:, 1], data[:, 2], rate)
    write_file("respeaker_3_4.wav", data[:, 3], data[:, 4], rate)

    v1 = np.average(data[:, 1] * data[:, 1])
    v2 = np.average(data[:, 2] * data[:, 2])
    v3 = np.average(data[:, 3] * data[:, 3])
    v4 = np.average(data[:, 4] * data[:, 4])


    print(v1, v2, v3, v4)
    
    samples = [v1, v2, v3, v4]
    max_v = np.max(samples)

    r1 = np.sqrt(max_v/v1)
    r2 = np.sqrt(max_v/v2)
    r3 = np.sqrt(max_v/v3)
    r4 = np.sqrt(max_v/v4)

    data[:, 1] = r1 * data[:, 1]
    data[:, 2] = r2 * data[:, 2]
    data[:, 3] = r3 * data[:, 3]
    data[:, 4] = r4 * data[:, 4]
    
    v1 = np.average(data[:, 1] * data[:, 1])
    v2 = np.average(data[:, 2] * data[:, 2])
    v3 = np.average(data[:, 3] * data[:, 3])
    v4 = np.average(data[:, 4] * data[:, 4])

    print(v1, v2, v3, v4)
    
   
    write_file("respeaker.wav", data[:, 3], data[:, 4], rate)

    
    
    
