import pandas as pd
import numpy as np
from scipy.signal import savgol_filter as sgf

smoothing_window = 5
smoothing_order = 2

def deriv(p, w):
    return p - np.roll(p,w)

folder = r''

OS_metadata = pd.read_csv('ftir_metadata.csv')
OS_library = pd.read_csv('ftir_library.csv')
OS_library = OS_library[((OS_library['wavenumber']<2300) | (OS_library['wavenumber']>2400)) & (OS_library['wavenumber']>905)]

OS_int = pd.DataFrame()
OS_derivative = pd.DataFrame()
wavenos = np.array(range(905,4000,1))
OS_int['wavenos'] = wavenos
OS_int.set_index('wavenos')

OS_derivative['wavenos'] = wavenos
OS_derivative.set_index('wavenos')

for name in OS_metadata['sample_name']:
    wn = OS_library[OS_library['sample_name']==name].sort_values(by='wavenumber')['wavenumber']
    sig = OS_library[OS_library['sample_name']==name].sort_values(by='wavenumber')['intensity']
    sigint = np.interp(wavenos,wn,sig)
    sigint = sigint - np.min(sigint)
    OS_int[name] = sigint
    der_sigint = sgf(deriv(sigint,smoothing_window),smoothing_window,smoothing_order)
    OS_derivative[name] = der_sigint


file_int = 'open_specy_ftir_library_INT.csv'
file_der = 'open_specy_ftir_library_DERINT.csv'

OS_int.to_csv(file_int, index=False)
OS_derivative.to_csv(file_der, index=False)

print(OS_derivative)