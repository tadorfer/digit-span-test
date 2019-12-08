from scipy.integrate import simps
import numpy as np
import matplotlib.pyplot as plt
import mne
import os


def plotArea():

    std_num = 2
    interp_fac = 100
    
        
    path = os.getcwd()+'/Data/'
    data = path+'Cognitive_Assessment_01.vhdr'
    print(data)
    raw = mne.io.read_raw_brainvision(data)
    raw.load_data()
    raw.set_eeg_reference('average', projection=True)
    raw.apply_proj()
        
    c3 = 14 # channel C3
    
    raw_hilb = raw.copy()
    hilb_picks = mne.pick_types(raw.info, meg=False, eeg=True)
    raw_hilb.apply_hilbert(hilb_picks)
    raw_amp = raw_hilb.copy()
    raw_amp.apply_function(np.abs, hilb_picks)
    smr_amp = raw_amp[hilb_picks[c3]][0][0].real
    smr_amp = smr_amp[:300000] # take first 5mins of EEG data
    
    mean_y1 = np.mean(smr_amp)
    std_y1 = np.std(smr_amp)
    
    xvals = np.linspace(0,len(smr_amp),len(smr_amp)*interp_fac)
    x = np.arange(0, len(smr_amp))
    smr_interp = np.interp(xvals, x, smr_amp)
    
    h = np.ones((len(smr_interp),))*(mean_y1+std_num*std_y1)
    idx = np.argwhere(np.diff(np.sign(h - smr_interp))).flatten() # where horizontal line intersects with y1
    
    if smr_interp[0] > h[0]:
        idx = np.delete(idx, 0)
    if smr_interp[-1] > h[0]:
        idx = np.delete(idx, -1)
    
    even, odd = [], []
    for number in range(len(idx)):
        if (number % 2) == 0: 
            even.append(number)
        else:
            odd.append(number) 
    print([len(even), len(idx)])
    
    res, inds_mark, bursts, caps = [], [], [], []
    for k in range(len(even)):
        m = smr_interp[idx[even[k]]:idx[odd[k]]]
        l = np.arange(0, len(m))
        area = simps(m, l)
        cut_out = h[0]*len(l)
        area -= cut_out
        res.append(area) # calculate distance between intersections (i.e. time of excursion)
        inds_mark.append(int(np.median([idx[even[k]], idx[odd[k]]])))
        burst_inds = (idx[even[k]], idx[odd[k]])
        bursts.append(burst_inds)
        caps.append([smr_interp[burst_inds[0]:burst_inds[1]]])
        
    res = [z / interp_fac for z in res]
    mean_area = np.mean(res)
    std_area = np.std(res)
    
    
    plt.figure()
    plt.hist(res, bins='auto')
    plt.axvline(x=mean_area, color='r')
    plt.axvline(x=mean_area-std_area, color='y')
    plt.axvline(x=mean_area+std_area, color='y')
    
    plt.show()
    
    return res, raw
    
result, raw = plotArea()