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

SCRIPTS_DIR = "[Star-Wars-Chat-Bot]data/Scripts/"
DIALOGUES_DIR = "[Star-Wars-Chat-Bot]data/Dialogues/"

SCRIPTS = [file for file in os.listdir(SCRIPTS_DIR)]
DIALOGUES = [file for file in os.listdir(DIALOGUES_DIR)]


#----------------------------------------------------------------------------#
def check_file(file_name, extension, directory):
    """
    Check whether a file is in the right format, contains at least some
    information, and is readable.

    Inputs:
        - file_name (string): name of the file
        - extension (string): e.g. ".txt"
        - dir (string): path to the directory where the file is

    Returns:
        (None) make assertions if any condition fails
    """
    full_path = directory + file_name
    if not file_name.endswith(extension):
        raise AssertionError()
    if not os.path.getsize(full_path) > 0:
        raise AssertionError()
    if not os.path.isfile(full_path) and os.access(full_path, os.R_OK):
        raise AssertionError()


# Test Scripts---------------------------------------------------------------#
@pytest.mark.parametrize("script", SCRIPTS)
def test_script_accessible(script, directory=SCRIPTS_DIR):
    """
    Test whether the scripts files are accessible for further anaylysis.
    """
    check_file(script, ".txt", directory)


# Test Dialogues-------------------------------------------------------------#
@pytest.mark.parametrize("dialogue", DIALOGUES)
def test_dialogues_accessible(dialogue, directory=DIALOGUES_DIR):
    """
    Test whether the dialogues files are accessible for further anaylysis.
    """
    check_file(dialogue, ".tsv", directory)
