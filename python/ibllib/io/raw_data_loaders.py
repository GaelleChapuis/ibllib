# -*- coding:utf-8 -*-
# @Author: Niccolò Bonacchi
# @Date: Monday, July 16th 2018, 1:28:46 pm
# @Last Modified by: Niccolò Bonacchi
# @Last Modified time: 16-07-2018 01:30:26.2626
"""**Raw Data Loader functions for PyBpod rig.**

Module contains one loader function per raw datafile

"""
import os
import json
import numpy as np
import pandas as pd
from dateutil import parser


def load_settings(session_path):
    """
    Load PyBpod Settings files (.json).

    [description]

    :param session_path: Absolute path of session folder
    :type session_path: str
    :return: Settings dictionary
    :rtype: dict
    """
    path = os.path.join(session_path, "raw_behavior_data",
                        "_ibl_pycwBasic.settings.json")
    with open(path, 'r') as f:
        settings = json.loads(f.readline())
    return settings


def load_data(session_path):
    """
    Load PyBpod data files (.jsonable).

    [description]

    :param session_path: Absolute path of session folder
    :type session_path: str
    :return: A list of len ntrials each trial being a dictionary
    :rtype: list of dicts
    """
    path = os.path.join(session_path, "raw_behavior_data",
                        "_ibl_pycwBasic.data.jsonable")
    data = []
    with open(path, 'r') as f:
        for line in f:
            data.append(json.loads(line))
    return data


def load_encoder_events(session_path):
    """
    Load Rotary Encoder (RE) events raw data file.

    Assumes that a folder calles "raw_behavior_data" exists in folder.

    On each trial the RE sends 3 events to Bonsai 1 - meaning trial start/turn
    off the stim; 2 - meaning show the current trial stimulus; and 3 - meaning
    begin the closed loop making the stim move whit the RE. These events are
    triggered by the state machine in the corrensponding states: trial_start,
    stim_on, closed_loop

    Raw datafile Columns:
        Event, RE timestamp, Source, data, Bonsai Timestamp

    Event is always equal 'Event' Source is always equal 'StateMachine'. For
    this reason these columns are dropped.

    >>> data.columns
    >>> ['re_ts',   # Rotary Encoder Timestamp  'numpy.int64'
         'sm_ev',   # State Machine Event       'numpy.int64'
         'bns_ts']  # Bonsai Timestamp          'pandas.Timestamp'
        # pd.to_datetime(data.bns_ts) to work in datetimes

    :param session_path: [description]
    :type session_path: [type]
    :return: dataframe w/ 3 cols and (ntrials * 3) lines
    :rtype: Pandas.DataFrame
    """
    path = os.path.join(session_path, "raw_behavior_data",
                        "_ibl_encoderEvents.bonsai_raw.csv")
    data = pd.read_csv(path, sep=' ', header=None)
    data = data.drop([0, 2, 5], axis=1)
    data.columns = ['re_ts', 'sm_ev', 'bns_ts']
    data.bns_ts = pd.Series([parser.parse(x) for x in data.bns_ts])
    return data


def load_encoder_positions(session_path):
    """
    Load Rotary Encoder (RE) positions from raw data file.

    Assumes that a folder calles "raw_behavior_data" exists in folder.

    Variable line number, depends on movements.

    Raw datafile Columns:
        Position, RE timestamp, RE Position, Bonsai Timestamp

    Position is always equal to 'Position' so this column was dropped.

    >>> data.columns
    >>> ['re_ts',   # Rotary Encoder Timestamp  'numpy.int64'
         're_pos',  # Rotary Encoder position   'numpy.int64'
         'bns_ts']  # Bonsai Timestamp          'pandas.Timestamp'
        # pd.to_datetime(data.bns_ts) to work in datetimes

    :param session_path: Absoulte path of session folder
    :type session_path: str
    :return: dataframe w/ 3 cols and N positions
    :rtype: Pandas.DataFrame
    """
    path = os.path.join(session_path, "raw_behavior_data",
                        "_ibl_encoderPositions.bonsai_raw.csv")
    data = pd.read_csv(path, sep=' ', header=None)
    data = data.drop([0, 4], axis=1)
    data.columns = ['re_ts', 're_pos', 'bns_ts']
    data.bns_ts = pd.Series([parser.parse(x) for x in data.bns_ts])
    return data


def load_encoder_trial_info(session_path):
    """
    Load Rotary Encoder trial info from raw data file.

    Assumes that a folder calles "raw_behavior_data" exists in folder.

    Raw datafile Columns:

    >>> data.columns
    >>> ['trial_num',     # Trial Number                     'numpy.int64'
         'stim_pos_init', # Initial position of visual stim  'numpy.int64'
         'stim_contrast', # Contrast of visual stimulus      'numpy.float64'
         'stim_freq',     # Frequency of gabor patch         'numpy.float64'
         'stim_angle',    # Angle of Gabor 0 = Vertical      'numpy.float64'
         'stim_gain',     # Wheel gain (mm/º of stim)        'numpy.float64'
         'stim_sigma',    # Size of patch                    'numpy.float64'
         'bns_ts' ]       # Bonsai Timestamp                 'pandas.Timestamp'
        # pd.to_datetime(data.bns_ts) to work in datetimes

    :param session_path: Absoulte path of session folder
    :type session_path: str
    :return: dataframe w/ 8 cols and ntrials lines
    :rtype: Pandas.DataFrame
    """
    path = os.path.join(session_path, "raw_behavior_data",
                        "_ibl_encoderTrialInfo.bonsai_raw.csv")
    data = pd.read_csv(path, sep=' ', header=None)
    data = data.drop([8], axis=1)
    data.columns = ['trial_num', 'stim_pos_init', 'stim_contrast', 'stim_freq',
                    'stim_angle', 'stim_gain', 'stim_sigma', 'bns_ts']
    data.bns_ts = pd.Series([parser.parse(x) for x in data.bns_ts])
    return data


if __name__ == '__main__':
    SESSION_PATH = "/home/nico/Projects/IBL/IBL-github/IBL_root/pybpod_data/\
test_mouse/2018-07-11/11"

    settings = load_settings(SESSION_PATH)
    data = load_data(SESSION_PATH)
    eEvents = load_encoder_events(SESSION_PATH)
    ePos = load_encoder_positions(SESSION_PATH)
    eTI = load_encoder_trial_info(SESSION_PATH)

    print("Done!")
