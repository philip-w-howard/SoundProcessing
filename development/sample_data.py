# Create a data set from one long sound file
import numpy as np
import wave
import soundfile as sf
import os
import random

g_index = 0

##################################################
# Convert a numeric offset to a text directory name
def make_dir_name(offset):
    if offset < 0:
        return 'N' + str(-offset)
    elif offset == 0:
        return 'Z'
    else:
        return 'P' + str(offset)

##################################################
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

##################################################
# Returns True if the sample isn't too quiet
# determination is based on the percentage of samples above a threshold
def valid_sample(slice, threshold=0.15, num_above=0.03):
    count = np.sum(abs(slice) > threshold)
    if count > len(slice) * num_above:
        return True

    return False

##################################################
# create a unique filename given an offset
def create_filename(dir_name, offset):
    global g_index
    g_index += 1
    return dir_name + '/' + make_dir_name(offset) + '/' + str(g_index) + '.wav'

##################################################
# create a time shifted file from a mono source
def write_file(dir_name, slice, clip_len, sample_rate, offset, start):
    sample = np.empty( (clip_len, 2) )
    sample[:,0] = slice[offset + start : offset + start + clip_len]
    sample[:,1] = slice[start : start + clip_len]

    sf.write(create_filename(dir_name, offset), sample, sample_rate, 'PCM_16')

##################################################
# read a sound file and chop it up into shifted pieces
def write_dir(filename, dir_name, clip_len, min_offset, max_offset):
    data, sample_rate = sf.read(filename)   
    print('Length', len(data), 'sample rate:', sample_rate)

    # only use one channel if the data file is stereo
    if len(data.shape) > 1:
        data = data[:,0]
    oversize = 2*max(abs(min_offset), abs(max_offset))   

    # create directory structure
    os.mkdir(dir_name, mode=700)
    for offset in range(min_offset, max_offset+1):
        subdirname = make_dir_name(offset)
        print("Creating", subdirname)
        os.mkdir(dir_name + "/" + subdirname, 700)

    num_files = len(data) // clip_len

    offset = min_offset
    count = 0
    for index in range(num_files) :
        slice = data[index * clip_len : (index+1)*clip_len + oversize]
        if valid_sample(slice):
            write_file(dir_name, slice, clip_len, sample_rate, offset, abs(min_offset))
            offset += 1
            count += 1
            if offset > max_offset :
                offset = min_offset

    print('wrote', count, 'files')

##################################################
# Get list of files from the directory
def get_file_list(dirname):
    filelist = []
    categories = os.listdir(dirname)
    for cat in categories:
        files = os.listdir(dirname + '/' + cat)
        filelist.append([cat, files])

    return filelist

##################################################
# Read first file to get the size
def get_file_size(dirname, filelist):
    data, rate = sf.read(dirname + '/' + filelist[0][0] + '/' + filelist[0][1][0])
    return len(data)

##################################################
# add a file to a list
def add_file(data, ans, dir, subdir, file):
    name = dir + '/' + subdir + '/' + file
    sample, rate = sf.read(name)
    data = np.insert(data, 0, sample, axis=0)
    ans = np.insert(ans, 0, offset_from_name(subdir))

    return data,ans

##################################################
# Build traning and validation sets
def read_dir(dirname, percent):
    random.seed()

    filelist = get_file_list(dirname)
    size = get_file_size(dirname, filelist)

    train_data = np.empty( (0, size, 2) )
    train_ans = np.empty( (0) )
    
    test_data = np.empty( (0, size, 2) )
    test_ans = np.empty( (0) )
    
    while len(filelist) > 0:
        for index in range(len(filelist)):
            filename = filelist[index][1].pop()
            value = random.random()
            if value <= percent :
                train_data, train_ans = add_file(train_data, train_ans, dirname, filelist[index][0], filename)
            else:
                test_data, test_ans = add_file(test_data, test_ans, dirname, filelist[index][0], filename)
                

        print('remaining len:', len(filelist[0][1]))
        for index in range(len(filelist)-1, -1, -1):
            if len(filelist[index][1]) == 0 :
                filelist.pop(index)

    return train_data, train_ans, test_data, test_ans

##################################################
if __name__ == '__main__':
    operation = input('read or write a directory (enter read or write): ')
    if operation == 'write':
        filename = input("source sound file: ")

        dir_name = input("Output directory: ")
        clip_len_t = input("Length per sample: ")
        min_offset_t = input("Min offset: ")
        max_offset_t = input("Max offset: ")

        #files_per_offset = int(files_per_offset_t)
        clip_len = int(clip_len_t)
        min_offset = int(min_offset_t)
        max_offset = int(max_offset_t)

        write_dir(filename, dir_name, clip_len, min_offset, max_offset)
    elif operation == 'read':
        dirname = input('directory: ')
        percent_training = input('percent_training: ')
        percent = float(percent_training)

        train_data, train_answers, val_data, val_answers = read_dir(dirname, percent)
        print('training:', train_data.shape, train_answers.shape)
        print('testing:', val_data.shape, val_answers.shape)
    else:
        print('Invalid operation. Must be "read" or "write"')

    print('done')
