# Read a dataset from a directory tree
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

# Get list of files from the directory
def get_file_list(dirname):
    filelist = []
    categories = os.listdir(dirname)
    for cat in categories:
        files = os.listdir(dirname + '/' + cat)
        filelist.append([cat, files])

    return filelist

# Read first file to get the size
def get_file_size(dirname, filelist):
    data, rate = sf.read(dirname + '/' + filelist[0][0] + '/' + filelist[0][1][0])
    return len(data)

# add a file to a list
def add_file(data, ans, dir, subdir, file):
    name = dir + '/' + subdir + '/' + file
#    print('adding', name)
    sample, rate = sf.read(name)
#    print("data", data.shape, "sample", sample.shape)
    data = np.insert(data, 0, sample, axis=0)
    ans = np.insert(ans, 0, offset_from_name(subdir))

    return data,ans

# Build traning and validation sets
def read_dir(dirname, percent):
    filelist = get_file_list(dirname)
    size = get_file_size(dirname, filelist)

    train_data = np.empty( (0, size, 2) )
    train_ans = np.empty( (0) )
    
    test_data = np.empty( (0, size, 2) )
    test_ans = np.empty( (0) )
    
    while len(filelist) > 0:
        for index in range(len(filelist)):
            filename = filelist[index][1].pop()
            train_data, train_ans = add_file(train_data, train_ans, dirname, filelist[index][0], filename)

        print('len 0)', len(filelist[0][1]))
        for index in range(len(filelist)-1, -1, -1):
            #print('index', index, len(filelist[index][1]))
            #print('filelist[index]', filelist[index])
            if len(filelist[index][1]) == 0 :
                print('popping', index)
                filelist.pop(index)

    return train_data, train_ans, test_data, test_ans

##################################################
if __name__ == '__main__':
    dirname = input('directory: ')
    percent_training = input('percent_training: ')
    percent = float(percent_training)

    train_data, train_answers, val_data, val_answers = read_dir(dirname, percent)
    print(train_data.shape, train_answers.shape)
