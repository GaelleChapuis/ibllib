# -*- coding: utf-8 -*-
"""
Created on Tue Sep 11 19:16:45 2018

@author: Miles
"""

import numpy as np
import matplotlib.pyplot as plt

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
    df['response_times'] = df['response_times']-df['goCue_times']
    plt.Figure()
    #print(np.array(df.index[df['choice']==1.].tolist())+1)
    leftWrong = (df['choice']==1.) & (df['feedbackType']==-1.)
    leftRight = (df['choice']==1.) & (df['feedbackType']==1.)
    rightWrong = (df['choice']==-1.) & (df['feedbackType']==-1.)
    rightRight = (df['choice']==-1.) & (df['feedbackType']==1.)
    plt.scatter(np.where(leftWrong)[0]+1, df['response_times'][leftWrong], marker='<', c='r', alpha=0.5, label='Left incorrect')
    plt.scatter(np.where(leftRight)[0]+1, df['response_times'][leftRight], marker='<', c='k', alpha=0.5, label='Left correct')
    plt.scatter(np.where(rightWrong)[0]+1, df['response_times'][rightWrong], marker='>', c='r', alpha=0.5, label='Right incorrect')
    plt.scatter(np.where(rightRight)[0]+1, df['response_times'][rightRight], marker='>', c='k', alpha=0.5, label='right correct')
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
    plt.ylim([df['response_times'].min(), df['response_times'].max()+1])
    #plt.ylabel('Rightward choices')
    plt.legend(loc=0, frameon=True, fancybox=True)
    #plt.legend(bbox_to_anchor=(-.03, 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
    plt.show()
