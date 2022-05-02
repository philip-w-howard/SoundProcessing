# Create a data set from one long sound file
import numpy as np
import wave
import soundfile as sf
import os

g_dir_name = "sound_files"
g_sample_rate = 44100
g_index = 0

# Convert a numeric offset to a text directory name
def dir_name(offset):
    if offset < 0:
        return 'N' + str(-offset)
    elif offset == 0:
        return 'Z'
    else:
        return 'P' + str(offset)

# Convert a text directory name to an integer offset
def offset_from_name(name):
    if name[0] == 'Z':
        return 0
    elif name[0] == 'P':
        return int(name[1:])
    elif name[0] == 'N':
        return -int(name[1:])
    else:
        raise Exception("Invalid directory name")

# Returns True if the sample isn't too quiet
# determination is based on the percentage of samples above a threshold
def valid_sample(slice, threshold=0.15, num_above=0.03):
    count = np.sum(abs(slice) > threshold)
    if count > len(slice) * num_above:
        return True

    return False

# create a unique filename given an offset
def create_filename(offset):
    global g_index
    g_index += 1
    return g_dir_name + '/' + dir_name(offset) + '/' + str(g_index) + '.wav'

# create a time shifted file from a mono source
def write_file(slice, clip_len, offset, start):
    sample = np.empty( (clip_len, 2) )
    sample[:,0] = slice[offset + start : offset + start + clip_len]
    sample[:,1] = slice[start : start + clip_len]

    sf.write(create_filename(offset), sample, g_sample_rate, 'PCM_16')

##################################################
if __name__ == '__main__':
    filename = input("source sound file: ")

    # read data
    
    data, g_sample_rate = sf.read(filename)
    
    print('Length', len(data), 'sample rate:', g_sample_rate)

    g_dir_name = input("Output directory: ")
    clip_len_t = input("Length per sample: ")
    min_offset_t = input("Min offset: ")
    max_offset_t = input("Max offset: ")

    #files_per_offset = int(files_per_offset_t)
    clip_len = int(clip_len_t)
    min_offset = int(min_offset_t)
    max_offset = int(max_offset_t)

    oversize = 2*max(abs(min_offset), abs(max_offset))   

    # create directory structure
    os.mkdir(g_dir_name, mode=700)
    for offset in range(min_offset, max_offset+1):
        subdirname = dir_name(offset)
        print("Creating", subdirname)
        os.mkdir(g_dir_name + "/" + subdirname, 700)

    num_files = len(data) // clip_len

    offset = min_offset
    count = 0
    for index in range(num_files) :
        slice = data[index * clip_len : (index+1)*clip_len + oversize]
        if valid_sample(slice):
            write_file(slice, clip_len, offset, abs(min_offset))
            offset += 1
            count += 1
            if offset > max_offset :
                offset = min_offset

    print('wrote', count, 'files')
