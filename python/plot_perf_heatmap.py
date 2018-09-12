# -*- coding: utf-8 -*-
"""
Created on Tue Sep 11 19:26:36 2018

@author: Miles
"""

import numpy as np
import matplotlib.pyplot as plt

def perf_per_contrast(df):
    """
    Returns the proportion of 'rightward chocies', given a dataframe of trials.
    Each value corresponds to a contrast, going from highest contrast on the left
    to highest contrast on the right.
        
    Example:
        df = alf.load_behaviour('2018-09-11_1_Mouse1', r'\\server\SubjectData')
        pp = perf_per_contrast(df)
        >> [0., 0.2, 0., 0.8, 0.9]
        
    Args:
        df (DataFrame): DataFrame constructed from an ALF trials object.
        
    Returns:
        pp (numpy.Array): An array of the size (n,) where n is the number of 
                          contrasts.  Each value is the proportion of 
                          'rightward choices', i.e. trials where the subject 
                          turned the wheel clockwise to threshold
    
    TODO: Optional contrast set input
    """
    contrastSet = (-100., -50., -25., -12.5, -0.06, 0., 0.06, 12.5, 25., 50., 100.)
    nn = np.array([sum((df['contrast']==c) & (df['included']==True)) for c in contrastSet], dtype=float)
    nn[nn == 0] = np.nan
    pp = np.array([sum((df['contrast']==c) & (df['included']==True) & (df['choice']==1.)) for c in contrastSet])/nn
    return pp

def plot_perf_heatmap(dfs, ax=None):
    """
    Plots a heat-map of performance for each contrast per session.
    
    The x-axis is the contrast, going from highest contrast on the left to 
    highest contrast on the right.  The y-axis is the session number, ordered 
    from most recent.  
        
    Example:
        refs, date, seq = list_exps('Mouse1', rootDir = r'\\server\Data')
        dfs = [load_behaviour(ref[0]) for ref in refs]
        plot_perf_heatmap(dfs)
        
    Args:
        dfs (List): List of data frames constructed from an ALF trials object.
        
    Returns:
        None
    
    TODO: Optional contrast set input
    """
    pp = np.vstack([perf_per_contrast(df) for df in dfs])
    pp = np.ma.array(pp, mask=np.isnan(pp))
    if ax is None:
        plt.Figure()
        ax = plt.gca()
    import copy; cmap=copy.copy(plt.get_cmap('bwr'))
    cmap.set_bad('grey',1.)
    ax.imshow(pp, extent=[0, 1, 0, 1], cmap=cmap, vmin = 0, vmax = 1)
    ax.set_xticks([0.05, .5, 0.95])
    ax.set_xticklabels([-100, 0, 100])
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    # Set bounds of axes lines
    #ax.spines['left'].set_bounds(0, 1)
    #ax.spines['bottom'].set_bounds(0, len(df.index))
    # Explode out axes
    #ax.spines['left'].set_position(('outward',10))
    ax.spines['bottom'].set_position(('outward',10))
