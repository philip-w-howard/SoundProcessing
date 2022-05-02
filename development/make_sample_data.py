# Create a data set from one long sound file
import numpy as np
import wave
import soundfile as sf
import os

def dir_name(offset):
    if offset < 0:
        return 'N' + str(-offset)
    elif offset == 0:
        return 'Z'
    else:
        return 'P' + str(offset)

def valid_sample(slice, threshold=0.15, num_above=0.03):
    count = np.sum(abs(slice) > threshold)
    if count > len(slice) * num_above:
        return True

    return False

if __name__ == '__main__':
    filename = input("source sound file: ")

    # read data
    data, samplerate = sf.read(filename)
    print('Length', len(data), 'sample rate:', samplerate)

    dirname = input("Output directory: ")
    clip_len_t = input("Length per sample: ")
    min_offset_t = input("Min offset: ")
    max_offset_t = input("Max offset: ")

    #files_per_offset = int(files_per_offset_t)
    clip_len = int(clip_len_t)
    min_offset = int(min_offset_t)
    max_offset = int(max_offset_t)

    # create directory structure
    os.mkdir(dirname, mode=700)
    for offset in range(min_offset, max_offset+1):
        subdirname = dir_name(offset)
        print("Creating", subdirname)
        os.mkdir(dirname + "/" + subdirname, 700)

    num_files = len(data) // clip_len

    offset = min_offset
    count = 0
    for index in range(num_files) :
        slice = data[index * clip_len : (index+1)*clip_len]
        if valid_sample(slice):
            sf.write(dirname + '/' + dir_name(offset) + '/' + str(index) + '.wav',
                     slice, samplerate, 'PCM_16')
            offset += 1
            count += 1
            if offset > max_offset :
                offset = min_offset

    print('wrote', count, 'files')
