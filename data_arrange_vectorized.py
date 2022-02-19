import pandas as pd
import numpy as np
from scipy.signal import savgol_filter as sgf

smoothing_window = 7
smoothing_order = 2

def deriv(p, w):
    return p - np.roll(p,w)

folder = r''

OS_metadata = pd.read_csv('reference_absorbance_raw_metadata.csv', encoding='latin1')
OS_library = pd.read_csv('reference_absorbance_raw.csv')
OS_library = OS_library[((OS_library['wavenumber']<2300) | (OS_library['wavenumber']>2400)) & (OS_library['wavenumber']>900)]
OS_library = OS_library.sort_values(by=['wavenumber'])

wavenos = np.array(range(900,4000,1))

grouped = OS_library.groupby(['sample_name'])

def interpolator(frame):
    try:
        sigint = np.interp(wavenos,frame['wavenumber'],frame['intensity'])
    except ValueError: sigint = np.zeros(len(wavenos))
    sigint = sigint - np.min(sigint)
    #der_sigint = sgf(deriv(sigint,smoothing_window),smoothing_window,smoothing_order)
    print('frame')
    return pd.Series(sigint)

def deriv_smth(ser):
    return pd.Series(sgf(deriv(ser,smoothing_window),smoothing_window,smoothing_order))

OS_intT = grouped.apply(interpolator)

OS_int = OS_intT.T.set_axis(wavenos)
OS_int.index.names=['wavenumbers']

OS_der = OS_int.apply(deriv_smth,axis=0)

OS_der = OS_der.set_axis(wavenos)
OS_der.index.names=['wavenumbers']

file_int = 'open_specy_ALL_interp.csv'
file_der = 'open_specy_ALL_deriv.csv'

OS_int.to_csv(file_int)
OS_der.to_csv(file_der)
