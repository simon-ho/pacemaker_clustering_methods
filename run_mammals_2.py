import os, sys, re
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn import mixture
import scipy.stats as sp
from scipy.spatial import distance
import scipy.stats as sc
from GMM_trees import *
import itertools
import multiprocessing
from multiprocessing import Pool

execfile('GMM_trees.py')

# Simulate 100 data sets
samples_temp_2 = simulate_data(mm_dat, 2, 'spherical', 100)
for i in range(len(samples_temp_2)):
    pd.DataFrame(samples_temp_2[i]).to_csv('sim_mammals_2/sim_'+str(i)+'.csv')

print 'fitting simulations mammals 2'

def fit_data(s_data):
    print 'step 1'
    fit_temp_vbgmm = fit_VBGMM(s_data)
    fit_temp_dpp = fit_DPGMM(s_data)
    print 'step 2'
    run_models = unlist([fit_temp_vbgmm[:2], fit_temp_dpp[:2]])
    models_order = np.hstack([fit_temp_vbgmm[2]['BIC'], fit_temp_dpp[2]['BIC']]).argsort()
    best_model = run_models[models_order[0]]

    k_best_model = len(set(best_model.predict(s_data)))
    name_best_model = ['vbgmm_diag', 'vbgmm_shperical', 'dpp_diag', 'dpp_spherical'][models_order[0]]
    return [name_best_model, k_best_model]
    

def fit_data(s_data):
    print 'step 1'
    fit_temp_vbgmm = fit_VBGMM(s_data)
    fit_temp_dpp = fit_DPGMM(s_data)
    print 'step 2'
    run_models = unlist([fit_temp_vbgmm[:2], fit_temp_dpp[:2]])
    models_order = np.hstack([fit_temp_vbgmm[2]['BIC'], fit_temp_dpp[2]['BIC']]).argsort()
    best_model = run_models[models_order[0]]

    k_best_model = len(set(best_model.predict(s_data)))
    name_best_model = ['vbgmm_diag', 'vbgmm_shperical', 'dpp_diag', 'dpp_spherical'][models_order[0]]
    return [name_best_model, k_best_model]
    

p = Pool(4)
s = p.map(fit_data, samples_temp_2)

mm_sims_2 = fit_sim_models(samples_temp_2)
pd.DataFrame(mm_sims_2).to_csv('mm_sims_2.csv')


