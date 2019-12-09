import os
import mne
import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt
from scipy.integrate import simps
from scipy.stats import kurtosis, skew


class SupraThreshold:
    
    def __init__(self, data, channel, std_num, interp_fac):
        self.data = data
        self.channel = channel
        self.std_num = std_num
        self.interp_fac = interp_fac
    
    
    def compute_features(self):
        "Extract desired rhythm from desired channel and compute features"
        
        # Loading data into MNE
        raw = mne.io.read_raw_brainvision(self.data)
        raw.load_data()
        raw.set_eeg_reference('average', projection=True)
        raw.apply_proj()
        
        # Applying Hilbert envelope on chosen rhythm
        raw_hilb = raw.copy()
        hilb_picks = mne.pick_types(raw.info, meg=False, eeg=True)
        raw_hilb.apply_hilbert(hilb_picks)
        raw_amp = raw_hilb.copy()
        raw_amp.apply_function(np.abs, hilb_picks)
        smr_amp = raw_amp[hilb_picks[self.channel]][0][0].real

        # Getting mean and standard deviation of chosen rhythm
        mean = np.mean(smr_amp)
        std = np.std(smr_amp)
        
        # Interpolating chosen rhythm for more accurate measures
        xvals = np.linspace(0, len(smr_amp), len(smr_amp)*self.interp_fac)
        x = np.arange(0, len(smr_amp))
        smr_interp = np.interp(xvals, x, smr_amp)
        
        # Computing intersection points between threshold and chosen rhythm
        h = np.ones((len(smr_interp),))*(mean+self.std_num*std)
        idx = np.argwhere(np.diff(np.sign(h - smr_interp))).flatten() 
        
        # Removing first intersection point if rhythm starts above threshold
        if smr_interp[0] > h[0]:
            idx = np.delete(idx, 0)
        if smr_interp[-1] > h[0]:
            idx = np.delete(idx, -1)
        
        # Since Python indexing starts at 0, all intersection points crossing
        # above threshold will have even indices, and those crossing below 
        # threshold will have odd indices. This is used to capture individual
        # suprathreshold bursts.
        even, odd = [], []
        for number in range(len(idx)):
            if (number % 2) == 0: 
                even.append(number)
            else:
                odd.append(number) 
    
        # Computing maximum, duration, skewness, kurtosis, and area
        all_M, all_D, all_S, all_K, all_A = [], [], [], [], []
        for i in range(len(even)):
            m = smr_interp[idx[even[i]]:idx[odd[i]]]
            l = np.arange(0, len(m))
            
            maximum = max(m)
            all_M.append(maximum)
            
            exc_length = idx[odd[i]]-idx[even[i]]
            all_D.append(exc_length)
            
            ske = skew(m)
            all_S.append(ske)
            
            kurt = kurtosis(m)
            all_K.append(kurt)
            
            area = simps(m, l)
            cut_out = h[0]*len(l)
            area -= cut_out # remove rectangle between threshold and x-axis
            all_A.append(area)
            
        # Scaling duration and area by dividing by interpolation factor    
        all_D = [j / self.interp_fac for j in all_D]
        all_A = [j / self.interp_fac for j in all_A]
        
        feats = {'Maximum': all_M, 'Duration': all_D, 'Skewness': all_S,
                 'Kurtosis': all_K, 'Area': all_A}
        
        return pd.DataFrame(feats)
    

path = os.getcwd()+'/Data/'
data = path+'Cognitive_Assessment_01.vhdr'


def main():
    inst = SupraThreshold(data, 5, 2, 100)
    df = inst.compute_features()
    return df
    
if __name__ == '__main__':
    df = main()


#plt.figure()
#plt.hist(res, bins='auto')
#plt.axvline(x=mean_area, color='r')
#plt.axvline(x=mean_area-std_area, color='y')
#plt.axvline(x=mean_area+std_area, color='y')
#plt.show()