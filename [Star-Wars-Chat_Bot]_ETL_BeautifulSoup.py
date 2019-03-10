##############################################################################
# Title:       [Star-Wars-Chat_Bot]_ParseScripts.py
# Description: To parse Star Wars scripts (.txt) in to dialogue
#              documents
# Input file (/StarWars Scripts/..) -> Output file (/StarWars Dialogues/..):
#     StarWars_EpisodeIII_script.txt -> StarWars_EpisodeIII_dialogues.tsv
#     StarWars_EpisodeIV_script.txt -> StarWars_EpisodeIV_dialogues.tsv
#     StarWars_EpisodeVI_script.txt -> StarWars_EpisodeVI_dialogues.tsv
# Author:      Kunyu He
##############################################################################


import re
import requests
import bs4

# Party line of names
NAME_DICT = {'BEN': "OBI-WAN",
             'THREEPIO': "C-3PO",
             'DARTH SlDIOUS': "DARTH SIDIOUS",
             'PALPATINE': "DARTH SIDIOUS",
             'EMPEROR': "DARTH SIDIOUS",
             'FlRESHIP PILOT': "FIRESHIP PILOT",
             'GlDDEAN DANU': "GIDDEAN DANU",
             'GiDDEAN DANU': "GIDDEAN DANU",
             'Kl-ADI-MUNDI': "KI-ADI-MUNDI",
             'TlON MEDON': "TION MEDON",
             'MACE WlNDU': "MACE WINDU",
             'MACE WiNDU': "MACE WINDU",
             'FANGZAR': "FANG ZAR",
             'QUI -GON': "QUI-GON",
             'PADMÉ': "PADME",
             'CORDÉ': "CORDE"}


def read_script(name, encoding=None):
    """
    Given name of the script file, reads it with assigned encoding method and
    returns a list of lines in the script with newline char removed.

    Inputs:
        name (string): name and extension of the script text file
        encoding (string): encoding method of the script file, i.e. 'gbk'

    Outputs:
        (list of strings) of lines in the script with newline char removed
    """
    with open('StarWars Scripts/' + name, 'r', encoding=encoding) as f:
        return [line.rstrip("\n") for line in f.readlines()]


def line_type(line, num_spaces):
    """
    Given a line, determines its type rouoghly by counting leading white
    spaces. Returns True if it equals to the desired number.

    Inputs:
        - line (string): a line from the list to check
        - num_spaces (int): number of spaces desired

    Returns:
        (Bool) True if the number of leading white spaces equals to our
        desired number
    """
    return len(line) - len(line.lstrip()) == num_spaces


def clean_name(line, name_party_line=NAME_DICT):
    """
    Given a line containing a name, parses the line and returns the name.

    Inputs:
        - line (string): a line from the list
        - name_party_line (dict): takes care of wrong spellings

    Returns:
        (string) cleaned name
    """
    name = line.strip()
    if ("'S") in name:
        name = re.search(r"^[A-Z0-9\s]+[^']", name).group().strip()
    name = name_party_line.get(name, name)

    name = re.search(r"^[A-Z0-9\s-]+[^a-z]", line.strip())
    if not name:
        pass
    name = re.sub(r"[\(\[].*?[\)\]]", "", name.group()).strip()

    return name
