# -*- coding: utf-8 -*-
"""
Module for working with experiment reference strings and local data repos without
the Alyx database.

An experiment reference string has the format 'YYYY-MM-DD_N_NAME' where N corresponds
to the nth experiment for that date, and NAME corresponds to the subject name.

This module assumes that the root directory (i.e. local data repository) has the
following folder structure:
    rootDir/
    ├────── NAME/
            ├───── YYYY-MM-DD/
                   └─────────── N/
        
Created on Mon Sep 10 21:23:27 2018

@author: Miles
"""

from os import listdir
from datetime import datetime
from os.path import join
from os import getcwd
import re

def parse_ref(ref):
    """
    Takes an experiment reference string and returns the subject, a datetime 
    object, and the sequence number as an integer.
    
    Example:
        subject, date, seq = parse_ref('2018-09-30_1_Mouse')
        print(subject)
        >> Mouse
    
    Args:
        ref (str): The experiment reference string
        
    Returns:
        subject (str): The subject name
        date (datetime): Date of the experiment
        seq (int): The experiment number for that date
    
    @author: Miles
    """
    pattern = r'(?P<date>^[0-9\-]+)_(?P<seq>\d+)_(?P<subject>\w+)'
    try:
        out = re.match(pattern,ref).groupdict()
    except:
        raise ValueError('%s could not be parsed', ref)
    return out['subject'], datetime.strptime(out['date'], '%Y-%m-%d'), int(out['seq'])


def construct_ref(subject, date, seq):
    """
    Construct an experiment reference with inputs.
    
    Example:
        ref = parse_ref('Mouse', datetime.date(2018,09,30), 2)
        print(ref)
        >> 2018-09-30_2_Mouse
    
    Args:
        subject (str): The subject name
        date (datetime): Date of the experiment
        seq (int): The experiment number for that date
        
    Returns:
        ref (str): The experiment reference string
    
    @author: Miles
    """
    if isinstance(date, datetime):
        date = date.strftime('%Y-%m-%d')
    return '_'.join([date, str(seq), subject])


def exp_path(ref, rootDir=None):
    """
    Return the full path to an experiment directory given a reference string.
    
    Example:
        path = exp_path('2018-09-30_2_Mouse', r'\\server1\Subjects')
        print(path)
        >> \\server1\Subjects\Mouse\2018-09-30\2
    
    Args:
        subject (str): The subject name
        rootDir (str): The root directory, i.e. where the subject data are stored.
                       If rootDir is None, the current working directory is used.
        
    Returns:
        path (str): The full path of the experiment folder
        
    TODO: Allow path obj as input
    
    @author: Miles
    """
    if rootDir is None:
        rootDir = getcwd()
    subject, date, seq = parse_ref(ref)
    path = join(rootDir, subject, date.strftime('%Y-%m-%d'), str(seq))
    return path


def exps_for_date(subjectPath, datestr):
    """
    Return list of expeiments for a given date.
    
    Example:
        dateDirs = exps_for_date('\\server1\Subjects\Mouse', '2018-09-30', )
        print(dateDirs)
        >> [\\server1\Subjects\Mouse\
    
    Args:
        subjectPath (str): 
        datestr (str): 
        
    Returns:
        dateDirs (str): 
        
    TODO: Allow datetime obj as input
    
    @author: Miles
    """
    dateDirs = listdir(join(subjectPath, datestr))
    dateDirs = [int(d) for d in dateDirs if re.match(r'\d', d)]
    return dateDirs
    

def list_exps(subject, rootDir=None):
    """
    Return a list of all experiments for a given mouse
    
    Example: 
        exps = list_exps('Mouse', rootDir=r'\\server1\Subjects')
        refs = exps[0] # Sublist of experiment reference strings
        dates = exps[1] # Sublist of experiment dates
        
    Args:
        subject (str): The subject name
        rootDir (str): The root directory, i.e. where the subject data are stored.
                       If rootDir is None, the current working directory is used.
        
    Returns:
        ref (list): Nested list of experiment reference strings, one for each date
        date (list): List of datetime objects, one per experiment
        seq (list): Nested list of experiment numbers (one list for each date)
    """
    if rootDir is None:
        rootDir = getcwd()
    subjectPath = join(rootDir, subject)
    subjectDirs = listdir(subjectPath)
    dateStrs = [date for date in subjectDirs if re.match(r'^[0-9\-]{3}', date)]
    seq = [exps_for_date(subjectPath, date) for date in dateStrs]
    ref = [[construct_ref(subject, dateStrs[i], seq[i][n]) for n in range(len(seq[i]))] for i in range(len(dateStrs))]
    date = [datetime.strptime(d, '%Y-%m-%d') for d in dateStrs]
    return ref, date, seq