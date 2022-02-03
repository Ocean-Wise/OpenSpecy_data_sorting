# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 13:23:52 2021

@author: Shreyas
"""

import pandas as pd
import os
import numpy as np
from scipy import stats

db_folder= ''                                  ##Option for hardwire input
#db_folder=input("Enter database folder path ")  ##Option for custom database
#db_file='primpke2018esm5.csv'                                     ##Option for hardwire input
#db_file=input("Enter database file name ")      ##Option for custom database

db_deriv_file='primpke2018esm5_1st_deriv.csv' #first derivative database file
db_catID_file='primpke2018_cluster_ID.csv' #simplified catID database file

database_der = pd.read_csv(os.path.join(db_folder,db_deriv_file))
db_catID = pd.read_csv(os.path.join(db_folder,db_catID_file))

columnheads=database_der.columns[3:]
wavenumbers=[int(k) for k in columnheads]

def norm_pearson(p,q):
    modp = p/(np.max(p) - np.min(p))
    modq = q/(np.max(q) - np.min(q))
    return stats.pearsonr(modp,modq)[0]

def catID(k):
    return (db_catID[db_catID['Cluster Autoanalysis'] == k]['Cluster_name']).values[0]
    
catIDs = [catID(k) for k in database_der['Cluster Autoanalysis']]

def library_fit_1(der_spectrum, wns, spectrum_name):
    pearson_rs=[]
    for n in range(len(database_der.index)):
        pearson_rs.append(norm_pearson(np.interp(wavenumbers,wns,der_spectrum),
                                         database_der.iloc[n,3:]))
    
    nearest1=pearson_rs.index(min(pearson_rs))
    #bf_name = database_der.iloc[nearest1,1]
    best_fit_spec = pd.DataFrame(data = {'wavenumbers': wavenumbers,
                                         'spectrum': database_der.iloc[nearest1,3:]})
    best_fit_name = database_der.iloc[nearest1,1]
    best_fit_id = database_der.iloc[nearest1,2]
    sorter_df = pd.concat([database_der.iloc[0:,0:3],
                           pd.Series(pearson_rs, name='Pearson_Rs'),
                           pd.Series(catIDs, name='Category_IDs')],
                          axis=1, sort=False)
    sorter_df = (sorter_df.sort_values(by=['Pearson_Rs'], ascending = True))[:10]
    return sorter_df, best_fit_spec, best_fit_name, best_fit_id, min(pearson_rs)
