# Correlation code
import numpy as np

##################################################
# compute a correlation where large numbers (1) are good.
def correlate(left, right):
    avg_l = np.average(left);
    avg_r = np.average(right);

    diff_l = left - avg_l
    diff_r = right - avg_r;

    sum1 = np.sum( diff_l * diff_r)

    square_l = diff_l * diff_l
    square_r = diff_r * diff_r
    
    sum2 = np.sum(square_l)
    sum3 = np.sum(square_r)

    ccv = sum1/(np.sqrt(sum2) * np.sqrt(sum3))

    return ccv
    
##################################################
# compute a correlation where small numbers (0) are good.
def correlate_least_squares(left, right):
    diff = left - right
    square = diff * diff   
    return np.sum(square)

##################################################
def compute_correlations(left, right, samples_sep):
    max_ccv = -100000
    max_ccv_index = -1
    min_sq = 10000000
    min_sq_index = -1
    
    for shift in range(-samples_sep, samples_sep + 1):
        left_shift = np.roll(left, shift)
        ccv = correlate(left_shift, right)
        if abs(ccv) > max_ccv:
            max_ccv = abs(ccv)
            max_ccv_index = shift
            
        least_sq = correlate_least_squares(left_shift, right)
        if least_sq < min_sq:
            min_sq = least_sq
            min_sq_index = shift
        
        # print("Shift: ", shift, " correlation: ", ccv, " least squares: ", least_sq)

    #print("range: ", -samples_sep, samples_sep)
    #print("Max ccv:", max_ccv, max_ccv_index)
    #print("Min sq:", min_sq, min_sq_index)

    return [max_ccv, max_ccv_index, min_sq, min_sq_index]
