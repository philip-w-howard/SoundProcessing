# Compute doa from correlation values
import numpy as np

##################################################
# compute a correlation where large numbers (1) are good.
def computed_doa(dist, corr_1_3, corr_2_4, rate=16000):
    sound = 34300 # cm/sec
    
    delta_1_3 = corr_1_3 * sound / rate
    delta_2_4 = corr_2_4 * sound / rate
    
    angle_1_3 = np.arccos(delta_1_3 / dist) * 180 / np.pi
    angle_2_4 = np.arccos(delta_2_4 / dist) * 180 / np.pi
    
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
        
    print('Angles: ', angle_1_3, angle_2_4, angle_1, angle_2)

    return angle_1
    
