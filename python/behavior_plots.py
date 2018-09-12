# -*- coding: utf-8 -*-
"""
Created on Tue Sep 11 18:39:52 2018

@author: Miles
"""

import psychofit as psy
import numpy as np
import matplotlib.pyplot as plt

def plot_psychometric(df):
    """
    Plots psychometric data for a given DataFrame of behavioural trials
    
    If the data contains more than six different contrasts (or > three per side)
    the data are fit with an erf function.  The x-axis is percent contrast and 
    the y-axis is the proportion of 'rightward choices', i.e. trials where the 
    subject turned the wheel clockwise to threshold.
    
    Example:
        df = alf.load_behaviour('2018-09-11_1_Mouse1', r'\\server\SubjectData')
        plot_psychometric(df)
        
    Args:
        df (DataFrame): DataFrame constructed from an ALF trials object.
        
    Returns:
        None
    
    TODO Process three response types
    TODO Better handling of graphics; allow axes as input
    TODO Better titling of figure
    TODO Return fit pars if available
    TODO May as well reuse perf_per_contrast?
    """
    
    contrastSet = np.sort(df['contrast'].unique())
    #choiceSet = np.array(set(df['choice']))
    nn = np.array([sum((df['contrast']==c) & (df['included']==True)) for c in contrastSet])
    pp = np.array([sum((df['contrast']==c) & (df['included']==True) & (df['choice']==-1.)) for c in contrastSet])/nn
    ci = 1.96*np.sqrt(pp*(1-pp)/nn)
    
    # graphics
    plt.Figure()
    plt.plot((-100, 100),(.5, .5),'k--', alpha=.5, dashes=(4, 7), linewidth=1)
    if contrastSet.size > 6:
        pars, L = psy.mle_fit_psycho(np.vstack((contrastSet,nn,pp)), 
                                     P_model='erf_psycho_2gammas',
                                     parstart=np.array([np.mean(contrastSet), 3., 0.05, 0.05]),
                                     parmin=np.array([np.min(contrastSet), 10., 0., 0.]), 
                                     parmax=np.array([np.max(contrastSet), 30., .4, .4]))
        plt.errorbar(contrastSet,pp,ci,fmt='ko',mfc='k')
        plt.plot(np.arange(-100,100), psy.erf_psycho_2gammas( pars, np.arange(-100,100) ))
        plt.title('bias = {:.2f}, threshold = {:.2g}, lapse = {:.2g}, {:.2f}'.format(*pars))
        plt.plot((0,0),(0,1),'k:', alpha=.5, dashes=(4, 7), linewidth=1)
    else:
        plt.errorbar(contrastSet[contrastSet<0],pp[contrastSet<0],ci[contrastSet<0],fmt='k-o',mfc='k')
        plt.errorbar(contrastSet[contrastSet>0],pp[contrastSet>0],ci[contrastSet>0],fmt='k-o',mfc='k')
        pars = None
    ax = plt.gca()
    
    # Hide the right and top spines
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    # Set bounds of axes lines
    ax.spines['left'].set_bounds(0, 1)
    ax.spines['bottom'].set_bounds(-100, 100)
    # Explode out axes
    ax.spines['left'].set_position(('outward',10))
    ax.spines['bottom'].set_position(('outward',10))
    # Reduce the clutter
    plt.xticks([-100, -50, 0, 50, 100])
    plt.yticks([0, .5, 1])
    # Set the limits
    plt.xlim([-102, 102])
    plt.ylim([0., 1.])
    plt.xlabel('Contrast (%)')
    #plt.ylabel('Rightward choices')
    plt.show()
    #plt.tick_params(top='off', bottom='off', left='off', right='off', labelleft='off', labelbottom='on')
    
    
def plot_RTs(df):
    """
    Scatter plot of responses, given a data frame of trials
    
    On the x-axis is trial number and on the y-axis, the response time in seconds,
    defined as the time between the go cue and a response being recorded.
    
    Example:
        df = alf.load_behaviour('2018-09-11_1_Mouse1', r'\\server\SubjectData')
        plot_RTs(df)
        
    Args:
        df (DataFrame): DataFrame constructed from an ALF trials object.
        
    Returns:
        None
    """
    response_times = df['response_times']-df['goCue_times']
    plt.Figure()
    #print(np.array(df.index[df['choice']==1.].tolist())+1)
    leftWrong = (df['choice']==1.) & (df['feedbackType']==-1.)
    leftRight = (df['choice']==1.) & (df['feedbackType']==1.)
    rightWrong = (df['choice']==-1.) & (df['feedbackType']==-1.)
    rightRight = (df['choice']==-1.) & (df['feedbackType']==1.)
    plt.scatter(np.where(leftWrong)[0]+1, response_times[leftWrong], marker='<', c='r', alpha=0.5, label='Left incorrect')
    plt.scatter(np.where(leftRight)[0]+1, response_times[leftRight], marker='<', c='k', alpha=0.5, label='Left correct')
    plt.scatter(np.where(rightWrong)[0]+1, response_times[rightWrong], marker='>', c='r', alpha=0.5, label='Right incorrect')
    plt.scatter(np.where(rightRight)[0]+1, response_times[rightRight], marker='>', c='k', alpha=0.5, label='right correct')
    plt.yscale('log')
    ax = plt.gca()
    # Hide the right and top spines
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    # Set bounds of axes lines
    #ax.spines['left'].set_bounds(0, 1)
    ax.spines['bottom'].set_bounds(0, len(df.index))
    # Explode out axes
    ax.spines['left'].set_position(('outward',10))
    ax.spines['bottom'].set_position(('outward',10))
    plt.xlabel('Trial')
    # Add second x
    #ax2 = ax.twiny()
    #plt.xlim([0 1])
    # Set the limits
    plt.ylim([min(response_times), max(response_times)+1])
    #plt.ylabel('Rightward choices')
    plt.legend(loc=0, frameon=True, fancybox=True)
    #plt.legend(bbox_to_anchor=(-.03, 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
    plt.show()


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
    plt.show()
