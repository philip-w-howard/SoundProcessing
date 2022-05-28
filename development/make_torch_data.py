#!/usr/bin/python
# Create a data set from one long sound file
import numpy as np
import wave
import soundfile as sf
import os

# Returns True if the sample isn't too quiet
# determination is based on the percentage of samples above a threshold
def valid_sample(slice, threshold=0.15, num_above=0.03):
    count = np.sum(abs(slice) > threshold)
    if count > len(slice) * num_above:
        return True

    return False

# create a time shifted file from a mono source
def write_file(filename, slice, clip_len, offset, start, rate):
    print('creating file:', filename)
    sample = np.empty( (clip_len, 2) )
    sample[:,0] = slice[offset + start : offset + start + clip_len]
    sample[:,1] = slice[start : start + clip_len]

    sf.write(filename, sample, rate, 'PCM_16')

##################################################
if __name__ == '__main__':
    filename = input("source sound file: ")
    output_name = input("output base name: ")

    # read data
    
    data, rate = sf.read(filename)
    
    print('Length', len(data), 'sample rate:', rate)

    dir_name = input("Output directory: ")
    clip_len_t = input("Length per sample: ")
    min_offset_t = input("Min offset: ")
    max_offset_t = input("Max offset: ")

    #files_per_offset = int(files_per_offset_t)
    clip_len = int(clip_len_t)
    min_offset = int(min_offset_t)
    max_offset = int(max_offset_t)

    oversize = 2*max(abs(min_offset), abs(max_offset))   

    # create directory structure
    os.mkdir(dir_name, mode=0o700)

    num_files = len(data) // clip_len

    offset = min_offset
    count = 0
    sample_list = []

    for index in range(num_files) :
        slice = data[index * clip_len : (index+1)*clip_len + oversize]
        if valid_sample(slice):
            curr_file = output_name + "_" + str(count) + '.wav'
            name =  dir_name + '/' + curr_file
            write_file(name, slice, clip_len, offset, abs(min_offset), rate)
            sample_list.append([curr_file, offset])
            offset += 1
            count += 1
            if offset > max_offset :
                offset = min_offset

    csv = open(dir_name + '/samples.csv', 'w');
    for sample in sample_list:
        print(f'{sample[0]}, {sample[1]}', file=csv)


    csv.close()

    print('wrote', count, 'files')
