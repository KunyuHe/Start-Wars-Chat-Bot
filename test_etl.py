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


from os import listdir, R_OK, access, system
from os.path import getsize, isfile

SCRIPTS_DIR = "[Star-Wars-Chat-Bot]data/Scripts/"
DIALOGUES_DIR = "[Star-Wars-Chat-Bot]data/Dialogues/"


#----------------------------------------------------------------------------#
def check_file(file_name, extension, directory=SCRIPTS_DIR):
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
    if not all([file_name.endswith(extension), getsize(full_path) > 0,
                isfile(full_path), access(full_path, R_OK)]):
        raise AssertionError()


# Test Scripts---------------------------------------------------------------#
def test_scripts_accessible(directory=SCRIPTS_DIR):
    """
    Test whether the scripts files are accessible for further anaylysis.
    """
    for file_name in listdir(directory):
        check_file(file_name, ".txt", directory)


# Test Dialogues-------------------------------------------------------------#
def test_dialogues_accessible(directory=DIALOGUES_DIR):
    """
    Test whether the dialogues files are accessible for further anaylysis.
    """
    for file_name in listdir(directory):
        check_file(file_name, ".tsv", directory)


#----------------------------------------------------------------------------#
system("python etl_get_dialogues.py")
system("python etl_get_scripts_bs4.py")
