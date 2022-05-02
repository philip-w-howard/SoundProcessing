import numpy as np
import wave
import soundfile as sf

data, samplerate = sf.read('ben_s.wav')

num_samples = 500
size = samplerate
threshold = 0.15

if len(data) < size * num_samples:
    num_samples = len(data) // size

num_ok = 0
num_ok_2 = 0
same_ok = 0
for index in range(num_samples):
    slice = data[index*size : (index+1)*size]

    count = np.sum(abs(slice) > threshold)
    #count = 0
    #for value in slice[0] :
    #    if abs(value) > threshold:
    #       count += 1
    #
    if count > size * 0.03 :
        num_ok += 1

    max = slice.max()
    if max > threshold * 1.6:
        num_ok_2 += 1

    if max > threshold * 1.6 and count > size * 0.03:
        same_ok += 1
        
print("samples:", num_samples, "ok", num_ok, num_ok_2, same_ok)
               
    
