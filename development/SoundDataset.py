#!/usr/bin/python
###################################################################
"""Module for importing audio to PyTorch. The audio is sterio and the
classification represents the shift, in samples, of the two channels."""
import os
import pandas as pd
#import numpy as np
import torch
from torch.utils.data import Dataset
import torchaudio

class OffsetAudio(Dataset):
    def __init__(self, annotations_file, sound_dir, transform=None, target_transform=None):
        """Initialize an OffsetAudio dataset. 

        Required parameters include annotations_file (specifies the category 
        for each sound file) and sound_dir (specifies the directory that 
        contains the sound files"""
        self.snd_labels = pd.read_csv(annotations_file)
        self.snd_dir = sound_dir
        self.transform = transform
        self.target_transform = target_transform
        self.data_rate = 44100

    def __len__(self):
        return len(self.snd_labels)

    def __getitem__(self, idx):
        sound_path = os.path.join(self.snd_dir, self.snd_labels.iloc[idx, 0])
        sound, self.data_rate = torchaudio.load(sound_path)
        label = self.snd_labels.iloc[idx, 1]
        if self.transform:
            sound = self.transform(sound)
        if self.target_transform:
            label = self.target_transform(label)
        return sound, label

    def data_rate(self):
        return self.data_rate
