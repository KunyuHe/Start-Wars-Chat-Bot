"""
Title:       test_etl.py
Description: Test code for checking the ETL output, including the scripts
             parsed from web and dialogues parsed from scripts.
Tested Files:
    ([Star-Wars-Chat-Bot]data/Scripts)
        EpisodeII_script.txt
        EpisodeIII_script.txt
    ([Star-Wars-Chat-Bot]data/Dialogues)
        EpisodeII_dialogues.tsv
        EpisodeIII_dialogues.tsv
        EpisodeIV_dialogues.tsv
        EpisodeV_dialogues.tsv
        EpisodeVI_dialogues.tsv
Author:      Kunyu He
"""

import os
import pytest
import subprocess
import pandas as pd

SCRIPTS_DIR = "[Star-Wars-Chat-Bot]data/Scripts/"
DIALOGUES_DIR = "[Star-Wars-Chat-Bot]data/Dialogues/"

TEST_ETL_SCRIPTS = [file for file in os.listdir() if file.startswith("etl_")]

TEST_ACCESS = [(SCRIPTS_DIR + f, None) for f in os.listdir(SCRIPTS_DIR)] + \
    [(None, DIALOGUES_DIR + f) for f in os.listdir(DIALOGUES_DIR)]

TEST_DIALOGUES = [DIALOGUES_DIR + f for f in os.listdir(DIALOGUES_DIR)]


#----------------------------------------------------------------------------#
def check_file(full_path, extension):
    """
    Check whether a file is in the right format, contains at least some
    information, and is readable.

    Inputs:
        - full_path (string): path to the file
        - extension (string): e.g. ".txt"

    Returns:
        (None) make assertions if any condition fails
    """
    if not full_path.endswith(extension):
        raise AssertionError()
    if not os.path.getsize(full_path) > 0:
        raise AssertionError()
    if not os.path.isfile(full_path) and os.access(full_path, os.R_OK):
        raise AssertionError()


#----------------------------------------------------------------------------#
@pytest.mark.parametrize("etl_script", TEST_ETL_SCRIPTS)
def test_etl_script(etl_script):
    """
    Test whether the etl python sxcripts run well.
    """
    if subprocess.call("python " + etl_script, shell=True) != 0:
        raise AssertionError()


@pytest.mark.parametrize("script,dialogue", TEST_ACCESS)
def test_file_accessible(script, dialogue):
    """
    Test whether the data files are accessible for further anaylysis.
    """
    if script:
        check_file(script, ".txt")
    if dialogue:
        check_file(dialogue, ".tsv")


@pytest.mark.parametrize("dialogue", TEST_DIALOGUES)
def test_dialogues(dialogue):
    """
    Test whether the .tsv dialogue files contain two columns for each row and
    are ready for further analysis.  
    """
    data = pd.read_csv(dialogue, delimiter="\t", header=None, encoding='gbk')
    if any(data.isnull().sum(axis=1) != 0):
        raise AssertionError()
