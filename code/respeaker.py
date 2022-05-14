# routines for handling the ReSpeaker USB 4-microphone array
from usb_4_mic_array.tuning import Tuning
import usb.core
import usb.util
import numpy as np
import sounddevice as sd

        
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

