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


import pytest
import os
import re

from etl_get_scripts_bs4 import go as scripts_go
from os import listdir, R_OK, access
from os.path import getsize, isfile

SCRIPTS_DIR = "[Star-Wars-Chat-Bot]data/Scripts/"
DIALOGUES_DIR = "[Star-Wars-Chat-Bot]data/Dialogues/"


# Test Scripts---------------------------------------------------------------#
def test_scripts_go(dir=SCRIPTS_DIR):
    """
    Test whether a script text file contains anything and is readable.
    """
    scripts_go()

    for file_name in listdir(SCRIPTS_DIR):
        full_path = SCRIPTS_DIR + file_name
        assert file_name.endswith(".txt")
        assert getsize(full_path) > 0
        assert isfile(full_path) and access(full_path, R_OK)


# Test Dialogues-------------------------------------------------------------#