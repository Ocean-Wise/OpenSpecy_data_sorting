import pandas as pd
import numpy as np
from scipy import stats

OS_metadata = pd.read_csv('ftir_metadata.csv')
der_spectra = pd.read_csv('open_specy_ftir_library_DERINT.csv')

del der_spectra['wavenos']

def norm_pearson(p,q):
    modp = p/(np.max(p) - np.min(p))
    modq = q/(np.max(q) - np.min(q))
    return stats.pearsonr(modp,modq)[0]

tuples = []
distances = []

for ix in range(1,len(der_spectra.columns)+1):
    for ix2 in range(ix+1,len(der_spectra.columns)+1):
        tuples.append((ix,ix2))
        distances.append(norm_pearson(der_spectra[str(ix)],der_spectra[str(ix2)]))


dist_key = pd.DataFrame()
dist_key['tuples'] = tuples
dist_key['distances'] = distances

def cluster_tot(threshold):
    clusters = []
    for ix in range(1,637):
        if ix not in [item for sublist in clusters for item in sublist]:
            prox_tups = dist_key[(dist_key['tuples'].apply({ix}.issubset)) & (dist_key['distances']>threshold)]['tuples']
            cluster1 = [item for sublist in prox_tups for item in sublist if item != ix]
            cluster1.insert(0,ix)
            clusters.append(cluster1)
    return clusters

clusters = cluster_tot(.3)
cluster_key = []
for sn in OS_metadata['sample_name']:
    cluster_key.append(next((i for i,v in enumerate(clusters) if (sn in v)), [99]))
#    for ix in range(len(clusters)):
#        if sn in clusters[ix]:
#            cluster_key.append(ix)

OS_metadata['cluster_key'] = cluster_key
OS_metadata.to_csv('ftir_metadata_clusters.csv')