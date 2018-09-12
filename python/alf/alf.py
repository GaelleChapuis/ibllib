# -*- coding: utf-8 -*-
"""
Module for identifying, and working with, ALF files.

An ALF file has the following components (those in brackets are optional):
    (_namespace_)object.attricbute(_timescale).ext
    
For more information, see the folloing documentation:
    https://github.com/cortex-lab/ALF


Created on Tue Sep 11 18:06:21 2018

@author: Miles
"""

import re, dat
import numpy as np
import pandas as pd
from os import listdir, getcwd
from os.path import isfile, join


def is_alf(fileName):
    """
    Returns a True for a given file name if it is an ALF file, otherwise 
    returns False
    
    Examples:
        match = is_alf('trials.feedbackType.npy')
        match == True
        >> True
        match = is_alf('config.txt')
        match == False
        >> True
    
    Args:
        fileName (str): The name of the file
        
    Returns:
        bool
    
    @author: Miles
    """
    pattern = r'(?P<obj>.+)\.(?P<typ>.+)\.(?P<ext>.+)'
    out = re.match(pattern, fileName)
    return out is not None


def alf_parts(fileName):
    """
    Return the object, type and extention for a given ALF file name
    
    Example:
        obj, typ, ext = alf_parts('trials.choice.npy')
        ('trials', 'choice', 'npy')
    
    Args:
        fileName (str): The name of the file
        
    Returns:
        obj (str): ALF object
        typ (str): The ALF attribute
        ext (str): The file extension
        
    TODO: Deal with namespaces
    
    @author: Miles
    """
    try:
        obj, typ, ext = fileName.split('.')
    except:
        print(fileName)
    return obj, typ, ext


def load_behavior(ref, rootDir=None):
    """
    Load the trials for a given experiment reference
    
    Example:
        df = load_behaviour('2018-09-11_1_MOUSE', rootDir = r'\\server1\Subjects')
        df.head()
        
    Args: 
        subject (str): The subject name
        rootDir (str): The root directory, i.e. where the subject data are stored.
                       If rootDir is None, the current working directory is used.
        
    Returns:
        df (DataFrame): DataFrame constructed from the trials object of the ALF 
                        files located in the experiment directory
                        
    TODO: Deal with namespaces: currently hard-coded
    """
    if rootDir is None:
        rootDir = getcwd()
    path = dat.exp_path(ref, rootDir)
    alfs = [f for f in listdir(path) if (isfile(join(path, f))) & (is_alf(f))]
    parts = [alf_parts(alf) for alf in alfs]
    # List of 'trials' attributes
    attr = [parts[i][1] for i in range(len(parts)) if parts[i][0].startswith('_ibl_trials')]
    attr.extend(['trialStart', 'trialEnd'])
    # Pull paths of trials ALFs
    trials = [join(path,f) for f in alfs if f.startswith('_ibl_trials')]
    if not trials:
        print('{}: Nothing to process'.format(ref))
        return
    # Load arrays into dictionary
    trialsDict = dict.fromkeys(attr)
    for p,name in zip(trials, attr):
        trialsDict[name] = np.load(p).squeeze()
    # Check all arrays the same length
    lengths = [len(val) for val in [trialsDict.values()]]
    assert len(set(lengths))==1,'Not all arrays in trials the same length'
    # Deal with intervals
    trialsDict['trialStart'] = trialsDict['intervals'][:,0]
    trialsDict['trialEnd'] = trialsDict['intervals'][:,1]
    trialsDict.pop('intervals', None)
    # Create data from from trials dict
    df = pd.DataFrame(trialsDict)
    df['contrast'] = (df['contrastRight']-df['contrastLeft'])*100
    return df